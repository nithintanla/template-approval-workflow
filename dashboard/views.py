from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Template, Brand
from .forms import TemplateForm
from .services import TemplateApprovalService

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
