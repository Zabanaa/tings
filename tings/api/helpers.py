from tings import db
from tings.utils import error_response, new_response, get_missing_fields
from .models import Project, Task, Label

class TaskHelper(object):

    def get_all():
        tasks           = [t.to_dict() for t in Task.query.all()]
        count           = len(tasks)

        data            = { "count": count, "tasks": tasks }
        return new_response(status_code=200, data=data)

    def create(payload):

        try:
            new_task     = Task(payload).save()
            json_task    = new_task.to_dict()

            headers      = { "location": new_task.url }
            data         = {
                "task": json_task,
                "message": "Task successfully added."
            }

            return new_response(status_code=201, data=data, headers=headers)

        except Exception as e:
            cause_of_error = str(e.__dict__['orig'])
            if "not-null" in cause_of_error:
                missing_fields = get_missing_fields(e.__dict__['params'])
                return error_response(
                        status_code=422,
                        message="Missing required fields.",
                        missing_fields=missing_fields
                )
            else:
                message = "Something went wrong, please ask a developer for assistance"
                return error_response(status_code=500, message=message)


    def get_one(task_id):

        task = Task.query.get(task_id)

        if task is None:
            message = "Task not found"
            return error_response(status_code=404, message=message)

        task = task.to_dict()
        data = {"task": task }
        return new_response(status_code=200, data=data)

    def update(task_id, payload):

        task = Task.query.get(task_id)

        if task is None:
            message = "Task not found"
            return error_response(status_code=404, message=message)
        else:
            try:
                task.update(payload)
                json_task   = task.to_dict()
                data        = {"task": json_task}
                return new_response(status_code=200, data=data)
            except:
                message = "Something went wrong, please ask a developer for assistance"
                return error_response(status_code=500, message=message)

    def delete(task_id):

        task = Task.query.get(task_id)

        if task is None:
            message = "Task not found"
            return error_response(status_code=404, message=message)

        task.delete()
        return new_response(status_code=204)

## Project
## Helper

class ProjectHelper(object):

    def get_all():

        projects        = [p.to_dict() for p in Project.query.all()]
        count           = len(projects)

        data            = { "count": count, "projects": projects }
        return new_response(status_code=200, data=data)

    def get_one(project_id):

        project         = Project.query.get(project_id)

        if project is None:
            message = "Project not found"
            return error_response(status_code=404, message=message)

        project         = project.to_dict()
        data            = { "project": project }
        return new_response(status_code=200, data=data)

    def create(payload):

        try:
            new_project = Project(payload)
            new_project.save()
            json_project = new_project.to_dict()

            headers      = { "location": new_project.url }

            data         = {
                "project": json_project,
                "message": "Project successfully created."
            }

            return new_response(status_code=201, data=data, headers=headers)

        except Exception as e:
            cause_of_error = str(e.__dict__['orig'])
            if "violates unique constraint" in cause_of_error:
                message = "A project with that name already exists."
                return error_response(status_code=409, message=message)

            elif "not-null" in cause_of_error:
                missing_fields = get_missing_fields(e.__dict__['params'])
                return error_response(
                        status_code=422,
                        message="Missing required fields.",
                        missing_fields=missing_fields
                )
            else:
                message = "Something went wrong, please ask a developer for assistance"
                return error_response(status_code=500, message=message)

    def update(payload, project_id):

        project = Project.query.get(project_id)

        if project is None:

            message = "Project not found"
            return error_response(status_code=404, message=message)

        else:

            try:
                project.update(payload)
                project  = project.to_dict()
                data = { "message": "Update successful", "project": project }
                return new_response(status_code=200, data=data)

            except Exception as e:
                cause_of_error = str(e.__dict__['orig'])
                if "violates unique constraint" in cause_of_error:
                    message = "A project with that name already exists."
                    return error_response(status_code=409, message=message)
                else:
                    message = "Something went wrong, please ask a developer for assistance"
                    return error_response(status_code=500, message=message)

    def delete(project_id):

        project = Project.query.get(project_id)

        if project is None:
            message = "Project not found"
            return error_response(status_code=404, message=message)

        project.delete()
        return new_response(status_code=204)
