from flask import Blueprint, request
from tings.api.models import Project, Task, Label
from tings.decorators import jsonise

api = Blueprint('tings_api', __name__)

# Projects Related Endpoints

@api.route("/projects", methods=["GET"], endpoint="all_projects")
@jsonise
def all_projects():
    return Project.get_all()

@api.route("/projects", methods=["POST"], endpoint="create_project")
@jsonise
def create_project():
    payload = request.get_json()
    return Project.create(payload)

@api.route("/projects/<int:id>", methods=["GET"], endpoint="get_project")
@jsonise
def get_project(id):
    return Project.get_one(id)

@api.route("/projects/<int:id>", methods=["PUT"], endpoint="update_project")
@jsonise
def update_project(id):
    payload = request.get_json()
    return Project.update(payload, id)

@api.route("/projects/<int:id>", methods=["DELETE"], endpoint="delete_project")
@jsonise
def delete_project(id):
    return Project.delete(id)

@api.route("/projects/<int:id>/tasks", methods=["GET"], endpoint="get_project_tasks")
@jsonise
def get_project_tasks(id):
    return Project.get_tasks(project_id=id)

@api.route("/projects/<int:id>/tasks/done", methods=["GET"], endpoint="done_tasks")
@jsonise
def get_done_tasks(id):
    return Project.get_tasks(project_id=id, done=True)

@api.route("/projects/<int:id>/labels", methods=["GET"], endpoint="get_project_labels")
@jsonise
def get_project_labels(id):
    return Project.get_labels(id)

# Task Related Endpoints
@api.route("/tasks", methods=["GET"], endpoint="all_tasks")
@jsonise
def all_tasks():
    return Task.get_all()

@api.route("/tasks", methods=["POST"], endpoint="create_task")
@jsonise
def add_task():
    new_task = request.get_json()
    return Task.create(new_task)

@api.route("/tasks/<int:id>", methods=["GET"], endpoint="get_task")
@jsonise
def get_task(id):
    return Task.get_one(id)

@api.route("/tasks/<int:id>", methods=["PUT"], endpoint="update_task")
@jsonise
def update_task(id):
    payload = request.get_json()
    return Task.update(payload, id)

@api.route("/tasks/<int:id>", methods=["DELETE"], endpoint="delete_task")
@jsonise
def delete_task(id):
    return Task.delete(id)

# Label Related Endpoints

@api.route("/labels", methods=["GET"], endpoint="all_labels")
@jsonise
def all_labels():
    return Label.get_all()

@api.route("/labels", methods=["POST"], endpoint="create_label")
@jsonise
def add_label():
    payload = request.get_json()
    return Label.create(payload)

@api.route("/labels/<int:id>", methods=["GET"], endpoint="get_label")
@jsonise
def get_label(id):
    return Label.get_one(id)

@api.route("/labels/<int:id>", methods=["PUT"], endpoint="update_label")
@jsonise
def update_label(id):
    payload = request.get_json()
    return Label.update(payload, id)

@api.route("/labels/<int:id>", methods=["DELETE"], endpoint="delete_label")
@jsonise
def delete_label(id):
    return Label.delete(id)

@api.route("/labels/<int:id>/tasks", methods=["GET"], endpoint="get_label_tasks")
@jsonise
def get_label_tasks(id):
    return Label.get_tasks(project_id=id)
