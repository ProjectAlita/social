from tools import db


def init_db():
    from .models.likes import Like
    from .models.users import User
    from .models.feedbacks import Feedback
    db.get_shared_metadata().create_all(bind=db.engine)
