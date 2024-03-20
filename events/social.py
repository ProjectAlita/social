from flask import g
from pydantic import ValidationError

from tools import auth
from pylon.core.tools import web, log

from ..models.users import User
from ..models.pd.users import UserModel


class Event:

    @web.event(f"auth_visitor")
    def add_social_user_data(self, context, event, payload):
        if payload.get('type', '') == 'token':
            return

        user_id = payload.get('id', '')
        if not isinstance(user_id, int):
            return

        try:
            auth_ctx = auth.get_referenced_auth_context(payload['reference'])
            avatar = auth_ctx['provider_attr']['attributes']['picture']
        except (AttributeError, KeyError):
            avatar = None

        # TODO: need to receive user title

        try:
            user_data = UserModel(user_id=user_id, avatar=avatar)
        except ValidationError as e:
            log.exception(e)
            return

        user = User.query.filter_by(user_id=user_id).first()
        if user:
            user.avatar = avatar
            user.commit()
        else:
            user = User(**user_data.dict())
            user.insert()

        return user.to_json()
