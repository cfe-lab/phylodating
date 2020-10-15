from django.db import models
from django.urls import reverse
import secrets

# Create your models here.

def generate_job_id():
    return secrets.randbits(24)

def upload_callback_info_csv(instance, filename):
    return '/'.join(('uploads', str(instance.job_id), 'inputs', 'info.csv'))

def upload_callback_unrooted_tree(instance, filename):
    return '/'.join(('uploads', str(instance.job_id), 'inputs', 'unrooted_tree.nwk'))

def upload_callback_rooted_tree(instance, filename):
    return '/'.join(('uploads', str(instance.job_id), 'outputs', 'rooted_tree.nwk'))

def upload_callback_data_file(instance, filename):
    return '/'.join(('uploads', str(instance.job_id), 'outputs', 'data.csv'))

def upload_callback_stats_file(instance, filename):
    return '/'.join(('uploads', str(instance.job_id), 'outputs', 'stats.csv'))

def upload_callback_plot_file(instance, filename):
    return '/'.join(('uploads', str(instance.job_id), 'outputs', 'divergence_vs_time.png'))

class Job(models.Model):

    email = models.CharField(
        max_length=200,
        blank=True
    )

    job_id = models.IntegerField(
        default=generate_job_id
    )

    info_csv = models.FileField(
        upload_to=upload_callback_info_csv
    )

    unrooted_tree = models.FileField(
        upload_to=upload_callback_unrooted_tree
    )

    rooted_tree_out = models.FileField(
        upload_to=upload_callback_rooted_tree
    )

    data_out = models.FileField(
        upload_to=upload_callback_data_file
    )

    stats_out = models.FileField(
        upload_to=upload_callback_stats_file
    )

    plot = models.ImageField(
        upload_to=upload_callback_plot_file
    )

    created_at = models.DateTimeField(auto_now_add=True)

    my_choices_dict = {
        'N': 'Not Run',
        'R': 'Running',
        'S': 'Successful',
        'F': 'Failed',
        'K': 'Killed'
    }

    my_choices = [
        (k, v) for k,v in my_choices_dict.items()
    ]

    bootstrap_alerts = {
        'N': 'secondary',
        'R': 'info',
        'S': 'success',
        'F': 'danger',
        'K': 'danger'
    }

    status = models.CharField(
        max_length = 1,
        choices=my_choices,
        default='N'
    )

    stdout = models.TextField()

    stderr = models.TextField()

    warnings = models.TextField(
        default=None,
        blank=True,
        null=True
    )

    cmd = models.TextField(
        blank=True
    )

    def get_absolute_url(self):
        return reverse('phylodating:details', kwargs=dict(job_id=self.job_id))
