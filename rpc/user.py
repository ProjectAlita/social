from typing import List
from pylon.core.tools import web, log

from ..models.users import User


class RPC:
    @web.rpc("social_get_user", "get_user")
    def get_user(self, user_id: int) -> dict:
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return {}
        return user.to_json()

    @web.rpc("social_get_users", "get_users")
    def get_user(self, user_ids: List[int]) -> List[dict]:
        users = User.query.filter(User.user_id.in_(user_ids)).all()
        return [user.to_json() for user in users]
