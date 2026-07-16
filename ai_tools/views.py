from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import ask_claude


@login_required
def resume_review(request):
    feedback = None
    error = None
    resume_text = ""

    if request.method == "POST":
        resume_text = (request.POST.get("resume_text") or "").strip()[:8000]
        if resume_text:
            system_prompt = (
                "You are a helpful, encouraging tech career coach reviewing resumes "
                "for developers, designers, and tech professionals. Give specific, "
                "actionable feedback in these sections: Strengths, Areas to Improve, "
                "and Suggested Rewrites. Keep it concise and practical."
            )
            feedback = ask_claude(system_prompt, resume_text, max_tokens=1200)
            if feedback is None:
                error = "Something went wrong talking to the AI. Please try again."
        else:
            error = "Please paste your resume text first."

    return render(request, "ai_tools/resume_review.html", {
        "feedback": feedback,
        "error": error,
        "resume_text": resume_text,
    })


@login_required
def idea_generator(request):
    ideas = None
    error = None
    skills = ""
    interests = ""

    if request.method == "POST":
        skills = (request.POST.get("skills") or "").strip()[:500]
        interests = (request.POST.get("interests") or "").strip()[:500]
        if skills:
            system_prompt = (
                "You are a creative tech project mentor. Based on the user's skills "
                "and interests, suggest 3 project ideas they could build. For each idea "
                "give: a title, a 2-sentence description, difficulty level (Beginner/"
                "Intermediate/Advanced), and 2-3 key technologies to use. Format clearly "
                "with headers for each idea."
            )
            user_message = f"Skills: {skills}\nInterests: {interests or 'Not specified'}"
            ideas = ask_claude(system_prompt, user_message, max_tokens=1200)
            if ideas is None:
                error = "Something went wrong talking to the AI. Please try again."
        else:
            error = "Please enter at least your skills."

    return render(request, "ai_tools/idea_generator.html", {
        "ideas": ideas,
        "error": error,
        "skills": skills,
        "interests": interests,
    })


@login_required
def interview_prep(request):
    questions = None
    error = None
    role = ""
    level = "mid"

    if request.method == "POST":
        role = (request.POST.get("role") or "").strip()[:200]
        level = request.POST.get("level") or "mid"
        if level not in ["junior", "mid", "senior"]:
            level = "mid"
        if role:
            system_prompt = (
                "You are a technical interviewer. Generate 5 realistic interview "
                "questions for the given role and experience level, mixing technical "
                "and behavioral questions. For each question, include a short note on "
                "what a good answer should cover. Format clearly with numbering."
            )
            user_message = f"Role: {role}\nExperience level: {level}"
            questions = ask_claude(system_prompt, user_message, max_tokens=1200)
            if questions is None:
                error = "Something went wrong talking to the AI. Please try again."
        else:
            error = "Please enter a role to prepare for."

    return render(request, "ai_tools/interview_prep.html", {
        "questions": questions,
        "error": error,
        "role": role,
        "level": level,
    })
