"""Exercise the notebook's actual loop definitions with offline test fixtures."""
import ast
import importlib.util
import json
from pathlib import Path
import time
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'workflow', ROOT / 'slides/examples/week5_retrieval/workflow.py')
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


def notebook_functions():
    notebook = json.loads((ROOT / 'labs/week_5_rag.ipynb').read_text())
    functions = []
    for cell in notebook['cells']:
        source = ''.join(cell['source'])
        if cell['cell_type'] != 'code' or source.startswith('%'):
            continue
        functions.extend(node for node in ast.parse(source).body
                         if isinstance(node, ast.FunctionDef)
                         and node.name in ('answer_with_loop', 'review_for_loop'))
    namespace = {'time': time, 'json': json, 'check_review': workflow.check_review}
    exec(compile(ast.Module(body=functions, type_ignores=[]), 'week5 notebook', 'exec'), namespace)
    return namespace


class ExtendedLoopTests(unittest.TestCase):
    def setUp(self):
        self.ns = notebook_functions()
        self.initial = [{'chunk_id': 'D1', 'text': 'Initial test evidence'}]
        self.extra = {'chunk_id': 'D2', 'text': 'Additional test evidence'}
        self.writer = Mock(side_effect=lambda *args: 'TEST draft')
        self.reviewer = Mock()
        self.retrieve = Mock(return_value=self.initial)
        self.ns.update(write_answer=self.writer, review_for_loop=self.reviewer,
                       retrieve=self.retrieve)
        self.question = 'Where do I collect my card?'

    def run_loop(self, reviews, replies=()):
        self.reviewer.side_effect = reviews
        ask = Mock(side_effect=replies)
        return self.ns['answer_with_loop'](self.question, ask_student=ask), ask

    def test_missing_fact_changes_query_and_adds_evidence_without_losing_original(self):
        self.retrieve.side_effect = [self.initial, self.initial + [self.extra]]
        result, ask = self.run_loop([
            {'status': 'missing_information', 'feedback': 'Lieu de retrait de la carte'},
            {'status': 'accepted', 'feedback': 'TEST evidence supports answer'},
        ])
        self.assertEqual(result['status'], 'accepted')
        self.assertEqual(result['passages'], self.initial + [self.extra])
        query = self.retrieve.call_args_list[1].args[0]
        self.assertIn(self.question, query)
        self.assertIn('Lieu de retrait de la carte', query)
        self.assertEqual(self.retrieve.call_args_list[1].kwargs, {'k': 8})
        self.assertEqual(result['trace'][0]['added_passage_ids'], ['D2'])
        self.assertEqual(self.writer.call_args_list[1].args[1], self.initial + [self.extra])
        ask.assert_not_called()

    def test_search_returning_only_seen_passages_stops_unresolved(self):
        result, ask = self.run_loop([
            {'status': 'missing_information', 'feedback': 'Replacement fee'},
        ])
        self.assertEqual(result['status'], 'no_new_evidence')
        self.assertEqual(len(result['trace']), 1)
        self.assertEqual(self.writer.call_count, 1)
        self.assertEqual(result['trace'][0]['added_passage_ids'], [])
        ask.assert_not_called()

    def test_clarifications_preserve_original_and_real_conversation_and_reset_draft(self):
        result, ask = self.run_loop([
            {'status': 'needs_clarification', 'feedback': 'Quelle composante ?'},
            {'status': 'needs_clarification', 'feedback': 'Quel campus ?'},
            {'status': 'accepted', 'feedback': 'TEST answer supported'},
        ], replies=['IUT', 'Aix'])
        self.assertEqual(result['status'], 'accepted')
        self.assertEqual(ask.call_count, 2)
        self.assertEqual(result['original_question'], self.question)
        for text in [self.question, 'Quelle composante ?', 'Student: IUT',
                     'Quel campus ?', 'Student: Aix']:
            self.assertIn(text, result['question'])
        self.assertEqual(result['clarifications'][0]['reply'], 'IUT')
        self.assertEqual(self.retrieve.call_count, 3)
        for call in self.writer.call_args_list[1:]:
            self.assertEqual(call.args[2:], ('', ''))
        self.assertGreaterEqual(result['student_wait_seconds'], 0)

    def test_empty_student_reply_pauses_without_a_final_answer(self):
        result, ask = self.run_loop([
            {'status': 'needs_clarification', 'feedback': 'Quelle composante ?'},
        ], replies=['   '])
        self.assertEqual(result['status'], 'needs_clarification')
        self.assertIsNone(result['answer'])
        self.assertEqual(result['clarification_question'], 'Quelle composante ?')
        self.assertEqual(result['question'], self.question)
        self.assertEqual(self.retrieve.call_count, 1)
        self.assertEqual(self.writer.call_count, 1)
        self.assertEqual(ask.call_count, 1)

    def test_revisions_keep_passages_and_send_feedback_to_writer(self):
        result, _ = self.run_loop([
            {'status': 'revise', 'feedback': 'Correct the citation'},
            {'status': 'accepted', 'feedback': 'TEST supported'},
        ])
        self.assertEqual(result['status'], 'accepted')
        self.assertEqual(self.retrieve.call_count, 1)
        self.assertEqual(self.writer.call_args_list[1].args,
                         (self.question, self.initial, 'TEST draft', 'Correct the citation'))

    def test_clarification_does_not_reset_attempt_budget_or_ask_after_last_attempt(self):
        result, ask = self.run_loop([
            {'status': 'needs_clarification', 'feedback': 'TEST clarification'}
            for _ in range(4)
        ], replies=['First reply', 'Second reply', 'Third reply'])
        self.assertEqual(result['status'], 'attempt_limit')
        self.assertEqual(len(result['trace']), 4)
        self.assertEqual(self.writer.call_count + self.reviewer.call_count, 8)
        self.assertEqual(ask.call_count, 3)
        self.assertEqual(self.retrieve.call_count, 4)

    def test_no_new_search_is_started_after_final_review(self):
        result, _ = self.run_loop([
            {'status': 'revise', 'feedback': 'TEST correction'} for _ in range(3)
        ] + [{'status': 'missing_information', 'feedback': 'TEST missing fact'}])
        self.assertEqual(result['status'], 'attempt_limit')
        self.assertEqual(self.retrieve.call_count, 1)
        self.assertEqual(self.writer.call_count + self.reviewer.call_count, 8)

    def test_extended_review_is_validated_and_simple_loop_keeps_its_contract(self):
        extended = {'status': 'needs_clarification', 'feedback': 'Which campus?'}
        workflow.check_review(extended, allow_clarification=True)
        with self.assertRaises(ValueError):
            workflow.check_review(extended)
        ns = notebook_functions()
        ns.update(loop_review_config=object(), build_context=lambda passages: 'TEST evidence',
                  call_model=Mock(return_value=Mock(text=json.dumps(
                      {'status': 'invented_status', 'feedback': 'TEST invalid'}))))
        with self.assertRaises(ValueError):
            ns['review_for_loop'](self.question, self.initial, 'TEST answer')


if __name__ == '__main__':
    unittest.main()
