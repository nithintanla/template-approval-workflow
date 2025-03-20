from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from dashboard.models import Template, Brand
from django.contrib import messages

@login_required
def review_templates(request):
    # Get filter parameters
    brand_id = request.GET.get('brand')
    message_type = request.GET.get('message_type')
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    # Base queryset
    if request.user.username == 'l1approver':
        templates = Template.objects.filter(status='pending_l1')
    elif request.user.username == 'l2approver':
        templates = Template.objects.filter(status='approved_l1')
    else:
        templates = Template.objects.none()

    # Apply filters
    if brand_id:
        templates = templates.filter(brand_id=brand_id)
    if message_type:
        templates = templates.filter(message_type=message_type)
    if status:
        templates = templates.filter(status=status)
    if date_from:
        templates = templates.filter(created_at__gte=date_from)
    if date_to:
        templates = templates.filter(created_at__lte=date_to)

    # Order by latest first
    templates = templates.order_by('-created_at')

    # Get counts for stats
    context = {
        'templates': templates,
        'brands': Brand.objects.all(),
        'status_choices': Template.STATUS_CHOICES,
        'pending_count': Template.objects.filter(status='pending_l1').count(),
        'approved_count': Template.objects.filter(status__in=['approved_l1', 'approved_l2']).count(),
        'rejected_count': Template.objects.filter(status__in=['rejected_l1', 'rejected_l2']).count(),
        'total_count': Template.objects.count(),
        'selected_brand': brand_id,
        'selected_type': message_type,
        'selected_status': status,
        'selected_date_from': date_from,
        'selected_date_to': date_to,
    }

    return render(request, 'approver/review_templates.html', context)

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
    if request.method == 'POST' and request.user.username == 'l1approver':
        template = get_object_or_404(Template, id=template_id)
        action = request.POST.get('action')
        
        if action == 'approve':
            template.status = 'approved_l1'
            message = 'Template approved and sent for L2 review'
        elif action == 'reject':
            template.status = 'rejected_l1'
            message = 'Template rejected by L1'
        
        template.save()
        messages.success(request, message)
        return JsonResponse({'status': 'success', 'message': message})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def approve_l2(request, template_id):
    if request.method == 'POST' and request.user.username == 'l2approver':
        template = get_object_or_404(Template, id=template_id)
        action = request.POST.get('action')
        
        if action == 'approve':
            template.status = 'approved_l2'
            message = 'Template approved by L2'
        elif action == 'reject':
            template.status = 'rejected_l2'
            message = 'Template rejected by L2'
        
        template.save()
        messages.success(request, message)
        return JsonResponse({'status': 'success', 'message': message})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
