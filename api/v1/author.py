from queue import Empty

from flask import request, g, jsonify
from pylon.core.tools import log
from tools import api_tools, auth, VaultClient

from ...models.users import User


class ProjectApi(api_tools.APIModeHandler):
    def get(self, **kwargs):
        user = self.module.context.rpc_manager.timeout(2).auth_main_current_user(g.auth)
        try:
            personal_project_id = self.module.context.rpc_manager.timeout(2).projects_get_personal_project_id(
                user['id'])
            user['personal_project_id'] = personal_project_id
        except Empty:
            ...

        social_user: User = User.query.filter(User.user_id == user['id']).first()
        if social_user:
            user['description'] = social_user.description
            user['avatar'] = social_user.avatar
            user['title'] = social_user.title
        else:
            try:
                auth_ctx = auth.get_referenced_auth_context(g.auth.reference)
                avatar = auth_ctx['provider_attr']['attributes']['picture']
            except (AttributeError, KeyError):
                avatar = None
            user['avatar'] = avatar

        if user.get('personal_project_id'):
            secrets = VaultClient(user['personal_project_id']).get_all_secrets()
            user['api_url'] = ''.join([
                secrets['galloper_url'],
                secrets.get('ai_project_api_url', '/api/v1')
            ])

        return jsonify(user)


class API(api_tools.APIBase):
    url_params = api_tools.with_modes([
        "",
        # "<int:user_id>",
    ])

    mode_handlers = {
        'default': ProjectApi,
    }

    def put(self, **kwargs):
        description = request.json.get('description')
        u = self.module.context.rpc_manager.timeout(2).auth_main_current_user(g.auth)
        user_id = u['id']
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            user.description = description
            user.insert()
        else:
            return {'error': 'User not found'}, 400

        return user.to_json(), 200
