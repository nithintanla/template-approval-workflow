from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Template, Brand, Agent, ApprovalSettings
from .forms import TemplateForm, BrandForm, AgentForm
from .services import TemplateApprovalService
from datetime import datetime, timedelta
import json

@login_required
def dashboard(request):
    templates = Template.objects.all()
    brands = Brand.objects.all()
    agents = Agent.objects.all()
    context = {
        'templates': templates,
        'brands': brands,
        'agents': agents,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def create_template(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.created_by = request.user
            
            # Check template content against keywords
            status, message = TemplateApprovalService.check_approval(template.content)
            template.status = status
            template.save()
            
            messages.success(request, message)
            return redirect('template_list')
        else:
            messages.error(request, 'There was an error with your submission.')
    else:
        form = TemplateForm()
    return render(request, 'dashboard/create_template.html', {'form': form})

@login_required
def template_list(request):
    templates = Template.objects.all()
    return render(request, 'dashboard/template_list.html', {'templates': templates})

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
    brands = Brand.objects.all()
    return render(request, 'dashboard/brand_list.html', {'brands': brands})

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
    return render(request, 'dashboard/agent_list.html', {'agents': agents})

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

def send_template_to_admin_for_approval(template):
    # Logic to send the template to the admin app for approval
    pass
