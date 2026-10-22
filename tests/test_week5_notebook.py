"""No network or paid calls: check collection, provenance and usage accounting."""
import hashlib
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock
import requests

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('week5_helpers', ROOT / 'labs/week5_helpers.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

HTML = b'''<html><main><nav>Ignore menu</nav><h2>Other service</h2>
<li class="accordion-item"><h2>Lost card</h2><div>
<p>Request a replacement through the portal.</p><ul><li>Bring ID.</li></ul>
</div></li><footer>Ignore footer</footer></main></html>'''
SOURCE = {'id': 'A', 'title': 'Administration', 'url': 'https://example.org/amu', 'scope': 'IUT'}


class Week5NotebookTests(unittest.TestCase):
    def test_accordion_heading_and_text_are_preserved_once(self):
        sections = h.extract_sections(HTML)
        self.assertEqual([s['heading'] for s in sections], ['Lost card', 'Lost card'])
        self.assertEqual([s['text'] for s in sections],
                         ['Request a replacement through the portal.', 'Bring ID.'])
        with self.assertRaises(ValueError):
            h.extract_sections('<html><body>No main content.</body></html>')

    def test_cached_snapshot_is_reused_and_tampering_detected(self):
        response = Mock(content=HTML, url=SOURCE['url'], headers={'Content-Type': 'text/html'})
        session = Mock()
        session.get.return_value = response
        with TemporaryDirectory() as folder:
            first = h.load_or_download(SOURCE, folder, session)
            second = h.load_or_download(SOURCE, folder, session)
            session.get.assert_called_once()
            self.assertFalse(first['from_cache'])
            self.assertTrue(second['from_cache'])
            self.assertEqual(first['downloaded_at'], second['downloaded_at'])
            next(Path(folder).glob('*.html')).write_text('Changed')
            with self.assertRaises(ValueError):
                h.load_or_download(SOURCE, folder, session)

    def test_failed_download_does_not_create_successful_cache(self):
        session = Mock()
        session.get.return_value.raise_for_status.side_effect = RuntimeError('HTTP failure')
        with TemporaryDirectory() as folder:
            with self.assertRaises(RuntimeError):
                h.load_or_download(SOURCE, folder, session)
            self.assertFalse(list(Path(folder).iterdir()))

    def test_timeout_uses_real_dated_snapshot_and_reuses_it(self):
        examples = ROOT / 'slides/examples/week5_retrieval'
        sources = json.loads((examples / 'amu_sources.json').read_text())['sources']
        session = Mock()
        session.get.side_effect = requests.ConnectTimeout('Test connection timeout')
        with TemporaryDirectory() as folder:
            for source in sources:
                first = h.load_or_download(source, folder, session, examples / 'snapshots')
                second = h.load_or_download(source, folder, session, examples / 'snapshots')
                self.assertEqual(first['data_origin'], 'course_snapshot')
                self.assertEqual(first['downloaded_at'], '2026-10-21')
                self.assertEqual(first['url'], source['url'])
                self.assertIn('ConnectTimeout', first['download_error'])
                self.assertTrue(first['sections'])
                self.assertTrue(second['from_cache'])
                self.assertEqual(first['sections'], second['sections'])
            self.assertEqual(session.get.call_count, len(sources))
            self.assertEqual(session.get.call_args.kwargs['timeout'], (5, 30))

    def test_invalid_fallback_is_not_cached(self):
        session = Mock()
        session.get.side_effect = requests.ConnectTimeout('Test timeout')
        with TemporaryDirectory() as folder:
            fallback = Path(folder) / 'fallback'
            fallback.mkdir()
            (fallback / 'A.html').write_bytes(HTML)
            (fallback / 'A.json').write_text(json.dumps(
                {'url': SOURCE['url'], 'sha256': 'wrong', 'downloaded_at': '2026-10-21'}))
            cache = Path(folder) / 'cache'
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                h.load_or_download(SOURCE, cache, session, fallback)
            self.assertFalse(list(cache.iterdir()))

    def test_chunks_keep_source_and_stable_ids(self):
        doc = {**SOURCE, 'sections': h.extract_sections(HTML), 'downloaded_at': '2026-10-21',
               'sha256': hashlib.sha256(HTML).hexdigest()}
        chunks = h.make_chunks([doc], max_words=5)
        self.assertEqual(chunks, h.make_chunks([doc], max_words=5))
        self.assertEqual(len({c['chunk_id'] for c in chunks}), len(chunks))
        self.assertTrue(all(c['url'] == SOURCE['url'] and c['heading'] == 'Lost card' for c in chunks))
        self.assertTrue(all(len(c['text'].split()) <= 5 for c in chunks))
        context = h.build_context(chunks[-1:])
        self.assertIn(chunks[-1]['chunk_id'], context)
        self.assertIn(SOURCE['url'], context)
        self.assertIn(doc['sha256'], chunks[-1]['source_sha256'])

    def test_metrics_use_fixed_reference_set_and_handle_missing_reference(self):
        self.assertEqual(h.retrieval_metrics(['D1', 'D2'], ['D2', 'D3']),
                         {'precision': 0.5, 'recall': 0.5})
        self.assertIsNone(h.retrieval_metrics(['D1'], [])['recall'])

    def test_unreported_usage_and_search_are_unknown(self):
        log = []
        row = h.record_call(log, None, 'gemini-3.5-flash-lite', 'web', 1, 'Unavailable', True)
        self.assertEqual(row['status'], 'failed')
        for field in ['input_tokens', 'total_tokens', 'reported_search_queries', 'cost_estimate_usd']:
            self.assertIsNone(row[field])

    def test_thinking_and_unique_search_queries_are_in_cost_estimate(self):
        grounding = Mock()
        grounding.model_dump.return_value = {
            'web_search_queries': ['lost card', 'lost card', '', 'AMU card'],
            'grounding_chunks': [{'web': {'uri': 'https://example.org/amu', 'title': 'Card'}}],
            'grounding_supports': [{'grounding_chunk_indices': [0]}],
        }
        response = SimpleNamespace(
            usage_metadata=SimpleNamespace(prompt_token_count=100, candidates_token_count=30,
                                           thoughts_token_count=20, total_token_count=150),
            candidates=[SimpleNamespace(grounding_metadata=grounding)], model_version='test',
        )
        evidence = h.web_evidence(response)
        self.assertTrue(evidence['search_evidenced'])
        self.assertEqual(len(evidence['sources']), 1)
        self.assertIn('grounding_supports', evidence['grounding'])
        row = h.record_call([], response, 'gemini-3.5-flash-lite', 'web', 1, None, True)
        self.assertAlmostEqual(row['cost_estimate_usd'], (100 * 0.30 + 50 * 2.50) / 1e6 + 2 * 0.014)

    def test_latest_experiment_does_not_count_earlier_calls(self):
        log, results = [], {}
        def successful():
            h.record_call(log, None, 'gemini-3.5-flash-lite', 'answer', 1, None)
            return {'answer': 'Test only.'}
        def failed():
            h.record_call(log, None, 'gemini-3.5-flash-lite', 'answer', 1, 'Timeout')
            raise TimeoutError('Test timeout')
        with TemporaryDirectory() as folder:
            h.run_experiment('RAG', successful, log, results, folder)
            h.run_experiment('RAG', failed, log, results, folder)
            table = h.comparison_table(results)
            self.assertEqual(len(list((Path(folder)/'runs').glob('*.json'))), 2)
            self.assertEqual(table.iloc[0]['status'], 'failed')
            self.assertEqual(table.iloc[0]['model_calls'], 1)
            self.assertEqual(len(log), 2)

    def test_notebook_has_no_paid_search_calls_and_keeps_same_question(self):
        nb = json.loads((ROOT / 'labs/week_5_rag.ipynb').read_text())
        code = '\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')
        self.assertNotIn('google_search=', code)
        self.assertNotIn('answer_with_web', code)
        self.assertIn("print(web_prompt)", code)
        self.assertNotIn('RUN_LIVE', code)
        self.assertNotIn('replacement card', code)
        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                self.assertEqual(cell['outputs'], [])
                self.assertIsNone(cell['execution_count'])


if __name__ == '__main__':
    unittest.main()
