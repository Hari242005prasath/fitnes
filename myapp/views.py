import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import userDetails

# Configure Google AI
GOOGLE_API_KEY = "AIzaSyCZ62IZsy-jNJYiBSdyGwMCg6pe_ly6Q94"
genai.configure(api_key=GOOGLE_API_KEY)

@csrf_exempt
def generate_fitness_plan(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            duration = data.get("duration", "4 weeks")
            goal = data.get("goal", "General Fitness")
            fitness_level = data.get("fitness_level", "Beginner")
            age = data.get("age", 25)
            gender = data.get("gender", "Male")
            weight = data.get("weight", 70)
            height = data.get("height", 170)
            activity_level = data.get("activity_level", "Moderately Active")
            diet_preference = data.get("diet_preference", "None")
            equipment = data.get("equipment", [])

            prompt = (
                f"Create a {duration} fitness plan for a {age}-year-old {gender} with a weight of {weight} kg and height of {height} cm. "
                f"The fitness level is {fitness_level}, and their primary goal is {goal}. They follow a {diet_preference} diet and have an "
                f"activity level of {activity_level}. Provide a structured day-by-day plan with clear headings (e.g., 'Week 1, Day 1 - Date, Time'). "
                f"The plan should include cardio, strength, flexibility exercises, and rest days. Specify exercise duration, intensity, and repetitions where applicable. "
                f"Also, incorporate exercises using the following equipment: {', '.join(equipment) if equipment else 'None'}. "
                f"If the provided data is insufficient or unrealistic, state explicitly that creating a fitness plan is impossible."
            )


            model = genai.GenerativeModel('gemini-1.5-flash')
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)

            return JsonResponse({"fitness_plan": response.text.replace("*", "").strip()}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


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




from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")  # Form field name
        password = request.POST.get("password")

        try:
            user = userDetails.objects.get(user=username, password=password)  # Use 'user' instead of 'username'
            request.session["user_id"] = user.id  # Store user session
            messages.success(request, "Login successful!")
            return redirect("home")  # Redirect to home page
        except userDetails.DoesNotExist:
            messages.error(request, "Invalid username or password")

    return render(request, "myapp/login.html")


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Gptinfo

@csrf_exempt
def save_fitness_plan(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            fitness_plan = data.get("fitness_plan", "")

            if fitness_plan:
                Gptinfo.objects.create(text=fitness_plan)
                return JsonResponse({"message": "Schedule saved successfully!"}, status=201)
            else:
                return JsonResponse({"error": "No fitness plan provided"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)


def display_fitness_plan(request):
    """Fetch the latest saved fitness plan and display it in another page"""
    latest_plan = Gptinfo.objects.last()  # Get the latest saved plan
    return render(request, "myapp/ourOldschedule.html", {"fitness_plan": latest_plan.text if latest_plan else "No schedule found!"})
