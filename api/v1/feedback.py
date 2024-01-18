import traceback
from flask import request
from pydantic import ValidationError
from pylon.core.tools import log
from ...models.pd.feedbacks import FeedbackUpdateModel

from tools import api_tools, config as c, auth


class ProjectApi(api_tools.APIModeHandler):
    @auth.decorators.check_api({
        "permissions": ["models.prompt_lib.feedback.details"],
        "recommended_roles": {
            c.ADMINISTRATION_MODE: {"admin": True, "editor": True, "viewer": False},
            c.DEFAULT_MODE: {"admin": True, "editor": True, "viewer": False},
        }})
    def get(self, project_id: int, feedback_id: int):
        result = self.module.get_feedback(feedback_id)
        if not result['ok']:
            return result, 404
        result['result'] = result['result'].to_json()
        return result, 200

    @auth.decorators.check_api({
        "permissions": ["models.prompt_lib.feedback.delete"],
        "recommended_roles": {
            c.ADMINISTRATION_MODE: {"admin": True, "editor": True, "viewer": False},
            c.DEFAULT_MODE: {"admin": True, "editor": True, "viewer": False},
        }})
    def delete(self, project_id, feedback_id):
        result = self.module.delete_feedback(feedback_id)
        return "", 204 if result['ok'] else 404

    @auth.decorators.check_api({
        "permissions": ["models.prompt_lib.feedback.update"],
        "recommended_roles": {
            c.ADMINISTRATION_MODE: {"admin": True, "editor": True, "viewer": False},
            c.DEFAULT_MODE: {"admin": True, "editor": True, "viewer": False},
        }})
    def put(self, project_id, feedback_id):
        try:
            payload = request.get_json()
            FeedbackUpdateModel.validate(payload)
            result = self.module.update_feedback(feedback_id, payload)
            if not result['ok']:
                return result, 404
            result['result'] = result['result'].to_json()
            return result, 200
        except ValidationError as e:
            return {"ok":False, "errors": e.errors()}, 400
        except Exception as e:
            log.info(traceback.format_exc())
            return {"error": str(e)}, 400



class API(api_tools.APIBase):
    url_params = api_tools.with_modes(
        [
            "<int:project_id>",
            "<int:project_id>/<int:feedback_id>",
        ]
    )

    mode_handlers = {c.DEFAULT_MODE: ProjectApi}
