from pydantic import ValidationError, parse_obj_as
from sqlalchemy import func
from traceback import format_exc
from typing import Optional, List

from tools import rpc_tools, db, auth
from pylon.core.tools import web, log

from ..models.likes import Like
from ..models.pd.likes import LikeModel


class RPC:
    @web.rpc(f'social_like', "like")
    def create_like(
        self, project_id: int | None, entity: str, entity_id: int, user_id: int = None
        ) -> dict:
        if not user_id:
            user_id = auth.current_user().get("id")
        try:
            like_data = LikeModel(
                entity=entity,
                entity_id=entity_id,
                user_id=user_id,
                project_id=project_id
            )
        except ValidationError as e:
            return {'ok': False, 'error': str(e)}
        like = Like(**like_data.dict())
        like.insert()
        return {'ok': True, 'like_id': like.id}

    @web.rpc("social_dislike", "dislike")
    def delete_like(
        self, project_id: int | None, entity: str, entity_id: int, user_id: int = None
        ) -> dict:
        if not user_id:
            user_id = auth.current_user().get("id")
        like = Like.query.filter(
            Like.project_id == project_id,
            Like.user_id == user_id,
            Like.entity == entity,
            Like.entity_id == entity_id
        ).first()
        if like:
            like.delete()
            return {'ok': True}
        return {'ok': False}

    @web.rpc("social_is_liked", "is_liked")
    def check_like(
        self, project_id: int | None, entity: str, entity_id: int, user_id: int = None
        ) -> bool:
        if not user_id:
            user_id = auth.current_user().get("id")
        like = Like.query.filter(
            Like.project_id == project_id,
            Like.user_id == user_id,
            Like.entity == entity,
            Like.entity_id == entity_id
        ).first()
        return like is not None

    @web.rpc("social_get_likes", "get_likes")
    def get_likes(
        self, project_id: int | None, entity: str, entity_id: int
        ) -> dict:
        likes = Like.query.filter(
            Like.project_id == project_id,
            Like.entity == entity,
            Like.entity_id == entity_id
        ).all()
        return {'total': len(likes), 'rows': [like.to_json() for like in likes]}

    @web.rpc("social_get_top_likes", "get_top_likes")
    def get_top_likes(
        self, project_id: int | None, entity: str, top_n: int = 10
        ) -> list[dict]:
        query = (
            Like.query(
                Like.project_id, Like.entity_id, func.count(Like.id).label('likes')
                )
            .filter(Like.project_id == project_id, Like.entity == entity)
            .group_by(Like.project_id, Like.entity_id)
            .order_by(func.count(Like.id).desc())
            .limit(top_n)
        )
        return [like.to_json() for like in query.all()]

    @web.rpc("social_get_like_model", "get_like_model")
    def get_like_model(self):
        return Like
