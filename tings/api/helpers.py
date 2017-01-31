from tings import db
from tings.utils import error_response, new_response, get_missing_fields
from .models import Project, Task, Label

class TaskHelper(object):
    pass

class ProjectHelper(object):

    def get_all():

        projects        = [p.to_dict() for p in Project.query.all()]
        count           = len(projects)

        data            = { "count": count, "projects": projects }
        return new_response(status_code=200, data=data)

    def get_one(project_id):
        try:
            project         = Project.query.get(project_id)
            project         = project.to_dict()
            data            = { "project": project }
            return new_response(status_code=200, data=data)
        except Exception as e:
            return error_response(status_code=404, message="Project not found")

    def create(payload):

        try:
            new_project = Project(payload)
            db.session.add(new_project)
            db.session.commit()

            json_project = new_project.to_dict()
            headers      = { "location": new_project.url }
            data         = { "project": json_project }
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
                for key, value in payload.items():
                    setattr(project, key, value)

                db.session.commit()
                project  = project.to_dict()

                data = { "message": "Update successful", "project": project }

                return new_response(status_code=200, data=data)

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
