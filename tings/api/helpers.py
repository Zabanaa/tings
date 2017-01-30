from .models import Project, Task, Label
from collections import namedtuple

Response = namedtuple('Response', 'status body headers')

class ProjectHelper(object):

    def get_all():
        projects        = [p.to_json() for p in Project.query.all()]
        count           = len(projects)
        body            = {

            "meta": {
                "type": "success",
                "status": 200
            },

            "data": {
                "count": count,
                "projects": projects
            }

        }

        response         = Response(status=200, body=body, headers=None)
        return response
