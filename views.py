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
from pathlib import Path
import logging
from django.urls import reverse

ROOT = Path(os.path.realpath(__file__)).parent.parent.parent

from .mailer import send_sfu_email

def read_markdown(md):
    with open(md) as f:
        return f.read()

def index(request):
    cwd = Path(os.path.dirname(os.path.realpath(__file__)))
    info_csv_help_md = cwd / 'docs' / 'info_csv_help.md'
    phylodating_help_md = cwd / 'docs' / 'phylodating_help.md'
    unrooted_tree_help_md = cwd / 'docs' / 'unrooted_tree_help.md'
    rooted_tree_help_md = cwd / 'docs' / 'rooted_tree_help.md'
    stats_csv_help_md = cwd / 'docs' / 'stats_csv_help.md'
    data_csv_help_md = cwd / 'docs' / 'data_csv_help.md'
    divergence_vs_time_help_md = cwd / 'docs' / 'divergence_vs_time_help.md'

    info_csv_help_md = read_markdown(info_csv_help_md)
    phylodating_help_md = read_markdown(phylodating_help_md)
    unrooted_tree_help_md = read_markdown(unrooted_tree_help_md)
    rooted_tree_help_md = read_markdown(rooted_tree_help_md)
    stats_csv_help_md = read_markdown(stats_csv_help_md)
    data_csv_help_md = read_markdown(data_csv_help_md)
    divergence_vs_time_help_md = read_markdown(divergence_vs_time_help_md)
    form = JobForm()
    version = VERSION
    return render(
        request,
        'jobs/index.html',
        {
            'form': form,
            'version': version,
            'info_csv_help': info_csv_help_md,
            'phylodating_help': phylodating_help_md,
            'unrooted_tree_help': unrooted_tree_help_md,
            'rooted_tree_help': rooted_tree_help_md,
            'stats_csv_help': stats_csv_help_md,
            'data_csv_help': data_csv_help_md,
            'divergence_vs_time_help': divergence_vs_time_help_md,
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
            sender = 'BCCFE Phylodating'
            subject = 'Your phylodating job'
            url = request.build_absolute_uri(reverse('phylodating:details', args=[new_job.job_id]))
            body = f'Hi there, you recently submitted a job using the BCCFE Phylodating webtool. To check the status of your job and/or download the results please use the following URL:\n\n{url}'
            if new_job.email:
                send_sfu_email(
                    sender, new_job.email, subject, body, attachment_list=-1, cc_list=-1
                )
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
    response = HttpResponse(content_type='application/zip')
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