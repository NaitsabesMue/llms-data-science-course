"""HTML extraction and experiment records for the Week 5 notebook.

Retrieval, prompts, API calls and the answer--review loop stay visible in the
notebook. This module performs no downloads or API requests on import.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
from uuid import uuid4

from bs4 import BeautifulSoup
import pandas as pd
import requests


def extract_sections(html):
    """Keep headings and paragraphs from the page's main content."""
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.select_one('main') or soup.select_one('article')
    if main is None:
        raise ValueError('No main/article element found; inspect the page before extracting it.')
    for node in main.select('script, style, nav, footer, aside, form, button, [role="navigation"]'):
        node.decompose()
    heading, sections, seen = [], [], set()
    for node in main.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'li']):
        # AMU's FAQ uses list items as containers for headings and paragraphs.
        # Read their children, not the whole accordion as one duplicated string.
        if node.name == 'li' and node.find(['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'li']):
            continue
        text = ' '.join(node.get_text(' ', strip=True).split())
        if not text:
            continue
        if node.name.startswith('h'):
            level = int(node.name[1:])
            heading = [(n, t) for n, t in heading if n < level] + [(level, text)]
            continue
        section = ' > '.join(t for _, t in heading)
        if (section, text) not in seen:
            sections.append({'heading': section, 'text': text})
            seen.add((section, text))
    if not sections:
        raise ValueError('No paragraphs found; inspect the HTML rather than indexing an empty page.')
    return sections


def load_or_download(source, cache_dir, session, fallback_dir=None):
    """Reuse cached HTML; try the website, then a labelled course snapshot."""
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(source['url'].encode()).hexdigest()[:16]
    html_path = cache_dir / f'{key}.html'
    info_path = cache_dir / f'{key}.json'
    cached = html_path.exists() and info_path.exists()
    if cached:
        raw = html_path.read_bytes()
        info = json.loads(info_path.read_text())
        if info['sha256'] != hashlib.sha256(raw).hexdigest():
            raise ValueError(f'Cached HTML changed: {html_path}. Start a new snapshot directory.')
    else:
        try:
            response = session.get(source['url'], timeout=(5, 30))
            response.raise_for_status()
            if 'html' not in response.headers.get('Content-Type', '').lower():
                raise ValueError(f"Expected an HTML page: {source['url']}")
            raw = response.content
            extract_sections(raw)
            info = {'url': response.url, 'downloaded_at': datetime.now(timezone.utc).isoformat(),
                    'sha256': hashlib.sha256(raw).hexdigest(), 'data_origin': 'website'}
        except (requests.RequestException, ValueError) as error:
            if fallback_dir is None:
                raise
            folder = Path(fallback_dir)
            info = json.loads((folder / f"{source['id']}.json").read_text())
            raw = (folder / f"{source['id']}.html").read_bytes()
            if info['url'] != source['url'] or info['sha256'] != hashlib.sha256(raw).hexdigest():
                raise ValueError(f"Course snapshot URL/checksum mismatch: {source['id']}") from error
            info = {**info, 'data_origin': 'course_snapshot',
                    'download_error': f'{type(error).__name__}: {error}'}
        extract_sections(raw)  # Do not save an unusable page as a successful download.
        html_path.write_bytes(raw)
        info_path.write_text(json.dumps(info, ensure_ascii=False, indent=2))
    if info.get('data_origin') == 'course_snapshot':
        print(f"{source['id']}: using the course snapshot from {info['downloaded_at']} "
              f"(website download failed: {info['download_error']}).")
    return {**source, **info, 'data_origin': info.get('data_origin', 'website'),
            'sections': extract_sections(raw), 'from_cache': cached}


def make_chunks(documents, max_words=80):
    """Group adjacent paragraphs under a heading, then split long sections."""
    if max_words < 1:
        raise ValueError('max_words must be positive.')
    chunks = []
    for doc in documents:
        sections = []
        for section in doc['sections']:
            if sections and sections[-1]['heading'] == section['heading']:
                sections[-1]['text'] += '\n' + section['text']
            else:
                sections.append(dict(section))
        for paragraph, section in enumerate(sections):
            words = section['text'].split()
            for part, start in enumerate(range(0, len(words), max_words)):
                text = ' '.join(words[start:start + max_words])
                chunks.append({
                    'chunk_id': f"{doc['id']}_p{paragraph}_{part}",
                    'doc_id': doc['id'], 'title': doc['title'], 'scope': doc['scope'],
                    'heading': section['heading'], 'text': text, 'url': doc['url'],
                    'downloaded_at': doc['downloaded_at'], 'source_sha256': doc['sha256'],
                })
    return chunks


def build_context(chunks):
    return '\n\n'.join(
        f"[{c['chunk_id']}] {c['title']} | {c['scope']}\n"
        f"Section: {c['heading']}\nURL: {c['url']}\n{c['text']}"
        for c in chunks
    )


def retrieval_metrics(retrieved_ids, relevant_ids):
    retrieved, relevant = set(retrieved_ids), set(relevant_ids)
    found = len(retrieved & relevant)
    return {'precision': found / len(retrieved) if retrieved else 0.0,
            'recall': found / len(relevant) if relevant else None}


def web_evidence(response):
    """Retain source and claim mappings as well as reported search queries."""
    candidates = getattr(response, 'candidates', None) or []
    grounding = getattr(candidates[0], 'grounding_metadata', None) if candidates else None
    data = grounding.model_dump(mode='json', exclude_none=True) if grounding else {}
    queries = list(dict.fromkeys(q.strip() for q in data.get('web_search_queries', []) if q.strip()))
    sources = [c['web'] for c in data.get('grounding_chunks', []) if c.get('web')]
    return {'queries': queries, 'sources': sources, 'grounding': data,
            'search_evidenced': bool(queries)}


# Standard paid-tier rates verified 2026-10-21. An estimate, not an account bill:
# free allowances, caching discounts and local computing costs are not applied.
# Gemini 3.8 Flash's listed rates change on 2027-01-01.
PRICES = {
    'gemini-3.5-flash-lite': {'input': 0.30, 'output': 2.50, 'search': 0.014},
    'gemini-3.8-flash': {'input': 0.75, 'output': 3.75, 'search': 0.014},
}
PRICE_CHECKED_ON = '2026-10-21'


def record_call(log, response, model, role, elapsed_s, error, web_search=False):
    usage = getattr(response, 'usage_metadata', None)
    count = lambda field: getattr(usage, field, None) if usage is not None else None
    evidence = web_evidence(response)
    # If the provider does not report search queries, do not invent a count.
    queries = len(evidence['queries']) if evidence['queries'] else (None if web_search else 0)
    row = {
        'model': model, 'role': role, 'elapsed_s': elapsed_s,
        'status': 'failed' if error else 'completed', 'error': error,
        'input_tokens': count('prompt_token_count'),
        'output_tokens': count('candidates_token_count'),
        'thinking_tokens': count('thoughts_token_count'),
        'total_tokens': count('total_token_count'),
        'reported_search_queries': queries,
        'model_version': getattr(response, 'model_version', None),
    }
    rates = PRICES.get(model)
    needed = [row[k] for k in ('input_tokens', 'output_tokens', 'thinking_tokens')]
    row['token_cost_estimate_usd'] = (
        (needed[0] * rates['input'] + (needed[1] + needed[2]) * rates['output']) / 1_000_000
        if rates and all(v is not None for v in needed) else None
    )
    row['search_cost_estimate_usd'] = rates['search'] * queries if rates and queries is not None else None
    parts = [row['token_cost_estimate_usd'], row['search_cost_estimate_usd']]
    row['cost_estimate_usd'] = sum(parts) if all(v is not None for v in parts) else None
    log.append(row)
    return row


def run_experiment(name, task, log, results, work):
    """Run one workflow; keep failures and every call; replace only its display row."""
    start, first_call = time.perf_counter(), len(log)
    result = {'name': name, 'run_id': uuid4().hex, 'started_at': datetime.now(timezone.utc).isoformat()}
    try:
        result.update(task())
        result.setdefault('status', 'completed')
    except Exception as error:
        result.update(status='failed', error=f'{type(error).__name__}: {error}', answer=None)
    result['elapsed_s'] = time.perf_counter() - start
    result['calls'] = list(log[first_call:])
    results[name] = result
    target = Path(work) / 'runs'
    target.mkdir(parents=True, exist_ok=True)
    (target / f"{result['run_id']}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(name, '|', result['status'])
    print(result.get('answer') or result.get('error') or 'No answer returned.')
    return result


def comparison_table(results):
    rows = []
    for name, result in results.items():
        calls = result['calls']
        row = {'workflow': name, 'status': result['status'], 'seconds': result['elapsed_s'],
               'model_calls': len(calls)}
        for field in ('input_tokens', 'output_tokens', 'thinking_tokens', 'total_tokens',
                      'reported_search_queries', 'cost_estimate_usd'):
            values = [c[field] for c in calls]
            row[field] = sum(values) if values and all(v is not None for v in values) else None
        rows.append(row)
    return pd.DataFrame(rows)
