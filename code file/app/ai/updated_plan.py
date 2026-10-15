from google.genai import types

from app.config import GEMINI_MODEL

from app.ai.gemini_client import get_gemini_client

from app.ai.gemini_generator import (
    SYSTEM_INSTRUCTIONS
)


def update_workout_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    age: int
):

    client = get_gemini_client()

    prompt = f"""
{SYSTEM_INSTRUCTIONS}

You are updating a FitBuddy 7-day fitness plan.

USER AGE:
{age}

FITNESS GOAL:
{goal}

USER FEEDBACK:
{feedback}

ORIGINAL PLAN:
--------------------------------
{original_plan}
--------------------------------

Create a revised complete 7-day fitness plan.

Apply the user's feedback where it is safe and reasonable.

Important:
- Keep the plan beginner-friendly.
- Keep at least one recovery day.
- Do not provide medical diagnosis or treatment.
- Do not recommend extreme workouts.
- Do not recommend starvation, dehydration, unsafe supplements,
  rapid weight loss, or extreme dieting.
- If the user reports pain, dizziness, or unusual symptoms,
  recommend stopping exercise and seeking professional advice.
- Provide easier alternatives.

Use this exact structure:

FITBUDDY - UPDATED 7 DAY FITNESS PLAN

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

Safety Note:
Stop exercising if you experience pain, dizziness,
or unusual symptoms. Consult a qualified healthcare
or fitness professional for health concerns.

Return only the updated plan.
"""

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.5,
                max_output_tokens=5000
            )
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        print("Gemini updated plan generated successfully.")

        return response.text.strip()

    except Exception as e:

        print("=" * 40)
        print("GEMINI UPDATED PLAN ERROR:")
        print(repr(e))
        print("Using safe local fallback plan.")
        print("=" * 40)

        # --------------------------------
        # SAFE LOCAL FALLBACK
        # --------------------------------

        feedback_lower = feedback.lower()

        # Default values
        day1_duration = "15-20 minutes"
        day1_exercises = (
            "Chair squats, wall push-ups, "
            "glute bridges and marching."
        )
        day1_sets = "2 sets of 8-10 repetitions."

        # Apply common feedback automatically
        if (
            "easier" in feedback_lower
            or "easy" in feedback_lower
            or "reduce" in feedback_lower
            or "short" in feedback_lower
            or "duration" in feedback_lower
        ):
            day1_duration = "10-15 minutes"
            day1_exercises = (
                "Chair squats, wall push-ups "
                "and gentle marching."
            )
            day1_sets = "1-2 sets of 6-8 repetitions."

        fallback_plan = f"""
FITBUDDY - UPDATED 7 DAY FITNESS PLAN

DAY 1
Focus: Beginner Full Body Movement
Warm-up: 3-5 minutes of easy walking.
Main Workout: {day1_exercises}
Sets/Repetitions or Duration: {day1_sets}
Rest: 60 seconds between exercises.
Cool-down: 3-5 minutes of gentle stretching.
Easier Alternative: Reduce repetitions or use chair support.

DAY 2
Focus: Light Cardio
Warm-up: 5 minutes of slow walking.
Main Workout: Comfortable walking at an easy pace.
Sets/Repetitions or Duration: 15-20 minutes.
Rest: Take short breaks whenever needed.
Cool-down: 5 minutes of gentle stretching.
Easier Alternative: Walk for a shorter duration.

DAY 3
Focus: Beginner Strength
Warm-up: 5 minutes of easy movement.
Main Workout: Chair squats, wall push-ups and glute bridges.
Sets/Repetitions or Duration: 2 sets of 8-10 repetitions.
Rest: 45-60 seconds between exercises.
Cool-down: 5 minutes of gentle stretching.
Easier Alternative: Reduce repetitions and use support.

DAY 4
Focus: Recovery and Mobility
Warm-up: 3-5 minutes of slow walking.
Main Workout: Gentle mobility, stretching and relaxed walking.
Sets/Repetitions or Duration: 10-15 minutes.
Rest: Rest whenever needed.
Cool-down: Gentle stretching and relaxed breathing.
Easier Alternative: Very gentle mobility only.

DAY 5
Focus: Full Body Strength
Warm-up: 5 minutes of easy walking.
Main Workout: Chair squats, wall push-ups, glute bridges and marching.
Sets/Repetitions or Duration: 2 sets of 8-10 repetitions.
Rest: 45-60 seconds between exercises.
Cool-down: 5 minutes of gentle stretching.
Easier Alternative: Use chair support and reduce repetitions.

DAY 6
Focus: Light Cardio
Warm-up: 5 minutes of slow walking.
Main Workout: Comfortable walking at an easy-to-moderate pace.
Sets/Repetitions or Duration: 15-25 minutes.
Rest: Take breaks whenever needed.
Cool-down: 5 minutes of slow walking and stretching.
Easier Alternative: Reduce walking duration.

DAY 7
Focus: Rest and Recovery
Warm-up: Optional gentle walk.
Main Workout: Gentle stretching and mobility.
Sets/Repetitions or Duration: 10-15 minutes.
Rest: Full rest is also acceptable.
Cool-down: Relaxed breathing and gentle stretching.
Easier Alternative: Complete rest.

Safety Note:
Stop exercising if you experience pain, dizziness,
or unusual symptoms. Consult a qualified healthcare
or fitness professional for health concerns.
"""

        return fallback_plan.strip()