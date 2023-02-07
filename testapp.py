import unittest
import requests
from flask import Flask
from app import app, compile_index_page, owner, repo, proxy, request_processing

class TestApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(owner, response.data.decode())
        self.assertIn(repo, response.data.decode())
        self.assertIn(proxy["http"], response.data.decode())
    
    def test_receive_data(self):
        response = self.app.post("/form", data={"owner_field": "tccmyqp", "repo_field": "p_test"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("tccmyqp", response.data.decode())
        self.assertIn("p_test", response.data.decode())
        
        
    # Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()
