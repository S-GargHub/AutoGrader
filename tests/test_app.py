import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from src.autograder import AutoGrader

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_login_with_invalid_credentials(self):
        response = self.app.post('/login', data={'email': 'invalid@example.com', 'password': 'invalid_password'})
        self.assertIn(b'Access denied:', response.data)
        self.assertIn(b'email is not from @sjsu.edu domain', response.data)

    def test_logout(self):
        response = self.app.post('/logout')
        self.assertEqual(response.status_code, 302)

    def test_access_problem_page_without_login(self):
        response = self.app.get('/problem')
        self.assertEqual(response.status_code, 302)

class TestAutoGrader(unittest.TestCase):
    def test_grade_solution(self):
        auto_grader = AutoGrader("Problem Name: Add Numbers \n Problem Description: Write a function to add two numbers.", "data/1/testCases.txt")
        student_solution = """def add(a, b): return a + b"""
        pass_count, error, test_results = auto_grader.grade_solution(student_solution)
        self.assertEqual(pass_count, 3)
        self.assertIsNone(error)

    def test_grade_solution_with_errors(self):
        auto_grader = AutoGrader("Problem Name: Add Numbers \n Problem Description: Write a function to add two numbers.", "data/1/testCases.txt")
        student_solution = """def add(a, b): return a"""
        pass_count, error, test_results = auto_grader.grade_solution(student_solution)
        self.assertEqual(pass_count, 1)
        self.assertIsNone(error)

    def test_grade_solution_with_compilation_error(self):
        auto_grader = AutoGrader("Problem Name: Add Numbers \n Problem Description: Write a function to add two numbers.", "data/1/testCases.txt")
        student_solution = """def add(a, b): return da"""
        pass_count, error, test_results = auto_grader.grade_solution(student_solution)
        self.assertEqual(pass_count, 0)
        self.assertIn('Error', error)

if __name__ == '__main__':
    unittest.main()
