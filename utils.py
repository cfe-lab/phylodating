import subprocess
import os
from pathlib import Path
from .models import Job
import time
import sys
import logging

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
        self.warnings = []
        self.update_output_paths()
        self.update_status('R')
        self.jobs = {
            'root_and_regress': self.root_and_regress(),
            'plot_divergence': self.plot()
        }
        self.update()

    def update_status(self, status):
        self.status = status
        self.job_model.status = self.status
        self.job_model.save()

    def update(self):
        stdout = []
        stderr = []
        cmds = []
        job_failed = False
        for name, completed in self.jobs.items():
            if completed is None:
                continue
            stdout.append(f'{name}: {completed.stdout}')
            stderr.append(f'{name}: {completed.stderr}')
            cmds.append(' '.join([str(x) for x in completed.args]))
            if 'error' in completed.stderr.lower():
                self.errors.append(completed.stderr)
                if name == 'root_and_regress':
                    job_failed = True
                elif name == 'plot_divergence':
                    self.warnings.append('Divergence plot could not be created')
            if 'Linear model did not fit' in completed.stderr:
                self.warnings.append('No evidence of a molecular clock was found in the data.  Please see information in “stats.csv”.  For this reason, the divergence vs. time plot was not created for these data.')
        if job_failed:
            self.status = 'F'
        else:
            self.status = 'S'
        self.job_model.status = self.status
        self.job_model.stdout = '\n'.join(stdout)
        self.job_model.stderr = '\n'.join(stderr)
        if self.warnings:
            self.job_model.warnings = '\n'.join(self.warnings)
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
        self.job_model.plot.name = os.path.join(root, 'divergence_vs_time.png')
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
