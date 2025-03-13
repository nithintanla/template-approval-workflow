from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from dashboard.models import Template

@login_required
def review_templates(request):
    # Only show templates with 'pending' status
    templates = Template.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'approver/review_templates.html', {'templates': templates})

@login_required
def update_template_status(request, template_id):
    if request.method == 'POST':
        template = get_object_or_404(Template, id=template_id)
        
        # Debug the incoming data
        print("POST data:", request.POST)  # Add this line to debug
        new_status = request.POST.get('status')
        print("Status received:", new_status)  # Add this line to debug
        
        # Check if status is in valid choices
        valid_statuses = ['approved_admin', 'rejected_admin']
        if new_status in valid_statuses:
            template.status = new_status
            template.save()
            
            return JsonResponse({
                'status': 'success',
                'message': f'Template has been {new_status.replace("_", " ")}',
                'template_id': template_id
            })
        
        return JsonResponse({
            'status': 'error', 
            'message': f'Invalid status: {new_status}. Must be one of {valid_statuses}'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
