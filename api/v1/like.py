from queue import Empty

from sqlalchemy.exc import IntegrityError
from tools import api_tools, auth

from ...constants import PROMPT_LIB_MODE


class PromptLibAPI(api_tools.APIModeHandler):
    @api_tools.endpoint_metrics
    def post(self, project_id, entity, entity_id):
        try:
            result = self.module.context.rpc_manager.timeout(2).social_like(
                project_id=project_id, entity=entity, entity_id=entity_id
            )
        except Empty:
            return {"ok": False, "error": "No response"}, 500
        except IntegrityError:
            return {"ok": False, "error": "Already liked"}, 400
        return result, 201

    @api_tools.endpoint_metrics
    def delete(self, project_id, entity, entity_id):
        try:
            result = self.module.context.rpc_manager.timeout(2).social_dislike(
                project_id=project_id, entity=entity, entity_id=entity_id
            )
        except Empty:
            return {"ok": False, "error": "No response"}, 500
        return result, 204


class API(api_tools.APIBase):
    url_params = api_tools.with_modes(
        [
            "<int:project_id>/<string:entity>/<int:entity_id>",
        ]
    )

    mode_handlers = {
        PROMPT_LIB_MODE: PromptLibAPI,
    }
