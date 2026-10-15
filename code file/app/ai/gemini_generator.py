from google.genai import types

from app.config import GEMINI_MODEL
from app.ai.gemini_client import get_gemini_client


# --------------------------------
# Safety Instructions
# --------------------------------

SYSTEM_INSTRUCTIONS = """
You are FitBuddy, an AI-powered fitness and wellness planning assistant.

Your job is to create practical, general wellness-oriented fitness plans.

Do not provide medical diagnosis.
Do not provide medical treatment.

Do not recommend:
- starvation
- dehydration
- dangerous exercises
- extreme workouts
- unsafe supplements
- rapid weight loss
- extreme dieting
- eating disorder behaviors

For users below 18:
- Focus on healthy movement, strength, mobility, recovery, sleep,
  and balanced nutrition.
- Do not focus on weight loss.

Always encourage users to consult a qualified healthcare or fitness
professional when they have health concerns.

Always tell users to stop exercise if they experience pain, dizziness,
or unusual symptoms.

Provide easier alternatives for exercises when possible.
"""


# --------------------------------
# FALLBACK WORKOUT PLAN
# --------------------------------

def get_fallback_workout(
    username: str,
    age: int,
    goal: str,
    intensity: str
):
    """
    Returns a safe built-in workout plan when Gemini
    is temporarily unavailable.
    """

    return f"""
FITBUDDY - 7 DAY FITNESS PLAN

User: {username}
Age: {age}
Goal: {goal}
Intensity: {intensity}

DAY 1
Focus: Full Body Beginner Movement
Warm-up: 5 minutes of easy walking and gentle mobility.
Main Workout: Bodyweight squats, wall push-ups, glute bridges and marching.
Sets/Repetitions or Duration: 2 sets of 8-10 repetitions each.
Rest: 45-60 seconds between exercises.
Cool-down: 5 minutes of gentle stretching.
Easier Alternative: Chair squats and wall push-ups.

DAY 2
Focus: Light Cardio and Mobility
Warm-up: 5 minutes of slow walking.
Main Workout: Comfortable walking with gentle arm movements.
Sets/Repetitions or Duration: 20-25 minutes.
Rest: Take short breaks whenever needed.
Cool-down: 5 minutes of gentle stretching.
Easier Alternative: Slow walking for a shorter duration.

DAY 3
Focus: Beginner Strength
Warm-up: 5 minutes of easy movement.
Main Workout: Chair squats, wall push-ups, bird-dog and glute bridges.
Sets/Repetitions or Duration: 2 sets of 8-10 repetitions.
Rest: 45-60 seconds between exercises.
Cool-down: 5 minutes of gentle stretching.
Easier Alternative: Reduce repetitions and use a chair for support.

DAY 4
Focus: Recovery and Mobility
Warm-up: 5 minutes of slow walking.
Main Workout: Gentle stretching, mobility exercises and relaxed walking.
Sets/Repetitions or Duration: 15-20 minutes.
Rest: Rest whenever needed.
Cool-down: Slow breathing and gentle stretching.
Easier Alternative: Perform only comfortable mobility exercises.

DAY 5
Focus: Full Body Strength
Warm-up: 5 minutes of easy walking and mobility.
Main Workout: Squats, wall push-ups, glute bridges and standing knee raises.
Sets/Repetitions or Duration: 2 sets of 8-12 repetitions.
Rest: 45-60 seconds between exercises.
Cool-down: 5 minutes of gentle stretching.
Easier Alternative: Chair squats and supported movements.

DAY 6
Focus: Light Cardio
Warm-up: 5 minutes of slow walking.
Main Workout: Comfortable walking at an easy-to-moderate pace.
Sets/Repetitions or Duration: 20-30 minutes.
Rest: Take breaks whenever needed.
Cool-down: 5 minutes of slow walking and stretching.
Easier Alternative: Reduce the walking duration.

DAY 7
Focus: Rest and Recovery
Warm-up: Optional 5-minute gentle walk.
Main Workout: Gentle mobility, stretching and relaxed walking.
Sets/Repetitions or Duration: 10-20 minutes.
Rest: Full rest is also acceptable.
Cool-down: Relaxed breathing and gentle stretching.
Easier Alternative: Complete rest or very gentle movement.

Safety Note:
Stop exercising if you experience pain, dizziness, or unusual symptoms.
For health concerns, consult a qualified healthcare or fitness professional.
""".strip()


# --------------------------------
# FALLBACK NUTRITION TIP
# --------------------------------

