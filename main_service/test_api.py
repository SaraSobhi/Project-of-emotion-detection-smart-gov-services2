import requests
import unittest
import time
import subprocess
import sys
import os

BASE_URL = "http://localhost:5000/api"

class TestBackendService(unittest.TestCase):
    
    def test_01_anonymous_registration(self):
        print("\nTesting Anonymous Registration...")
        response = requests.post(f"{BASE_URL}/users/register", json={"role": "anonymous"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['role'], 'anonymous')
        self.assertTrue('user_id' in data)
        self.global_user_id = data['user_id']
        print(f"Anonymous User ID: {self.global_user_id}")
        return self.global_user_id

    def test_02_admin_registration(self):
        print("\nTesting Admin Registration...")
        payload = {"role": "admin", "username": "admin1", "password": "password123"}
        response = requests.post(f"{BASE_URL}/users/register", json=payload)
        # It might fail if run multiple times without restart, so we accept 201 or 400 (already exists)
        if response.status_code == 400 and "already exists" in response.text:
             print("Admin already exists.")
        else:
            self.assertEqual(response.status_code, 201)
            print("Admin created.")

    def test_03_admin_login(self):
        print("\nTesting Admin Login...")
        payload = {"username": "admin1", "password": "password123"}
        response = requests.post(f"{BASE_URL}/users/login", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Login successful")
        print("Login successful.")

    def test_04_feedback_crud(self):
        print("\nTesting Feedback CRUD...")
        
        # Create anonymous user for the feedback
        r_user = requests.post(f"{BASE_URL}/users/register", json={"role": "anonymous"})
        user_id = r_user.json()['user_id']

        # 1. Create
        payload = {"feedback": "This is a test feedback.", "user_id": user_id}
        r_create = requests.post(f"{BASE_URL}/feedbacks", json=payload)
        self.assertEqual(r_create.status_code, 201)
        data = r_create.json()
        feedback_id = data['id']
        print(f"Created Feedback ID: {feedback_id}")
        
        # Verify new fields
        self.assertTrue('created_at' in data)
        # We check for one of the new fields to confirm structure
        # Note: If ML service is not running or fails, these might be None, but keys should exist (or we check if creating feedback success)
        # Actually in the code we insert None if call fails.
        # But let's check keys are in response (RealDictCursor returns them even if None usually if selected *)
        self.assertTrue('sentiment' in data)
        self.assertTrue('confidence' in data)
        print(f"Sentiment: {data.get('sentiment')}")

        # 2. Read All
        r_all = requests.get(f"{BASE_URL}/feedbacks")
        self.assertEqual(r_all.status_code, 200)
        self.assertTrue(len(r_all.json()) > 0)

        # 3. Read One
        r_one = requests.get(f"{BASE_URL}/feedbacks/{feedback_id}")
        self.assertEqual(r_one.status_code, 200)
        self.assertEqual(r_one.json()['feedback'], "This is a test feedback.")

        # 4. Update
        r_update = requests.put(f"{BASE_URL}/feedbacks/{feedback_id}", json={"feedback": "Updated Feedback"})
        self.assertEqual(r_update.status_code, 200)
        self.assertEqual(r_update.json()['feedback'], "Updated Feedback")

        # 5. Delete
        r_delete = requests.delete(f"{BASE_URL}/feedbacks/{feedback_id}")
        self.assertEqual(r_delete.status_code, 200)
        
        # Verify Delete
        r_check = requests.get(f"{BASE_URL}/feedbacks/{feedback_id}")
        self.assertEqual(r_check.status_code, 404)
        print("Feedback CRUD passed.")

if __name__ == '__main__':
    # Ensure server is running or wait a bit if we just started it
    try:
        requests.get("http://localhost:5000/api/users/register") # Just checking connectivity
    except requests.exceptions.ConnectionError:
        print("Server not running due to connection error. Please make sure app.py is running.")
        # sys.exit(1) # Don't exit here so we can see the output if user runs it manually
        
    unittest.main()
