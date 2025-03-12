from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from dashboard.models import Template

@login_required
def review_templates(request):
    templates = Template.objects.filter(status='pending')  # Filter templates with status 'pending'
    return render(request, 'approver/review_templates.html', {'templates': templates})

@login_required
def update_template_status(request, template_id):
    if request.method == 'POST':
        template = Template.objects.get(id=template_id)
        new_status = request.POST.get('status')
        if new_status in ['approved', 'rejected']:
            template.status = new_status
            template.save()
            return JsonResponse({'message': f'Template {new_status} successfully.', 'status': 'success'})
        return JsonResponse({'message': 'Invalid status.', 'status': 'error'})
    return JsonResponse({'message': 'Invalid request method.', 'status': 'error'})
