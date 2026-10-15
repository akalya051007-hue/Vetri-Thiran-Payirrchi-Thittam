from fastapi import (
    APIRouter,
    Request,
    Form,
    HTTPException
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse
)

from fastapi.templating import (
    Jinja2Templates
)

from app.config import ADMIN_KEY

from app.schemas import (
    UserInput,
    FeedbackRequest
)

from app.database import (
    get_user,
    save_user,
    get_all_users,
    update_user_plan,
    update_user_details,
    delete_user
)

from app.ai.gemini_generator import (
    generate_workout_gemini,
    generate_nutrition_tip
)

from app.ai.updated_plan import (
    update_workout_plan
)


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# ==========================================
# HOME
# ==========================================

@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "error": None
        }
    )


# ==========================================
# GENERATE WORKOUT
# ==========================================

@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    try:

        # ------------------------------------------
        # Create validated user data
        # ------------------------------------------

        user_data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )


        # ------------------------------------------
        # Generate workout using Gemini
        # ------------------------------------------

        workout = generate_workout_gemini(
            username=user_data.username,
            user_id=user_data.user_id,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity
        )


        # ------------------------------------------
        # Generate nutrition tip
        # ------------------------------------------

        nutrition_tip = generate_nutrition_tip(
            goal=user_data.goal,
            age=user_data.age
        )


        # ------------------------------------------
        # Check existing user
        # ------------------------------------------

        existing_user = get_user(
            user_data.user_id
        )


        # ------------------------------------------
        # Update existing user
        # ------------------------------------------

        if existing_user:

            user = update_user_details(
                user_id=user_data.user_id,
                username=user_data.username,
                age=user_data.age,
                weight=user_data.weight,
                goal=user_data.goal,
                intensity=user_data.intensity,
                original_plan=workout,
                nutrition_tip=nutrition_tip
            )


        # ------------------------------------------
        # Create new user
        # ------------------------------------------

        else:

            user = save_user({
                "username": user_data.username,
                "user_id": user_data.user_id,
                "age": user_data.age,
                "weight": user_data.weight,
                "goal": user_data.goal,
                "intensity": user_data.intensity,
                "original_plan": workout,
                "updated_plan": None,
                "feedback": None,
                "nutrition_tip": nutrition_tip
            })


        # ------------------------------------------
        # Show result page
        # ------------------------------------------

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "message": "Your AI fitness plan has been generated.",
                "error": None
            }
        )


    except Exception as exc:

        print("========================================")
        print("GENERATE WORKOUT ERROR:")
        print(repr(exc))
        print("========================================")

        raise


# ==========================================
# SUBMIT FEEDBACK / UPDATE PLAN
# ==========================================

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):

    try:

        # ------------------------------------------
        # Validate feedback data
        # ------------------------------------------

        feedback_data = FeedbackRequest(
            user_id=user_id,
            feedback=feedback
        )


        # ------------------------------------------
        # Find user
        # ------------------------------------------

        user = get_user(
            feedback_data.user_id
        )


        if not user:

            raise HTTPException(
                status_code=404,
                detail="User ID was not found."
            )


        # ------------------------------------------
        # Generate updated plan
        # ------------------------------------------

        updated_plan = update_workout_plan(
            original_plan=user.original_plan,
            feedback=feedback_data.feedback,
            goal=user.goal,
            age=user.age
        )


        # ------------------------------------------
        # Save updated plan
        # ------------------------------------------

        updated_user = update_user_plan(
            user_id=user.user_id,
            updated_plan=updated_plan,
            feedback=feedback_data.feedback
        )


        # ------------------------------------------
        # Show updated result
        # ------------------------------------------

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": updated_user,
                "message": "Your plan was updated successfully using Gemini AI.",
                "error": None
            }
        )


    except Exception as exc:

        print("========================================")
        print("UPDATE PLAN ERROR:")
        print(repr(exc))
        print("========================================")

        raise


# ==========================================
# ADMIN - VIEW ALL USERS
# ==========================================

@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(
    request: Request,
    key: str = ""
):

    if key != ADMIN_KEY:

        raise HTTPException(
            status_code=403,
            detail="Invalid admin key."
        )


    users = get_all_users()


    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users
        }
    )


# ==========================================
# ADMIN - DELETE USER
# ==========================================

@router.post(
    "/delete-user"
)
def remove_user(
    user_id: str = Form(...),
    key: str = Form(...)
):

    if key != ADMIN_KEY:

        raise HTTPException(
            status_code=403,
            detail="Invalid admin key."
        )


    delete_user(user_id)


    return RedirectResponse(
        url=f"/view-all-users?key={key}",
        status_code=303
    )


# ==========================================
# HEALTH CHECK
# ==========================================

@router.get("/health")
def health():

    return {
        "status": "ok",
        "application": "FitBuddy",
        "message": "FitBuddy backend is running"
    }
