"""Check Week 4 data splits and evaluation without models, keys or API calls."""
import ast
import json
from pathlib import Path
import runpy
from types import SimpleNamespace
import unittest
import re
import time

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


class Week4NotebookTests(unittest.TestCase):
    def setUp(self):
        notebook = json.loads((ROOT / 'labs/week_4_classification.ipynb').read_text())
        self.cells = {cell['id']: ''.join(cell['source']) for cell in notebook['cells']}
        self.ns = {'pd': pd, 're': re, 'json': json, 'time': time,
                   'DEVICE': 'cpu', 'display': lambda *args: None}
        for cell_id in ['labels', 'training-data', 'development-data', 'regex']:
            # Load definitions and data without executing display/demo statements.
            tree = ast.parse(self.cells[cell_id])
            tree.body = [node for node in tree.body
                         if isinstance(node, (ast.Assign, ast.FunctionDef))]
            exec(compile(tree, cell_id, 'exec'), self.ns)
        for cell_id in ['llm-function', 'evaluation-functions']:
            tree = ast.parse(self.cells[cell_id])
            tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
            exec(compile(tree, cell_id, 'exec'), self.ns)

    def test_original_training_and_separate_five_label_splits(self):
        test_data = runpy.run_path(str(ROOT / 'data/eval_data_week4.py'))['eval_data']
        datasets = [self.ns['train_data'], self.ns['dev_data'], test_data]
        self.assertEqual([len(data) for data in datasets], [50, 10, 20])
        key = self.ns['text_key']
        keys = []
        for data in datasets:
            self.assertEqual({row['label'] for row in data}, set(self.ns['labels']))
            texts = {key(row['text']) for row in data}
            self.assertEqual(len(texts), len(data))
            keys.append(texts)
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                self.assertFalse(keys[i] & keys[j])

    def test_regex_revision_preserves_original_and_adds_missing_spelling(self):
        classify = self.ns['classify_regex']
        original = self.ns['patterns']
        revised = {**original, 'check_email': r'messagerie|e-?mail'}
        self.assertIsNone(classify('Consulter mes e-mails'))
        self.assertEqual(classify('Consulter mes e-mails', revised), 'check_email')
        self.assertIsNone(classify('Consulter mes e-mails', original))
        for text in ['Ouvrir ma messagerie', 'Consulter mes emails']:
            self.assertEqual(classify(text, revised), 'check_email')
        self.assertEqual(classify("m'inscrire à un cours", revised), 'register_classes')

    def install_api_reply(self, text):
        usage = SimpleNamespace(prompt_token_count=10, candidates_token_count=5,
                                total_token_count=16)
        response = SimpleNamespace(text=text, usage_metadata=usage)
        self.ns.update(
            client=SimpleNamespace(models=SimpleNamespace(generate_content=lambda **kwargs: response)),
            model_name='test-model', llm_config=None,
        )

    def test_valid_reply_and_actual_usage(self):
        self.install_api_reply('{"label": "check_email"}')
        result = self.ns['classify_llm']('Ouvrir ma messagerie')
        self.assertEqual(result['prediction'], 'check_email')
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['total_tokens'], 16)

    def test_invalid_replies_preserve_usage(self):
        for text in ['not JSON', '{"label": "unknown"}', '["check_email"]',
                     '{"label": []}', '{"label": "check_email", "extra": 1}']:
            with self.subTest(text=text):
                self.install_api_reply(text)
                result = self.ns['classify_llm']('Ouvrir ma messagerie')
                self.assertEqual(result['status'], 'invalid_reply')
                self.assertIsNone(result['prediction'])
                self.assertEqual(result['input_tokens'], 10)

    def test_failures_remain_in_denominator_and_usage_stays_missing(self):
        cases = [{'text': str(i), 'label': 'check_email'} for i in range(5)]

        def classifier(text):
            if text == '0':
                return {'prediction': 'check_email', 'input_tokens': 10}
            if text == '1':
                return {'prediction': 'get_schedule'}
            if text == '2':
                return {'prediction': None}
            if text == '3':
                return {'prediction': None, 'status': 'invalid_reply', 'input_tokens': 7}
            raise TimeoutError('Simulated API timeout')

        result = self.ns['evaluate'](cases, {'test': classifier})
        summary = self.ns['summarize'](result).loc['test']
        self.assertEqual(len(result), 5)
        self.assertEqual(summary['correct'], 1)
        self.assertEqual(summary['accuracy'], 0.2)
        self.assertEqual(summary['no_label_or_failed'], 3)
        self.assertEqual(result.iloc[-1]['status'], 'error')
        self.assertIn('TimeoutError', result.iloc[-1]['error'])
        self.assertTrue(pd.isna(result.iloc[-1]['input_tokens']))
        self.assertEqual(result['input_tokens'].sum(min_count=1), 17)

    def test_regex_only_evaluation_has_no_api_usage(self):
        result = self.ns['evaluate'](self.ns['dev_data'], {
            'Regex': lambda text: {'prediction': self.ns['classify_regex'](text)},
        })
        self.assertTrue(result['total_tokens'].isna().all())
        self.assertTrue(pd.isna(self.ns['summarize'](result).iloc[0]['mean_input_tokens']))


if __name__ == '__main__':
    unittest.main()
