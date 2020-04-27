from django.core.management.base import BaseCommand, CommandError
from phylodating.models import Job
from phylodating.utils import JobProcess

class Command(BaseCommand):
    help = 'Submits the job'

    def add_arguments(self, parser):
        parser.add_argument('job_id', type=int)

    def handle(self, *args, **options):
        try:
            job = Job.objects.get(pk=options['job_id'])
            process = JobProcess(job)
        except Job.DoesNotExist:
            raise CommandError('Job "%s" does not exist' % options['job_id'])

        self.stdout.write(self.style.SUCCESS('Successfully closed job "%s"' % options['job_id']))