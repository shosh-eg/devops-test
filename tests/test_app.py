import unittest
from app import app, add_task
import sqlite3

class TestApp(unittest.TestCase):
    def test_app_startup(self):
        with app.test_client() as client:
            self.assertEqual(client.get('/').status_code, 200)

    def test_add_task(self):
        add_task("Test Task")
        conn = sqlite3.connect('db.sqlite')
        c = conn.cursor()
        c.execute("SELECT task_name FROM tasks WHERE task_name = 'Test Task'")
        self.assertIsNotNone(c.fetchone())
        conn.close()

    def test_sqlite_connection(self):
        conn = sqlite3.connect('db.sqlite')
        c = conn.cursor()
        c.execute("SELECT 1")
        self.assertEqual(c.fetchone()[0], 1)
        conn.close()

    def test_get_tasks(self):
        with app.test_client() as client:
            response = client.get('/tasks')
            self.assertTrue(len(response.json['tasks']) > 0)

if __name__ == '__main__':
    unittest.main()