def get_fallback_nutrition_tip(
    goal: str,
    age: int
):
    """
    Returns a safe built-in nutrition/recovery tip
    when Gemini is temporarily unavailable.
    """

    return (
        "Tip: Choose balanced meals with vegetables, fruits, "
        "whole grains and protein-rich foods, and drink enough water. "
        "Get adequate sleep and allow your body enough time to recover "
        "between workouts."
    )


# --------------------------------
# Generate Workout
# --------------------------------

def generate_workout_gemini(
    username: str,
    user_id: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
):

    client = get_gemini_client()

    prompt = f"""
You are FitBuddy, a general fitness and wellness assistant.

Create a practical beginner-friendly 7-day fitness plan.

User:
Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Safety rules:
- Keep workouts beginner-friendly.
- No extreme workouts.
- No starvation or dehydration.
- No unsafe supplements.
- No rapid weight-loss advice.
- Include rest and recovery.
- Include at least one recovery-oriented day.
- Tell the user to stop if they experience pain, dizziness,
  or unusual symptoms.
- Do not provide medical diagnosis or treatment.
- Provide easier alternatives for exercises.

Use this format:

FITBUDDY - 7 DAY FITNESS PLAN

DAY 1
Focus:
Warm-up:
Main Workout:
Sets/Repetitions or Duration:
Rest:
Cool-down:
Easier Alternative:

DAY 2
Focus:
Warm-up:
Main Workout:
Sets/Repetitions or Duration:
Rest:
Cool-down:
Easier Alternative:

DAY 3
Focus:
Warm-up:
Main Workout:
Sets/Repetitions or Duration:
Rest:
Cool-down:
Easier Alternative:

DAY 4
Focus:
Warm-up:
Main Workout:
Sets/Repetitions or Duration:
Rest:
Cool-down:
Easier Alternative:

DAY 5
Focus:
Warm-up:
Main Workout:
Sets/Repetitions or Duration:
Rest:
Cool-down:
Easier Alternative:

DAY 6
Focus:
Warm-up:
Main Workout:
Sets/Repetitions or Duration:
Rest:
Cool-down:
Easier Alternative:

DAY 7
Focus:
Warm-up:
Main Workout:
Sets/Repetitions or Duration:
Rest:
Cool-down:
Easier Alternative:

Return only the fitness plan.
"""

    try:

        print("=" * 40)
        print("Trying Gemini AI for workout generation...")
        print("Model:", GEMINI_MODEL)
        print("=" * 40)

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=1500
            )
        )

        if response.text:

            print("=" * 40)
            print("GEMINI WORKOUT SUCCESS")
            print("=" * 40)

            return response.text.strip()

        print("Gemini returned an empty response.")
        print("Using fallback workout plan.")

        return get_fallback_workout(
            username=username,
            age=age,
            goal=goal,
            intensity=intensity
        )

    except Exception as e:

        print("=" * 40)
        print("GEMINI WORKOUT ERROR:")
        print(repr(e))
        print("=" * 40)

        print("Gemini unavailable.")
        print("Using fallback workout plan.")

        return get_fallback_workout(
            username=username,
            age=age,
            goal=goal,
            intensity=intensity
        )


# --------------------------------
# Generate Nutrition Tip
# --------------------------------

def generate_nutrition_tip(
    goal: str,
    age: int
):

    client = get_gemini_client()

    prompt = f"""
You are FitBuddy, a general wellness assistant.

User age:
{age}

Fitness goal:
{goal}

Generate one short nutrition or recovery tip.

Rules:
- Do not give calorie targets.
- Do not recommend starvation.
- Do not recommend extreme diets.
- Do not recommend unsafe supplements.
- Encourage balanced meals.
- Encourage hydration.
- Encourage adequate sleep.
- Encourage recovery.
- If the user is below 18, do not provide weight-loss coaching.

Return only 2-4 sentences.

Start with:

Tip:
"""

    try:

        print("=" * 40)
        print("Trying Gemini AI for nutrition tip...")
        print("=" * 40)

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=300
            )
        )

        if response.text:

            print("=" * 40)
            print("GEMINI NUTRITION SUCCESS")
            print("=" * 40)

            return response.text.strip()

        print("Gemini returned an empty nutrition response.")
        print("Using fallback nutrition tip.")

        return get_fallback_nutrition_tip(
            goal=goal,
            age=age
        )

    except Exception as e:

        print("=" * 40)
        print("GEMINI NUTRITION ERROR:")
        print(repr(e))
        print("=" * 40)

        print("Gemini unavailable.")
        print("Using fallback nutrition tip.")

        return get_fallback_nutrition_tip(
            goal=goal,
            age=age
        )