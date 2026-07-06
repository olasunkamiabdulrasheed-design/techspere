# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication


def job_list(request):
    job_type = request.GET.get('type', '')
    jobs = Job.objects.filter(is_active=True)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'selected_type': job_type,
        'job_types': Job.JOB_TYPES,
    })


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    already_applied = False
    if request.user.is_authenticated:
        already_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'already_applied': already_applied})


@login_required
def job_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        apply_link = request.POST.get('apply_link')
        if title and company and description:
            Job.objects.create(
                poster=request.user,
                title=title,
                company=company,
                location=location,
                job_type=job_type,
                description=description,
                requirements=requirements,
                apply_link=apply_link
            )
            return redirect('job_list')
    return render(request, 'jobs/job_create.html')


@login_required
def job_apply(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter')
        JobApplication.objects.get_or_create(
            job=job,
            applicant=request.user,
            defaults={'cover_letter': cover_letter}
        )
    return redirect('job_detail', pk=job.pk)