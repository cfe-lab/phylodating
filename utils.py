import subprocess
import os
from pathlib import Path
from .models import Job
import time

SCRIPTS = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'scripts'
)

ROOT_AND_REGRESS = os.path.join(
    SCRIPTS,
    'root_and_regress.R'
)

PLOT = os.path.join(
    SCRIPTS,
    'plot_divergence_vs_time.R'
)


class JobProcess:


    def __init__(self, job_model):
        self.job_model = job_model
        self.status = 'N'
        self.errors = []
        self.update_output_paths()
        self.jobs = {
            'root_and_regress': self.root_and_regress(),
            'plot_divergence': self.plot()
        }
        self.update_status()


    def update_status(self):
        stdout = []
        stderr = []
        cmds = []
        for name, completed in self.jobs.items():
            if completed is None:
                continue
            stdout.append(f'{name}: {completed.stdout}')
            stderr.append(f'{name}: {completed.stderr}')
            cmds.append(' '.join(completed.args))
            if 'error' in completed.stderr.lower():
                self.errors.append(completed.stderr)
        if self.errors:
            self.status = 'F'
        else:
            self.status = 'S'
        self.job_model.status = self.status
        self.job_model.stdout = '\n'.join(stdout)
        self.job_model.stderr = '\n'.join(stderr)
        self.cmd = '\n'.join(cmds)
        self.job_model.save()


    def update_output_paths(self):
        root = os.path.join(
            os.path.dirname(
                os.path.dirname(self.job_model.info_csv.path)
            ),
            'outputs'
        )
        if not os.path.exists(root):
            os.mkdir(root)
        self.job_model.rooted_tree_out.name = os.path.join(root, 'rooted_tree.nwk')
        self.job_model.data_out.name = os.path.join(root, 'data.csv')
        self.job_model.stats_out.name = os.path.join(root, 'stats.csv')
        self.job_model.save()


    def spawn(self, cmd):
        try:
            completed_process = subprocess.run(
                cmd,
                capture_output=True,
                check=True,
                encoding='utf-8'
            )
        except subprocess.CalledProcessError as e:
            self.errors.append(e.stderr)
            return e
        return completed_process


    def root_and_regress(self):
        cmd = [
            'Rscript',
            ROOT_AND_REGRESS,
            f'--runid={self.job_model.job_id}',
            f'--tree={self.job_model.unrooted_tree.path}',
            f'--info={self.job_model.info_csv.path}',
            f'--rootedtree={self.job_model.rooted_tree_out.path}',
            f'--data={self.job_model.data_out.path}',
            f'--stats={self.job_model.stats_out.path}'
        ]
        return self.spawn(cmd)


    def plot(self):
        self.plot_prefix = os.path.join(
            os.path.dirname(self.job_model.stats_out.path),
            'divergence_vs_time'
        )
        cmd = [
            'Rscript',
            PLOT,
            f'--info={self.job_model.info_csv.path}',
            f'--rootedtree={self.job_model.rooted_tree_out.path}',
            f'--stats={self.job_model.stats_out.path}',
            f'--plotprefix={self.plot_prefix}'
        ]
        return self.spawn(cmd)
