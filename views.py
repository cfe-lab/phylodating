import os
from datetime import datetime
from zipfile import ZipFile
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Job
from .forms import JobForm
from .utils import JobProcess
from .version import VERSION
from django.core import management
import subprocess

ROOT = '/alldata/bblab_site'


def index(request):
    form = JobForm()
    version = VERSION
    return render(
        request,
        'jobs/index.html',
        {
            'form': form,
            'version': version
        }
    )


def results(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            new_job = form.save()
            # This is to call the command via code
            # management.call_command('submit_job', new_job.id)
            subprocess.Popen(['/usr/local/bin/python3.7', os.path.join(ROOT, 'manage.py'), 'submit_job', str(new_job.id)])
            return redirect(new_job)
        else:
            return HttpResponse(f'Form is invalid: {form.errors}')
    else:
        form = JobForm()
    return render(request, 'jobs/index.html', {'form': form})


def details(request, job_id):
    job = Job.objects.get(job_id=job_id)
    readable_status = job.my_choices_dict[job.status]
    alert_suffix = job.bootstrap_alerts[job.status]
    context = {
        'job': job,
        'status': readable_status,
        'alert_suffix': alert_suffix
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
        z.write(job.plot.path, os.path.basename(job.plot.path))
    return response


def download_sample(request):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    sample_path = os.path.join(current_dir, 'static', 'sample.zip')
    zip_file = open(sample_path, 'rb')
    response = FileResponse(zip_file, as_attachment=True)#filename='phylodating_sample_data.zip')
    return response