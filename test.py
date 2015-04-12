# coding=utf-8
import unittest
import api
import json

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = api.app.test_client()

    def test_hello_world(self):
        rv = self.app.get('/')
        assert "Hej, världen!" in rv.data

    def test_default_todos(self):
        rv = self.app.get('/api/todos/')
        todos_file = open('fixtures.json')
        expected_todos = json.load(todos_file)
        api_todos = json.loads(rv.data)['todos']
        assert expected_todos == api_todos

    def test_get_todo(self):
        rv = self.app.get('/api/todos/1')
        todos_file = open('fixtures.json')
        expected_todo = json.load(todos_file)[0]
        api_todo = json.loads(rv.data)
        assert expected_todo == api_todo

    # TODO: Stop depending on test case execution order
    def test_new_todo(self):
        data = {'title': 'Test'}
        rv = self.app.post('/api/todos/',
                           data=json.dumps(data),
                           content_type='application/json')
        api_todo = json.loads(rv.data)
        assert 'Test' == api_todo['title']

    def test_put_todo(self):
        data = {'title': 'Test2'}
        rv = self.app.put('/api/todos/3',
                           data=json.dumps(data),
                           content_type='application/json')
        api_todo = json.loads(rv.data)
        assert 'Test2' == api_todo['title']

    def test_remove_todo(self):
        rv = self.app.delete('/api/todos/3')
        assert 'OK' == rv.data

if __name__ == '__main__':
    unittest.main()