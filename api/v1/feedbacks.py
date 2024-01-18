from flask import request
from tools import api_tools, config as c, auth
from pydantic import ValidationError
from ...models.pd.feedbacks import FeedbackModel

# from pylon.core.tools import log



class ProjectAPI(api_tools.APIModeHandler):
    @auth.decorators.check_api({
        "permissions": ["models.prompt_lib.feedbacks.list"],
        "recommended_roles": {
            c.ADMINISTRATION_MODE: {"admin": True, "editor": True, "viewer": False},
            c.DEFAULT_MODE: {"admin": True, "editor": True, "viewer": False},
        }})
    @api_tools.endpoint_metrics
    def get(self, project_id: int | None = None, **kwargs):
        args = dict(request.args)    
        result = self.module.list_feedbacks(args)
        return result['result'], 200


    @auth.decorators.check_api({
        "permissions": ["models.prompt_lib.feedbacks.create"],
        "recommended_roles": {
            c.ADMINISTRATION_MODE: {"admin": True, "editor": True, "viewer": False},
            c.DEFAULT_MODE: {"admin": True, "editor": True, "viewer": False},
        }})
    @api_tools.endpoint_metrics
    def post(self, project_id: int | None = None, **kwargs):
        data = request.get_json()
        author_id = auth.current_user().get("id")
        data["user_id"] = author_id        
        try:
            FeedbackModel.validate(data)
        except ValidationError as e:
            return {"ok":False, "errors": e.errors()}, 400
        
        result = self.module.feedback_create(data)
        if not result["ok"]:
            return result, 400
        
        result['result'] = result['result'].to_json()
        return result, 201
        

class API(api_tools.APIBase):
    url_params = api_tools.with_modes(
        [
            "",
            "<int:project_id>",
        ]
    )

    mode_handlers = {
        c.DEFAULT_MODE: ProjectAPI,
    }
