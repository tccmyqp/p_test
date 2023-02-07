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
        response = self.app.post("/form", data={"owner_field": "new_owner", "repo_field": "new_repo"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("new_owner", response.data.decode())
        self.assertIn("new_repo", response.data.decode())
        
        
    # Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()
