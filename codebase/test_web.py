import unittest

from fastapi.testclient import TestClient

from web import app


class DemoWebTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.addCleanup(self.client.close)

    def test_healthcheck(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_demo_uses_the_fake_agent(self):
        response = self.client.post("/ask", json={"text": "Thử TeaParty"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"output": "[câu trả lời giả — chưa nối model] Thử TeaParty"})

    def test_blank_input_is_rejected(self):
        response = self.client.post("/ask", json={"text": "   "})
        self.assertEqual(response.status_code, 422)
