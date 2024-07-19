from settings import api, db, socketio, app
from resources import TaskResource, TaskListResource

api.add_resource(TaskListResource, '/tasks')
api.add_resource(TaskResource, '/tasks/<int:task_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        socketio.run(app, debug=True)