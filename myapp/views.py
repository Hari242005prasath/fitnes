from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
import os

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv("AIzaSyCZ62IZsy-jNJYiBSdyGwMCg6pe_ly6Q94")  # Store API key in an environment variable
genai.configure(api_key=GOOGLE_API_KEY)

# Define reasonable input limits
MIN_AGE, MAX_AGE = 1, 120
MIN_WEIGHT, MAX_WEIGHT = 10, 300  # kg
MIN_HEIGHT, MAX_HEIGHT = 50, 250  # cm
VALID_DURATIONS = ["weekly", "monthly", "yearly"]  # Example valid durations

def generate_fitness_plan(request):
    if request.method == "POST":
        try:
            # Retrieve form data
            duration = request.POST.get("duration", "").lower()
            goal = request.POST.get("goal", "").strip()
            fitness_level = request.POST.get("fitness_level", "").strip()
            age = int(request.POST.get("age", 0))
            gender = request.POST.get("gender", "").strip().lower()
            weight = float(request.POST.get("weight", 0))
            height = float(request.POST.get("height", 0))
            activity_level = request.POST.get("activity_level", "").strip()
            diet_preference = request.POST.get("diet_preference", "").strip()
            equipment = request.POST.getlist("equipment")

            # Validate input data
            if (
                duration not in VALID_DURATIONS or
                not (MIN_AGE <= age <= MAX_AGE) or
                not (MIN_WEIGHT <= weight <= MAX_WEIGHT) or
                not (MIN_HEIGHT <= height <= MAX_HEIGHT)
            ):
                return JsonResponse({"error": "Data inadequate. Please provide valid inputs."})

            # Create prompt for AI
            prompt = (
                f"Create a {duration} fitness plan for a {age}-year-old {gender} "
                f"with a weight of {weight} kg and height of {height} cm. The fitness level is {fitness_level}, "
                f"and their primary goal is {goal}. They follow a {diet_preference} diet and have an activity level of {activity_level}. "
                f"Provide a detailed plan with cardio, strength, flexibility exercises, and rest days. "
                f"Also suggest exercises using the following equipment: {', '.join(equipment) if equipment else 'None'}."
            )

            # Generate fitness plan using Google Gemini API
            model = genai.GenerativeModel("gemini-1.5-flash")
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)

            return JsonResponse({"plan": response.text.replace("*", "").strip()})

        except ValueError:
            return JsonResponse({"error": "Invalid numerical input. Please check age, weight, and height."})
        except Exception as e:
            return JsonResponse({"error": f"Error generating fitness plan: {e}"})

    return render(request, "myapp/index.html")

def home(request):
    return render(request, 'myapp/index.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Streak


@login_required
def dashboard(request):
    streak, created = Streak.objects.get_or_create(user=request.user)
    if request.method == 'POST':  # When user logs activity
        streak.update_streak()
        return redirect('dashboard')

    return render(request, 'dashboard.html', {'streak': streak})


from django.shortcuts import render

def index(request):
    return render(request, 'myapp/index.html')

def about(request):
    return render(request, 'myapp/about.html')

def contact(request):
    return render(request, 'myapp/contact.html')

def joinin(request):
    return render(request, 'myapp/joinin.html')

def newSchedule(request):
    # Your view logic here
    return render(request, 'myapp/newSchedule.html')

def ourSchedule(request):
    # Your view logic here
    return render(request, 'myapp/ourSchedule.html')

def streak(request):
    return render(request,'myapp/streak.html')