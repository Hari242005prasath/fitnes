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
                f"The {duration} must be above 0 else return not possible"
            )

            model = genai.GenerativeModel('gemini-1.5-flash')
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)

            return JsonResponse({"fitness_plan": response.text}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)



from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import io
import json
from bs4 import BeautifulSoup

@csrf_exempt
def generate_fitness_pdf(request):
    try:
        if request.method == 'POST':
            # Get the fitness plan content
            fitness_plan_html = request.POST.get('fitness_plan', '')
            
            # Create a buffer for the PDF
            buffer = io.BytesIO()
            
            # Create the PDF object using ReportLab
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Create the elements list to build the PDF
            elements = []
            
            # Get styles
            styles = getSampleStyleSheet()
            title_style = styles['Heading1']
            normal_style = styles['Normal']
            
            # Add title
            elements.append(Paragraph("Your Fitness Plan", title_style))
            elements.append(Spacer(1, 20))
            
            # Parse the HTML content
            soup = BeautifulSoup(fitness_plan_html, 'html.parser')
            
            # Find the table
            table = soup.find('table')
            if table:
                # Extract table data
                table_data = []
                for row in table.find_all('tr'):
                    cols = row.find_all(['th', 'td'])
                    row_data = [Paragraph(col.get_text(strip=True), normal_style) for col in cols]
                    table_data.append(row_data)
                
                # Create the table
                if table_data:
                    pdf_table = Table(table_data, repeatRows=1)
                    pdf_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 1), (-1, -1), 10),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('PADDING', (0, 0), (-1, -1), 6),
                    ]))
                    elements.append(pdf_table)
            
            # Add note at the bottom
            note = soup.find('div', class_='note')
            if note:
                elements.append(Spacer(1, 20))
                elements.append(Paragraph(note.get_text(strip=True), normal_style))
            
            # Build the PDF
            doc.build(elements)
            
            # Get the value of the buffer and create the response
            pdf = buffer.getvalue()
            buffer.close()
            
            # Create the HTTP response
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="fitness_plan.pdf"'
            response.write(pdf)
            
            return response
            
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")  # For debugging
        return HttpResponse(status=500)
    
    return HttpResponse(status=400)


def home(request):
    return render(request, 'myapp/index.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Streak, WorkoutStreak, WorkoutAnalytics


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
    gptinfos = Gptinfo.objects.all().order_by('-created_at')
    return render(request, 'myapp/ourSchedule.html', {'gptinfos': gptinfos})

def streak(request):
    today = timezone.now().date()
    
    # Get all workouts ordered by date
    streak_data = WorkoutStreak.objects.filter(
        date__lte=today
    ).order_by('-date')
    
    streak_count = streak_data.count()
    weekly_workouts = streak_data.filter(
        date__gte=today - timedelta(days=7)
    ).count()
    
    context = {
        'streak_count': streak_count,
        'weekly_workouts': weekly_workouts,
        'workouts': streak_data[:7]
    }
    
    return render(request, 'myapp/streak.html', context)

def analytics(request):
    today = timezone.now().date()
    
    # Get all workouts
    workouts = WorkoutStreak.objects.all().order_by('date')
    
    # Calculate current streak
    streak_count = 0
    check_date = today
    while WorkoutStreak.objects.filter(date=check_date).exists():
        streak_count += 1
        check_date -= timedelta(days=1)
    
    # Calculate longest streak
    longest_streak = 0
    current_streak = 0
    prev_date = None
    
    for workout in workouts:
        if prev_date is None or (workout.date - prev_date).days == 1:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1
        prev_date = workout.date
    
    # Get workout distribution
    workout_types = WorkoutStreak.objects.values('workout_type').annotate(
        count=Count('workout_type')
    )
    
    # Get weekly progress data
    week_data = []
    for i in range(7):
        date = today - timedelta(days=i)
        workout = WorkoutStreak.objects.filter(date=date).first()
        week_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'duration': workout.duration if workout else 0
        })
    
    context = {
        'current_streak': streak_count,
        'longest_streak': longest_streak,
        'total_workouts': workouts.count(),
        'workout_distribution': list(workout_types),
        'weekly_progress': week_data
    }
    
    return render(request, 'myapp/analytics.html', context)




from django.shortcuts import render, redirect
from django.contrib import messages
from .models import userDetails

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Check if user exists in userDetails model
            user = userDetails.objects.get(user=username, password=password)
            
            # If user exists, create a session and redirect to index/home
            request.session['user_id'] = user.id
            messages.success(request, 'Login successful!')
            return redirect('index')  # or use 'home' if that's your URL name
            
        except userDetails.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return render(request, 'myapp/login.html')
    
    return render(request, 'myapp/login.html')


import json
import io
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from bs4 import BeautifulSoup
from .models import Gptinfo
from django.utils import timezone

@csrf_exempt
def save_fitness_plan(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fitness_plan = data.get('fitness_plan', '')
            
            # Generate filename with timestamp
            timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
            filename = f'fitness_plan_{timestamp}.pdf'
            
            # Save to Gptinfo model
            gptinfo = Gptinfo()
            gptinfo.pdf_file.save(filename, ContentFile(fitness_plan.encode()))
            gptinfo.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Plan saved successfully!'
            })
            
        except Exception as e:
            print(f"Error saving plan: {str(e)}")  # For debugging
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=400)


from django.shortcuts import render
from .models import Gptinfo

def display_fitness_plan(request):
    gptinfos = Gptinfo.objects.all()
    return render(request, 'myapp/ourOldschedule.html', {'gptinfos': gptinfos})


from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import WorkoutStreak, WorkoutAnalytics
from django.db.models import Count
from django.http import JsonResponse
from datetime import timedelta

@login_required
def streak(request):
    if request.method == 'POST':
        # Handle the streak check-in
        today = timezone.now().date()
        workout_type = request.POST.get('workout_type', '')
        duration = request.POST.get('duration', 0)
        
        streak, created = WorkoutStreak.objects.get_or_create(
            date=today,
            defaults={
                'workout_type': workout_type,
                'duration': duration
            }
        )
        
        if not created:
            streak.workout_type = workout_type
            streak.duration = duration
            streak.save()
            
        # Update analytics
        analytics, _ = WorkoutAnalytics.objects.get_or_create(user=request.user)
        analytics.total_workouts += 1
        
        # Calculate current streak
        consecutive_days = 0
        check_date = today
        while WorkoutStreak.objects.filter(date=check_date).exists():
            consecutive_days += 1
            check_date = check_date - timezone.timedelta(days=1)
        
        analytics.current_streak = consecutive_days
        analytics.longest_streak = max(analytics.longest_streak, consecutive_days)
        analytics.save()
        
        return JsonResponse({'status': 'success', 'streak': consecutive_days})
    
    # Get user's streak data for display
    streak_data = WorkoutStreak.objects.filter(
        date__gte=timezone.now().date() - timedelta(days=30)
    ).order_by('-date')[:30]  # Last 30 days
    
    analytics, _ = WorkoutAnalytics.objects.get_or_create(user=request.user)
    
    context = {
        'streak_data': streak_data,
        'current_streak': analytics.current_streak,
        'longest_streak': analytics.longest_streak,
        'total_workouts': analytics.total_workouts
    }
    
    return render(request, 'myapp/streak.html', context)



def log_workout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create or update today's workout
            workout, created = WorkoutStreak.objects.update_or_create(
                date=timezone.now().date(),
                defaults={
                    'workout_type': data['workout_type'],
                    'duration': int(data['duration']),
                    'calories': int(data.get('calories', 0)),
                    'notes': data.get('notes', '')
                }
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Workout updated successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)