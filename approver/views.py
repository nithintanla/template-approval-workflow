from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from dashboard.models import Template

@login_required
def review_templates(request):
    if request.user.username == 'l1approver':
        templates = Template.objects.filter(status='pending').order_by('-created_at')
    elif request.user.username == 'l2approver':
        templates = Template.objects.filter(status='approved_l1').order_by('-created_at')
    else:
        templates = Template.objects.none()  # No access for other users
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

@login_required
def approve_l1(request, template_id):
    if request.method == 'POST':
        template = get_object_or_404(Template, id=template_id)
        new_status = request.POST.get('status')
        if new_status == 'approved_l1':
            template.status = 'approved_l1'
            template.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Template has been approved by L1 and sent for L2 approval',
                'template_id': template_id
            })
        elif new_status == 'rejected_l1':
            template.status = 'rejected_l1'
            template.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Template has been rejected by L1',
                'template_id': template_id
            })
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid status for L1 approval'
        })
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def approve_l2(request, template_id):
    if request.method == 'POST':
        template = get_object_or_404(Template, id=template_id)
        if template.status == 'approved_l1':
            new_status = request.POST.get('status')
            if new_status == 'approved_l2':
                template.status = 'approved_l2'
                template.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Template has been approved by L2',
                    'template_id': template_id
                })
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid status for L2 approval'
            })
        return JsonResponse({
            'status': 'error',
            'message': 'Template must be approved by L1 first'
        })
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
