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
                f"activity level of {activity_level}. Provide a structured day-by-day plan in **valid HTML table format**, "
                f"with proper `<table>`, `<tr>`, and `<td>` tags for alignment."

                f"The table should have these columns: *Day, Time, Exercise Type, Workout Details (Reps, Sets, Duration), Protein Goal (g), Meal Plan (Breakfast, Lunch, Dinner, Snacks)*. "
                f"Ensure that the meal plan aligns with their {diet_preference} diet and supports their goal (muscle gain, weight loss, endurance, etc.). "

                f"Include rest days where appropriate, and ensure exercises use the provided equipment: {', '.join(equipment) if equipment else 'None'}. "
                f"The {age} should not exceed above 80.If it exceeds do not generate the plan. "
            )

            model = genai.GenerativeModel('gemini-1.5-flash')
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)

            return JsonResponse({"fitness_plan": response.text}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)



from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io
import json
from bs4 import BeautifulSoup

def generate_fitness_pdf(request):
    try:
        if request.method != "POST":
            return JsonResponse({"error": "Invalid request method"}, status=400)

        if request.content_type == "application/json":
            data = json.loads(request.body.decode("utf-8"))
            fitness_plan_html = data.get("fitness_plan", "").strip()
        else:
            fitness_plan_html = request.POST.get("fitness_plan", "").strip()

        if not fitness_plan_html:
            return JsonResponse({"error": "No fitness plan data received"}, status=400)

        # Convert AI-generated HTML table to structured data
        soup = BeautifulSoup(fitness_plan_html, "html.parser")
        table_data = []

        styles = getSampleStyleSheet()
        body_style = styles["BodyText"]
        body_style.wordWrap = "LTR"  # Enable word wrapping

        for row in soup.find_all("tr"):
            columns = [Paragraph(col.get_text(strip=True), body_style) for col in row.find_all(["th", "td"])]
            table_data.append(columns)

        if not table_data:
            return JsonResponse({"error": "Invalid table format in AI response"}, status=400)

        # Generate PDF
        buffer = io.BytesIO()
        
        # Set proper margins (2cm on left & right)
        margin = 56.7  # 2 cm in points
        page_width, page_height = letter
        available_width = page_width - (2 * margin)  # Adjusted width after margins
        
        doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=margin, rightMargin=margin)
        elements = []

        # Add title with spacing
        title = Paragraph("<b>Your Fitness Plan</b>", styles["Title"])
        elements.append(title)
        elements.append(Spacer(1, 12))  # Add space after title

        # Define column widths dynamically to fit within available width
        num_columns = len(table_data[0]) if table_data else 5  # Default to 5 columns
        col_widths = [available_width / num_columns] * num_columns  # Distribute width evenly

        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ]))

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="fitness_plan.pdf"'
        return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Gptinfo

@csrf_exempt
def save_fitness_plan(request):
    """Generate and save a fitness plan PDF"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            fitness_plan_text = data.get("fitness_plan", "")

            if not fitness_plan_text:
                return JsonResponse({"error": "No fitness plan provided"}, status=400)

            # Generate PDF
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.drawString(100, 750, "Your AI-Generated Fitness Plan")

            y_position = 730  # Start position
            for line in fitness_plan_text.split("\n"):
                p.drawString(100, y_position, line)
                y_position -= 20  # Move down

            p.save()
            buffer.seek(0)

            # Save to database
            pdf_filename = "fitness_plan.pdf"
            gptinfo_instance = Gptinfo()
            gptinfo_instance.pdf_file.save(pdf_filename, buffer, save=True)

            return JsonResponse({
                "success": True,
                "message": "Fitness plan saved successfully!",
                "pdf_url": gptinfo_instance.pdf_file.url
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


from django.shortcuts import render
from django.http import JsonResponse
from .models import Gptinfo

def display_fitness_plan(request):
    plans = Gptinfo.objects.all()

    # Get the latest plan (modify logic if needed)
    latest_plan = plans.last()  # Retrieves the most recent PDF

    context = {"fitness_plan_url": latest_plan.pdf_file.url if latest_plan else None}

    return render(request, "myapp/ourOldschedule.html", context)


def streak(request):
    return render(request,'myapp/streak.html')