from flask import Blueprint, request
from .helpers import ProjectHelper, TaskHelper
from tings.decorators import jsonise

api = Blueprint('tings_api', __name__)

# Projects Related Endpoints

@api.route("/projects", methods=["GET"], endpoint="all_projects")
@jsonise
def all_projects():
    return ProjectHelper.get_all()

@api.route("/projects", methods=["POST"], endpoint="create_project")
@jsonise
def create_project():
    payload = request.get_json()
    return ProjectHelper.create(payload)

@api.route("/projects/<int:project_id>", methods=["GET"], endpoint="get_project")
@jsonise
def get_project(project_id):
    return ProjectHelper.get_one(project_id)

@api.route("/projects/<int:project_id>", methods=["PUT"], endpoint="update_project")
@jsonise
def update_project(project_id):
    payload = request.get_json()
    return ProjectHelper.update(payload, project_id)

@api.route("/projects/<int:project_id>", methods=["DELETE"], endpoint="delete_project")
@jsonise
def delete_project(project_id):
    return ProjectHelper.delete(project_id)

@api.route("/projects/<int:project_id>/tasks", methods=["GET"], endpoint="project_tasks")
def get_project_tasks(project_id):
    pass

@api.route("/projects/<int:project_id>/tasks/done", methods=["GET"], endpoint="done_tasks")
def get_done_tasks(project_id):
    pass

# Task Related Endpoints
@api.route("/tasks", methods=["GET"], endpoint="all_tasks")
@jsonise
def all_tasks():
    return TaskHelper.get_all()

@api.route("/tasks", methods=["POST"], endpoint="create_task")
@jsonise
def add_task():
    new_task = request.get_json()
    return TaskHelper.create(new_task)

@api.route("/tasks/<int:task_id>", methods=["GET"], endpoint="get_task")
@jsonise
def get_task(task_id):
    return TaskHelper.get_one(task_id)

@api.route("/tasks/<int:task_id>", methods=["PUT"], endpoint="update_task")
@jsonise
def update_task(task_id):
    payload = request.get_json()
    return TaskHelper.update(task_id, payload)

@api.route("/tasks/<int:task_id>", methods=["DELETE"], endpoint="delete_task")
def delete_task(task_id):
    # return controller.delete_task(task_id)
    pass

# Label Related Endpoints

@api.route("/labels", methods=["GET"], endpoint="all_labels")
def all_labels():
    # return controller.get_labels()
    pass

@api.route("/labels", methods=["POST"], endpoint="create_label")
def add_label():
    # new_label = request.payload()
    # return create_label(new_label)
    pass

@api.route("/labels/<int:label_id>", methods=["GET"], endpoint="get_label")
def get_label(label_id):
    # return controller.get_label(label_id)
    pass

@api.route("/labels/<int:label_id>", methods=["PUT"], endpoint="update_label")
def update_label(label_id):
    # return controller.update_label(label_id)
    pass

@api.route("/labels/<int:label_id>", methods=["DELETE"], endpoint="delete_label")
def delete_label(label_id):
    # return controller.delete_label(label_id)
    pass

@api.route("/label/<int:label_id>/tasks", methods=["GET"], endpoint="label_tasks")
def get_label_tasks(label_id):
    # return controller.delete_label_tasks(label_id)
    pass
