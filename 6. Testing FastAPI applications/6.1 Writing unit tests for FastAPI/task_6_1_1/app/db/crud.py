from sqlalchemy.orm import Session
from app.db.database import Base, sync_engine
from app.models.schemas import UserCreate
from app.models.models import User


class SyncCRUD:

    @staticmethod
    def create_tables():
        Base.metadata.drop_all(bind=sync_engine)
        Base.metadata.create_all(bind=sync_engine)

    @staticmethod
    def create_user_db(db: Session, new_user: UserCreate):
        add_user = User(username=new_user.username,
                        password=new_user.password,
                        email=new_user.email,
                        age=new_user.age)
        db.add(add_user)
        db.commit()
        db.refresh(add_user)
        return add_user

    @staticmethod
    def read_user_db(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def delete_user_db(db: Session, user_id: int):
        delete_user = SyncCRUD.read_user_db(db=db, id=user_id)
        if delete_user:
            db.delete(delete_user)
            db.commit()
            return delete_user
        return None
