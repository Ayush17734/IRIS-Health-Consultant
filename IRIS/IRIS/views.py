from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import random
from django.http import HttpResponse
from collections import Counter
from .iris_core import iris_health_consultant as analyze


from django.shortcuts import render, redirect
from .iris_core import iris_health_consultant
from django.contrib.auth.decorators import login_required
from datetime import datetime


from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')





from django.shortcuts import render
from .iris_core import iris_health_consultant

def home(request):
    response = None
    if request.method == 'POST':
        user_query = request.POST.get('query')
        if user_query:
            response = iris_health_consultant(user_query.lower())
    return render(request, 'home.html', {'response': response})

# health/views.py
# health/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .iris_core import iris_health_consultant
from .models import ChatMessage

@login_required
def chat_view(request):
    # Reset the chat history if 'reset' button was clicked
    if request.method == "POST" and 'reset' in request.POST:
        ChatMessage.objects.filter(user=request.user).delete()
        return redirect('chat')

    if request.method == "POST":
        user_message = request.POST.get("message")

        if user_message:
            # Save user message
            ChatMessage.objects.create(user=request.user, sender='user', message=user_message)

            # Build context from recent chat history (last 10 messages for example)
            recent_messages = ChatMessage.objects.filter(user=request.user).order_by('-timestamp')[:10]
            conversation_context = "\n".join(reversed([
                f"You: {m.message}" if m.sender == 'user' else f"IRIS: {m.message}"
                for m in recent_messages
            ]))

            # Get Gemini reply
            bot_reply = iris_health_consultant(
                user_query=user_message,
                user_name=request.user.first_name or request.user.username,
                conversation_context=conversation_context
            )

            # Save bot message
            ChatMessage.objects.create(user=request.user, sender='bot', message=bot_reply)

    # Fetch full chat history for display
    chat_history = ChatMessage.objects.filter(user=request.user).order_by('timestamp')

    return render(request, 'home.html', {'chat_history': chat_history})

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'register.html')


# health/views.py


from .models import HealthTip
from datetime import date


DAILY_TIPS = [
    "💧 Stay hydrated! Aim for at least 8 glasses of water today.",
    "🚶‍♀️ Take a 10-minute walk — it's good for your heart and mood!",
    "🥗 Eat a rainbow — add colorful veggies and fruits to your meal.",
    "🧘‍♂️ Take 5 deep breaths now. Relax your shoulders.",
    "😴 Sleep early tonight. Your body heals best during rest.",
    "📵 Take a break from screens for 30 minutes today.",
    "💚 Practice gratitude — write down one thing you’re thankful for."
]

def get_or_create_daily_tip():
    today = date.today()
    tip_obj = HealthTip.objects.filter(date=today).first()
    
    if not tip_obj:
        # Rotate tip using weekday (0 = Monday)
        index = today.weekday() % len(DAILY_TIPS)
        tip = DAILY_TIPS[index]
        tip_obj = HealthTip.objects.create(date=today, tip=tip)

    return tip_obj


from datetime import date, datetime
from django.shortcuts import render, redirect
from .models import HealthTip, MedicationReminder


def dashboard(request):
    tip_obj = get_or_create_daily_tip()
    daily_tip = tip_obj.tip

    if request.method == 'POST':
        if 'new_tip' in request.POST:
            new_tip = request.POST.get('new_tip')
            if new_tip:
                tip_obj.tip = new_tip
                tip_obj.save()

        elif 'medication' in request.POST:
            message = request.POST.get('medication')
            time_str = request.POST.get('time')
            time = datetime.strptime(time_str, '%H:%M').time() if time_str else None

            MedicationReminder.objects.create(
                user=request.user,
                message=message,
                time=time
            )

        elif 'remove' in request.POST:
            reminder_id = request.POST.get('remove')
            MedicationReminder.objects.filter(id=reminder_id, user=request.user).delete()

        return redirect('dashboard')  # Always refresh after a POST

    reminders_qs = MedicationReminder.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'dashboard.html', {
        'daily_tip': daily_tip,
        'reminders': reminders_qs,
    })

