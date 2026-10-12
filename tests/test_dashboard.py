import unittest

from dashboard_api import app


class DashboardApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_status_reports_local_workflow(self):
        response = self.client.get("/api/status")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["status"], "ok")
        self.assertIn("LangGraph", payload["workflow"])

    def test_run_invokes_demo_graph(self):
        response = self.client.post("/api/run")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["status"], "ok")
        self.assertIn("Workflow completed", payload["message"])


if __name__ == "__main__":
    unittest.main()
