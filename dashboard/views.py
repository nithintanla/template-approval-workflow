from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Template, Brand, Analytics, Agent
from .forms import TemplateForm
from .services import TemplateApprovalService
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import json

@login_required
def dashboard(request):
    templates = Template.objects.all()
    brands = Brand.objects.all()
    context = {
        'templates': templates,
        'brands': brands,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def create_template(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.created_by = request.user
            template.status = 'pending'
            template.save()
            
            # Check template approval
            approved, message = TemplateApprovalService.check_approval(template.content)
            if approved:
                template.status = 'approved'
            else:
                template.status = 'rejected'
            template.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Template submitted for approval',
                'approval_status': template.status,
                'approval_message': message
            })
    else:
        form = TemplateForm()
    return render(request, 'dashboard/create_template.html', {'form': form})

@login_required
def template_list(request):
    templates = Template.objects.all()
    return render(request, 'dashboard/template_list.html', {'templates': templates})

@login_required
def analytics(request):
    # Get data for the last 7 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    
    # Get analytics data
    analytics_data = Analytics.objects.filter(
        date__range=[start_date, end_date]
    ).select_related('template')

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(list(analytics_data.values('date', 'views', 'responses', 'template__title')))
    
    # Create views trend chart
    views_fig = px.line(df, x='date', y='views', 
                        title='Template Views Over Time',
                        labels={'date': 'Date', 'views': 'Number of Views'})
    views_chart = views_fig.to_html(full_html=False)

    # Create response rate chart
    df['response_rate'] = (df['responses'] / df['views'] * 100).round(2)
    response_fig = px.bar(df, x='template__title', y='response_rate',
                         title='Template Response Rates',
                         labels={'template__title': 'Template', 'response_rate': 'Response Rate (%)'})
    response_chart = response_fig.to_html(full_html=False)

    # Get agent performance data
    agents = Agent.objects.select_related('brand').all()
    agent_stats = []
    for agent in agents:
        templates_count = Template.objects.filter(brand=agent.brand).count()
        agent_stats.append({
            'name': agent.name,
            'brand': agent.brand.name,
            'templates': templates_count,
            'active': '✓' if agent.is_active else '✗'
        })

    context = {
        'views_chart': views_chart,
        'response_chart': response_chart,
        'agent_stats': agent_stats
    }
    return render(request, 'dashboard/analytics.html', context)

@login_required
def approval_settings(request):
    settings = ApprovalSettings.objects.latest('created_at') if ApprovalSettings.objects.exists() else None
    
    if request.method == 'POST':
        keywords = request.POST.get('rejection_keywords', '')
        if settings:
            settings.rejection_keywords = keywords
            settings.save()
        else:
            settings = ApprovalSettings.objects.create(rejection_keywords=keywords)
        messages.success(request, 'Approval settings updated successfully.')
        return redirect('approval_settings')
        
    return render(request, 'dashboard/approval_settings.html', {'settings': settings})

@login_required
def review_templates(request):
    templates = Template.objects.filter(status='rejected')
    return render(request, 'dashboard/review_templates.html', {'templates': templates})

@login_required
def update_template_status(request, template_id):
    if request.method == 'POST':
        template = Template.objects.get(id=template_id)
        new_status = request.POST.get('status')
        if new_status in ['approved', 'rejected']:
            template.status = new_status
            template.save()
            messages.success(request, f'Template {new_status} successfully.')
    return redirect('review_templates')
