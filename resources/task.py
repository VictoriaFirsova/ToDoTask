from flask import request
from flask_restplus import Resource, fields, Namespace

from models.task import TaskModel
from schemas.task import TaskSchema

task_NOT_FOUND = "task not found."


task_ns = Namespace('task', description='task related operations')
tasks_ns = Namespace('tasks', description='tasks related operations')

task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)

#Model required by flask_restplus for expect
task = tasks_ns.model('task', {
    'title': fields.String('Name of the task'),
    'content': fields.String('Contet of the task'),

})


class Task(Resource):

    def get(self, id):
        task_data = TaskModel.find_by_id(id)
        if task_data:
            return task_schema.dump(task_data)
        return {'message': task_NOT_FOUND}, 404

    def delete(self,id):
        task_data = TaskModel.find_by_id(id)
        if task_data:
            task_data.delete_from_db()
            return {'message': "task Deleted successfully"}, 200
        return {'message': task_NOT_FOUND}, 404

    @task_ns.expect(task)
    def put(self, id):
        task_data = TaskModel.find_by_id(id)
        task_json = request.get_json()

        if task_data:
            task_data.content = task_json['content']
            task_data.title = task_json['title']
        else:
            task_data = task_schema.load(task_json)

        task_data.save_to_db()
        return task_schema.dump(task_data), 200


class TaskList(Resource):
    @tasks_ns.doc('Get all the tasks')
    def get(self):
        return task_list_schema.dump(TaskModel.find_all()), 200

    @tasks_ns.expect(task)
    @tasks_ns.doc('Create an task')
    def post(self):
        task_json = request.get_json()
        task_data = task_schema.load(task_json)
        task_data.save_to_db()

        return task_schema.dump(task_data), 201