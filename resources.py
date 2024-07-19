from flask_restful import Resource, reqparse
from settings import db, socketio
from models import Task

task_parser = reqparse.RequestParser()
task_parser.add_argument('title', type=str, required=True, help='Title is required')
task_parser.add_argument('description', type=str)
task_parser.add_argument('completed', type=bool)

class TaskResource(Resource):
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}

    def put(self, task_id):
        args = task_parser.parse_args()
        task = Task.query.get_or_404(task_id)
        task.title = args['title']
        task.description = args['description']
        task.completed = args['completed']
        db.session.commit()
        socketio.emit('task_updated', {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed})
        return {'message': 'Task updated'}

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        socketio.emit('task_deleted', {'id': task.id})
        return {'message': 'Task deleted'}

class TaskListResource(Resource):
    def get(self):
        tasks = Task.query.all()
        return [{'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed} for task in tasks]

    def post(self):
        args = task_parser.parse_args()
        task = Task(title=args['title'], description=args['description'], completed=args['completed'])
        db.session.add(task)
        db.session.commit()
        socketio.emit('task_created', {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed})
        return {'message': 'Task created'}, 201
