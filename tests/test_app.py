import unittest

import app


class AppTests(unittest.TestCase):
    def test_graph_is_compiled(self):
        self.assertIsNotNone(app.graph)

    def test_manager_preserves_state(self):
        state = {"message": "test"}
        self.assertEqual(app.manager(state), state)


if __name__ == "__main__":
    unittest.main()
