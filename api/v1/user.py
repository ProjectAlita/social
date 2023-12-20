from flask import request
from pylon.core.tools import log
from tools import api_tools

from ...models.users import User


class ProjectApi(api_tools.APIModeHandler):
    def put(self, user_id: int):
        description = request.json.get('description')
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            user.description = description
            user.insert()
        else:
            return 'User not found', 404

        return user.to_json(), 201


class API(api_tools.APIBase):
    url_params = api_tools.with_modes(
        [
            "<int:user_id>",
        ]
    )

    mode_handlers = {
        'default': ProjectApi,
    }
