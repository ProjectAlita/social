from pylon.core.tools import web, log

from ..models.users import User


class RPC:
    @web.rpc("social_get_user", "get_user")
    def get_user(self, user_id: int) -> dict:
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return {}
        return user.to_json()
