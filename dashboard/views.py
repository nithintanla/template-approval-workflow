from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse  # Add this import
from .models import Template, Brand, Agent, ApprovalSettings
from .forms import TemplateForm, BrandForm, AgentForm
from .services import TemplateApprovalService, TemplateModeration
from datetime import datetime, timedelta
import json

@login_required
def dashboard(request):
    templates = Template.objects.all()
    brands = Brand.objects.all()
    agents = Agent.objects.all()
    
    # Add counts for different template statuses
    pending_count = templates.filter(status='pending_l1').count()
    approved_l1_count = templates.filter(status='approved_l1').count()
    approved_l2_count = templates.filter(status='approved_l2').count()
    rejected_l1_count = templates.filter(status='rejected_l1').count()
    rejected_l2_count = templates.filter(status='rejected_l2').count()
    
    context = {
        'templates': templates,
        'brands': brands,
        'agents': agents,
        'pending_count': pending_count,
        'approved_l1_count': approved_l1_count,
        'approved_l2_count': approved_l2_count,
        'rejected_l1_count': rejected_l1_count,
        'rejected_l2_count': rejected_l2_count,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def create_template(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.created_by = request.user
            template.status = 'pending_l1'  # Set initial status for L1 approval
            template.save()
            messages.success(request, 'Template created and sent for L1 approval.')
            return redirect('template_list')
    else:
        form = TemplateForm()
    return render(request, 'dashboard/create_template.html', {'form': form})

@login_required
def template_list(request):
    # Get filter parameters
    brand = request.GET.get('brand')
    message_type = request.GET.get('message_type')
    status = request.GET.get('status')
    date = request.GET.get('date')
    stage = request.GET.get('stage')
    aggregator = request.GET.get('aggregator')

    # Base queryset
    templates = Template.objects.all()

    # Apply filters
    if brand:
        templates = templates.filter(brand_id=brand)
    if message_type:
        templates = templates.filter(message_type=message_type)
    if status:
        templates = templates.filter(status=status)
    if date:
        templates = templates.filter(created_at__date=date)
    if stage:
        templates = templates.filter(stage=stage)
    if aggregator:
        templates = templates.filter(aggregator=aggregator)

    template_filters = [
        {
            'name': 'message_type',
            'label': 'Message Type',
            'selected': message_type,
            'options': [
                {'value': 'text', 'label': 'Text'},
                {'value': 'media', 'label': 'Media'},
                {'value': 'card', 'label': 'Card'},
            ]
        },
        {
            'name': 'stage',
            'label': 'Stage',
            'selected': stage,
            'options': [
                {'value': 'all', 'label': 'All'},
                {'value': 'creation', 'label': 'Creation'},
                {'value': 'review', 'label': 'Review'},
            ]
        },
        {
            'name': 'status',
            'label': 'Status',
            'selected': status,
            'options': [
                {'value': opt[0], 'label': opt[1]} 
                for opt in Template.STATUS_CHOICES
            ]
        },
        {
            'name': 'brand',
            'label': 'Brand',
            'selected': brand,
            'options': [
                {'value': b.id, 'label': b.name} 
                for b in Brand.objects.all()
            ]
        },
        {
            'name': 'aggregator',
            'label': 'Aggregator',
            'selected': aggregator,
            'options': [
                {'value': 'all', 'label': 'All'},
                # Add your aggregator options here
            ]
        }
    ]

    context = {
        'templates': templates,
        'template_filters': template_filters,
        'total_count': Template.objects.count(),
        'pending_count': Template.objects.filter(status='pending').count(),
    }

    return render(request, 'dashboard/template_list.html', context)

@login_required
def approval_settings(request):
    settings = ApprovalSettings.objects.latest('created_at') if ApprovalSettings.objects.exists() else None
    if request.method == 'POST':
        rejection_keywords = request.POST.get('rejection_keywords', '')
        keywords_approve = request.POST.get('keywords_approve', '')
        keywords_manual = request.POST.get('keywords_manual', '')
        if settings:
            settings.rejection_keywords = rejection_keywords
            settings.keywords_approve = keywords_approve
            settings.keywords_manual = keywords_manual
            settings.save()
        else:
            settings = ApprovalSettings.objects.create(
                rejection_keywords=rejection_keywords,
                keywords_approve=keywords_approve,
                keywords_manual=keywords_manual
            )
        messages.success(request, 'Approval settings updated successfully.')
        return redirect('approval_settings')
    return render(request, 'dashboard/approval_settings.html', {'settings': settings})

@login_required
def review_templates(request):
    templates = Template.objects.filter(status__in=['rejected_system', 'rejected_admin'])
    return render(request, 'dashboard/review_templates.html', {'templates': templates})

@login_required
def update_template_status(request, template_id):
    if request.method == 'POST':
        template = Template.objects.get(id=template_id)
        new_status = request.POST.get('status')
        if new_status in ['approved_admin', 'rejected_admin']:
            template.status = new_status
            template.save()
            messages.success(request, f'Template {new_status.replace("_", " ")} successfully.')
    return redirect('review_templates')

@login_required
def brand_list(request):
    # Get filter parameters
    search = request.GET.get('search', '')
    date_from = request.GET.get('date_from')

    # Base queryset
    brands = Brand.objects.all()

    # Apply filters
    if search:
        brands = brands.filter(name__icontains=search)
    if date_from:
        brands = brands.filter(created_at__date=date_from)

    context = {
        'brands': brands,
        'selected_date_from': date_from,
    }
    return render(request, 'dashboard/brand_list.html', context)

@login_required
def create_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand created successfully.')
            return redirect('brand_list')
    else:
        form = BrandForm()
    return render(request, 'dashboard/create_brand.html', {'form': form})

@login_required
def agent_list(request):
    agents = Agent.objects.all()
    brands = Brand.objects.all()
    
    # Handle filters
    selected_brand = request.GET.get('brand')
    selected_status = request.GET.get('status')
    selected_date = request.GET.get('date')

    if selected_brand:
        agents = agents.filter(brand_id=selected_brand)
    if selected_status:
        is_active = selected_status == 'active'
        agents = agents.filter(is_active=is_active)
    if selected_date:
        agents = agents.filter(created_at__date=selected_date)

    context = {
        'agents': agents,
        'brands': brands,
        'selected_brand': selected_brand,
        'selected_status': selected_status,
        'selected_date': selected_date,
    }
    return render(request, 'dashboard/agent_list.html', context)

@login_required
def create_agent(request):
    if request.method == 'POST':
        form = AgentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agent created successfully.')
            return redirect('agent_list')
    else:
        form = AgentForm()
    return render(request, 'dashboard/create_agent.html', {'form': form})

@login_required
def edit_agent(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    
    if request.method == 'POST':
        form = AgentForm(request.POST, instance=agent)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agent updated successfully.')
            return redirect('agent_list')
    else:
        form = AgentForm(instance=agent)
    
    return render(request, 'dashboard/edit_agent.html', {
        'form': form,
        'agent': agent
    })

@login_required
def delete_agent(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    if request.method == 'POST':
        agent.delete()
        messages.success(request, 'Agent deleted successfully.')
        return redirect('agent_list')
    return render(request, 'dashboard/delete_agent.html', {'agent': agent})

def send_template_to_admin_for_approval(template):
    # Logic to send the template to the admin app for approval
    pass

@login_required
def profile(request):
    return render(request, 'dashboard/profile.html', {'user': request.user})

@login_required
def edit_template(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    
    if request.method == 'POST':
        form = TemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, 'Template updated successfully.')
            return redirect('template_list')
    else:
        form = TemplateForm(instance=template)
    
    return render(request, 'dashboard/edit_template.html', {
        'form': form,
        'template': template
    })

@login_required
def edit_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand updated successfully.')
            return redirect('brand_list')
    else:
        form = BrandForm(instance=brand)
    
    return render(request, 'dashboard/edit_brand.html', {
        'form': form,
        'brand': brand
    })
