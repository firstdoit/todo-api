# coding=utf-8
from flask import Flask, jsonify, abort, make_response, request
from flask.ext.cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

with open('fixtures.json') as todos_file:
    todos = json.load(todos_file)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)

@app.route('/')
def index():
    return u"Hej, världen!"

@app.route('/api/todos/', methods=['GET'])
def list_todos():
    return jsonify({'todos': todos})

@app.route('/api/todos/', methods=['POST'])
def create_todo():
    if not request.json or not 'title' in request.json:
        abort(400)

    maxId = max([t['id'] for t in todos]) if len(todos) > 0 else 0

    todo = {
        'id': maxId + 1,
        'title': request.json['title'],
        'done': False
    }
    todos.append(todo)

    return jsonify(todo), 201

@app.route('/api/todos/<int:id>', methods=['GET'])
def read_todo(id):
    todo = [t for t in todos if t['id'] == id]

    if len(todo) == 0:
        abort(404)

    return jsonify(todo[0])

@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = [t for t in todos if t['id'] == id]

    if len(todo) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) != bool:
        abort(400)
    if '$index' in request.json:
        newIndex = request.json.get('$index')

        if not(isinstance(request.json['$index'], int)):
            abort(400)
        if newIndex < 0:
            abort(400)
        if newIndex >= len(todos):
            abort(400)

        oldIndex = todos.index(todo[0])
        todos.insert(newIndex, todos.pop(oldIndex))

    todo[0]['title'] = request.json.get('title', todo[0]['title'])
    todo[0]['done'] = request.json.get('done', todo[0]['done'])

    return jsonify(todo[0])

@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = [t for t in todos if t['id'] == id]
    if len(todo) == 0:
        abort(404)
    todos.remove(todo[0])
    return "OK"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
