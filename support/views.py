from django.shortcuts import render
from django.http import HttpResponse
from .models import SupportTicket
from django.contrib.auth.decorators import login_required

# Create your views here.

# List support tickets
@login_required
def ticket_list(request):
    tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'support/ticket_list.html', {'tickets': tickets})

# Show ticket detail
def ticket_detail(request, ticket_id):
    return HttpResponse(f'Ticket detail for {ticket_id} (to be implemented)')

# Submit a support ticket
def submit_ticket(request):
    return HttpResponse('Submit support ticket (to be implemented)')
