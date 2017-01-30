from flask import Blueprint
from .helpers import ProjectHelper
from tings.decorators import jsonise

api = Blueprint('tings_api', __name__)

# Projects Related Endpoints

@api.route("/projects", methods=["GET"])
@jsonise
def all_projects():
    return ProjectHelper.get_all()

@api.route("/projects", methods=["POST"])
def add_project():
    # payload = request.get_payload()
    # return add_project(payload)
    pass

@api.route("/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    pass

@api.route("/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    pass

@api.route("/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    pass

@api.route("/projects/<int:project_id>/tasks", methods=["GET"])
def get_project_tasks(project_id):
    pass

@api.route("/projects/<int:project_id>/tasks/done", methods=["GET"])
def get_done_tasks(project_id):
    pass




# Task Related Endpoints
@api.route("/tasks", methods=["GET"])
def all_tasks():
    return "all tasks"

@api.route("/tasks", methods=["POST"])
def add_task():
    # new_task = request.get_paylaoad()
    # return create_task(new_task)
    pass

@api.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    # return controller.get_task(task_id)
    pass

@api.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    # return controller.update_task(task_id)
    pass

@api.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    # return controller.delete_task(task_id)
    pass

# Label Related Endpoints

@api.route("/labels", methods=["GET"])
def all_labels():
    # return controller.get_labels()
    pass

@api.route("/labels", methods=["POST"])
def add_label():
    # new_label = request.payload()
    # return create_label(new_label)
    pass

@api.route("/labels/<int:label_id>", methods=["GET"])
def get_label(label_id):
    # return controller.get_label(label_id)
    pass

@api.route("/labels/<int:label_id>", methods=["PUT"])
def update_label(label_id):
    # return controller.update_label(label_id)
    pass

@api.route("/labels/<int:label_id>", methods=["DELETE"])
def delete_label(label_id):
    # return controller.delete_label(label_id)
    pass

@api.route("/label/<int:label_id>/tasks", methods=["GET"])
def get_label_tasks(label_id):
    # return controller.delete_label_tasks(label_id)
    pass
