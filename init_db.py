from tools import db


def init_db():
    from .models.likes import Like
    db.get_shared_metadata().create_all(bind=db.engine)
