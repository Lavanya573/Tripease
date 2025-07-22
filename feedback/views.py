from django.shortcuts import render
from django.http import HttpResponse
from .models import Feedback

# Create your views here.

# List all feedback
def feedback_list(request):
    feedbacks = Feedback.objects.select_related('user', 'room').all()
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks})

# Show feedback detail
def feedback_detail(request, feedback_id):
    return HttpResponse(f'Feedback detail for {feedback_id} (to be implemented)')

# Submit feedback
def submit_feedback(request):
    return HttpResponse('Submit feedback (to be implemented)')
