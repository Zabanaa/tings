from tings import db
from .models import Project, Task, Label
from collections import namedtuple

Response = namedtuple('Response', 'status body headers')

class ProjectHelper(object):

    def get_all():

        projects        = [p.to_json() for p in Project.query.all()]
        count           = len(projects)
        meta            = { "type": "success", "status": 200 }
        data            = { "count": count, "projects": projects }

        body            = { "meta": meta, "data": data }
        response         = Response(status=200, body=body, headers=None)

        return response

    def create(payload):

        try:
            new_project = Project(payload)
            db.session.add(new_project)
            db.session.commit()

            json_project = new_project.to_json()
            headers      = { "location": new_project.url }
            meta         = { "type": "success", "status": 201 }
            data         = { "project": json_project }
            body         = { "meta": meta, "data": data }
            response     = Response(status=201, body=body, headers=headers)
            return response
        except Exception as e:
            # return 409, 422, whatevs
            print(e)
            response = Response(status=223, body="kjewe", headers=None)
            return response
