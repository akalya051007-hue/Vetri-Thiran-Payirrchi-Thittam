from datetime import datetime, timezone

from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Float,
    Text,
    DateTime
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker
)

from app.config import DATABASE_URL


# --------------------------------
# Database Engine
# --------------------------------

connect_args = {}

if DATABASE_URL.startswith("sqlite"):

    connect_args = {
        "check_same_thread": False
    }


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# --------------------------------
# Base Class
# --------------------------------

class Base(DeclarativeBase):
    pass


# --------------------------------
# User Table
# --------------------------------

class User(Base):

    __tablename__ = "users"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id: Mapped[str] = mapped_column(
        String(80),
        unique=True,
        index=True
    )


    username: Mapped[str] = mapped_column(
        String(120)
    )


    age: Mapped[int] = mapped_column(
        Integer
    )


    weight: Mapped[float] = mapped_column(
        Float
    )


    goal: Mapped[str] = mapped_column(
        String(80)
    )


    intensity: Mapped[str] = mapped_column(
        String(20)
    )


    original_plan: Mapped[str] = mapped_column(
        Text
    )


    updated_plan: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    nutrition_tip: Mapped[str] = mapped_column(
        Text
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


# --------------------------------
# Initialize Database
# --------------------------------

def init_db():

    Base.metadata.create_all(
        bind=engine
    )


# --------------------------------
# Get User
# --------------------------------

def get_user(user_id: str):

    with SessionLocal() as db:

        return (
            db.query(User)
            .filter(
                User.user_id == user_id
            )
            .first()
        )


# --------------------------------
# Save User
# --------------------------------

def save_user(data):

    with SessionLocal() as db:

        user = User(**data)

        db.add(user)

        db.commit()

        db.refresh(user)

        return user


# --------------------------------
# Get All Users
# --------------------------------

def get_all_users():

    with SessionLocal() as db:

        return (
            db.query(User)
            .order_by(
                User.created_at.desc()
            )
            .all()
        )


# --------------------------------
# Update User Plan
# --------------------------------

def update_user_plan(
    user_id: str,
    updated_plan: str,
    feedback: str
):

    with SessionLocal() as db:

        user = (
            db.query(User)
            .filter(
                User.user_id == user_id
            )
            .first()
        )

        if not user:

            return None


        user.updated_plan = updated_plan

        user.feedback = feedback


        db.commit()

        db.refresh(user)

        return user


# --------------------------------
# Update User Information
# --------------------------------

def update_user_details(
    user_id: str,
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
    original_plan: str,
    nutrition_tip: str
):

    with SessionLocal() as db:

        user = (
            db.query(User)
            .filter(
                User.user_id == user_id
            )
            .first()
        )

        if not user:

            return None


        user.username = username

        user.age = age

        user.weight = weight

        user.goal = goal

        user.intensity = intensity

        user.original_plan = original_plan

        user.updated_plan = None

        user.feedback = None

        user.nutrition_tip = nutrition_tip


        db.commit()

        db.refresh(user)

        return user


# --------------------------------
# Delete User
# --------------------------------

def delete_user(user_id: str):

    with SessionLocal() as db:

        user = (
            db.query(User)
            .filter(
                User.user_id == user_id
            )
            .first()
        )

        if not user:

            return False


        db.delete(user)

        db.commit()

        return True