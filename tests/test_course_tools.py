import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'labs'))
from course_tools import run_agent, summarize_measurements


class AgentTests(unittest.TestCase):
    def test_tool_result_drives_next_action(self):
        def choose(state):
            if not state['observations']:
                return {'tool': 'add', 'args': {'a': 2, 'b': 3}}
            return {'final': state['observations'][-1]['result']}
        run = run_agent('Sum', choose, {'add': lambda a, b: a + b}, lambda value, state: value == 5)
        self.assertEqual((run['status'], run['final'], len(run['trace'])), ('verified', 5, 2))

    def test_invalid_actions_consume_budget(self):
        for action in ['not json', [], {'tool': 'shell', 'args': {}},
                       {'tool': 'add', 'args': {'unexpected': 1}},
                       {'tool': 'add', 'args': []}]:
            with self.subTest(action=action):
                calls = []
                run = run_agent('x', lambda state: action,
                                {'add': lambda a, b: calls.append((a, b))},
                                lambda value, state: True, max_steps=2)
                self.assertEqual(run['status'], 'step_limit')
                self.assertEqual(len(run['trace']), 2)
                self.assertEqual(calls, [])
                self.assertTrue(all('error' in row['observation'] for row in run['trace']))

    def test_unverified_final_is_not_completion(self):
        run = run_agent('x', lambda state: {'final': 'unsupported'}, {},
                        lambda value, state: False, max_steps=3)
        self.assertEqual(run['status'], 'step_limit')
        self.assertIsNone(run['final'])

    def test_tool_failure_is_visible_and_recoverable(self):
        def broken():
            raise RuntimeError('missing data')
        def choose(state):
            return {'final': 'needs data'} if state['observations'] else {'tool': 'read', 'args': {}}
        run = run_agent('x', choose, {'read': broken}, lambda value, state: value == 'needs data')
        self.assertIn('missing data', run['trace'][0]['observation']['error'])
        self.assertEqual(run['status'], 'verified')

    def test_policy_cannot_mutate_internal_observations(self):
        def choose(state):
            state['observations'].append({'forged': True})
            return {'final': 1}
        run = run_agent('x', choose, {}, lambda value, state: not state['observations'])
        self.assertEqual(run['status'], 'verified')


class EvaluationTests(unittest.TestCase):
    def test_missing_measurements_are_not_zero(self):
        result = summarize_measurements([{'group': 'a', 'value': '10'}, {'group': 'a', 'value': ''}])
        self.assertEqual(result['a'], {'rows': 2, 'observed': 1, 'missing': 1, 'mean': 10.0})


if __name__ == '__main__':
    unittest.main()
