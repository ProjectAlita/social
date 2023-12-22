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
        try:
            auth_ctx = auth.get_referenced_auth_context(g.auth.reference)
            avatar = auth_ctx['provider_attr']['attributes']['picture']
        except (AttributeError, KeyError):
            avatar = None
        user['avatar'] = avatar

        social_user: User = User.query.get(user['id'])
        user['description'] = social_user.description
        user['avatar'] = social_user.avatar
        user['title'] = social_user.title

        if user.get('personal_project_id'):
            config_data = self.module.context.rpc_manager.timeout(2).prompts_get_config(
                project_id=user['personal_project_id'],
                user_id=user['id']
            )
            config_data = config_data.dict()
            user['integrations'] = config_data['integrations']
            user['api_url'] = config_data['url']

        user['tokens'] = []
        user_tokens = auth.list_tokens(user['id'])
        for t in user_tokens:
            tkn = auth.encode_token(t['id'])
            user['tokens'].append({
                'value': tkn,
                'expires': t['expires'],
                'name': t['name'],
                'id': t['id']
            })

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
