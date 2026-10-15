from typing import Literal

from pydantic import (
    BaseModel,
    Field
)


# --------------------------------
# User Input Schema
# --------------------------------

class UserInput(BaseModel):

    username: str = Field(
        min_length=2,
        max_length=120
    )


    user_id: str = Field(
        min_length=2,
        max_length=80
    )


    age: int = Field(
        ge=13,
        le=100
    )


    weight: float = Field(
        gt=0,
        le=500
    )


    goal: Literal[
        "weight loss",
        "muscle gain",
        "general wellness",
        "flexibility",
        "endurance"
    ]


    intensity: Literal[
        "low",
        "medium",
        "high"
    ]


# --------------------------------
# Feedback Schema
# --------------------------------

class FeedbackRequest(BaseModel):

    user_id: str = Field(
        min_length=2,
        max_length=80
    )


    feedback: str = Field(
        min_length=3,
        max_length=1000
    )