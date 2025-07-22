from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatSession
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django import forms
from django.shortcuts import render, get_object_or_404
from .models import ChatSession, ChatMessage  # use your model names

# Create your views here.

@login_required
def start_chat(request):
    # Find or create an active chat session for this user
    session, created = ChatSession.objects.get_or_create(user=request.user, is_active=True)
    return redirect('chat_session', session_id=session.id)


# @login_required
@login_required
def chat_session(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id)

    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            ChatMessage.objects.create(
                session=session,
                sender=request.user,
                message=content
            )
            return redirect('chat_session', session_id=session.id)

    messages = ChatMessage.objects.filter(session=session)

    return render(request, 'chat/chat_session.html', {
        'session': session,
        'messages': messages
    })



# def chat_session(request, session_id):
#     from .models import ChatSession
#     session = None
#     if request.user.is_staff:
#         session = ChatSession.objects.get(pk=session_id)
#         # Assign the agent if not already assigned
#         if session.agent is None:
#             session.agent = request.user
#             session.save()
#     else:
#         session = ChatSession.objects.get(pk=session_id, user=request.user)
#     return render(request, 'chat/chat_session.html', {'session': session})

@staff_member_required
def admin_dashboard(request):
    active_sessions = ChatSession.objects.filter(is_active=True).select_related('user', 'agent')
    if not active_sessions.exists():
        # Optionally, redirect to a help page or just render the dashboard with a message
        # return redirect('some_help_page')
        # For now, just render the dashboard (template now shows a message)
        pass
    return render(request, 'chat/admin_dashboard.html', {'active_sessions': active_sessions})

@csrf_exempt
@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        from .models import ChatMessage
        msg = ChatMessage(file=file, sender=request.user, message_type='file')
        msg.save()
        return JsonResponse({'file_url': msg.file.url})
    return JsonResponse({'error': 'No file uploaded'}, status=400)

class FeedbackForm(forms.Form):
    rating = forms.ChoiceField(choices=[(5, 'Excellent'), (4, 'Good'), (3, 'Average'), (2, 'Poor'), (1, 'Terrible')], widget=forms.RadioSelect)
    comments = forms.CharField(widget=forms.Textarea, required=False)

@login_required
def chat_feedback(request, session_id):
    session = ChatSession.objects.get(pk=session_id, user=request.user)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Save feedback to session or a new model if needed
            session.is_active = False
            session.save()
            # Optionally store feedback in a new model
            return render(request, 'chat/feedback_thanks.html')
    else:
        form = FeedbackForm()
    return render(request, 'chat/feedback.html', {'form': form, 'session': session})

