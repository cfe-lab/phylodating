import os
from datetime import datetime
from zipfile import ZipFile
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Job
from .forms import JobForm
from .utils import JobProcess


def index(request):
    form = JobForm()
    return render(request, 'jobs/index.html', {'form': form})


def results(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            new_job = form.save()
            process = JobProcess(new_job)
            context = {
                'process': process
            }
            return redirect(new_job)
        else:
            return HttpResponse(f'Form is invalid: {form.errors}')
    else:
        form = JobForm()
    return render(request, 'jobs/index.html', {'form': form})


def details(request, job_id):
    job = Job.objects.get(job_id=job_id)
    context = {
        'job': job,
    }
    return render(request, 'jobs/details.html', context)


def download(request, job_id):
    job = Job.objects.get(job_id=job_id)
    context = {
        'job': job
    }
    response = HttpResponse(content_type='text/csv')
    today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    response['Content-Disposition'] = f'attachment; filename="phylodating_{job.job_id}_{today}.zip"'
    with ZipFile(response, 'w') as z:
        z.write(job.data_out.path, os.path.basename(job.data_out.path))
        z.write(job.rooted_tree_out.path, os.path.basename(job.rooted_tree_out.path))
        z.write(job.stats_out.path, os.path.basename(job.stats_out.path))
    return response