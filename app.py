from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from ma import ma
from db import db


from resources.task import Task, TaskList, tasks_ns, task_ns
from marshmallow import ValidationError

app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Sample Flask-RestPlus Application')
app.register_blueprint(bluePrint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(task_ns)
api.add_namespace(tasks_ns)



@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


task_ns.add_resource(Task, '/<int:id>')
tasks_ns.add_resource(TaskList, "")


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=8001, debug=True)