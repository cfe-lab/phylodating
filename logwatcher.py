import yaml
import os
from pathlib import Path

from mailer import send_sfu_email


class Logwatcher:


    def __init__(self):
        self.cwd = Path(os.path.realpath(__file__)).parent
        self.watched_logs_file =  self.cwd / 'watched_logs.yaml'
        self.watched_logs = self.load_yaml(self.watched_logs_file)
        self.log_details_file = self.cwd / '.log_details.yaml'
        if not os.path.isfile(self.log_details_file):
            self.log_details_file.touch()
            self.log_details = {}
        else:
            self.log_details = self.load_yaml(self.log_details_file) or {}
        self.update_log_details()


    def load_yaml(self, yaml_file):
        with open(yaml_file) as f:
            return yaml.load(f, Loader=yaml.FullLoader)


    def save_yaml(self, yaml_file, data):
        with open(yaml_file, 'w') as o:
            return yaml.dump(data, o)


    def update_log_details(self):
        changed_logs = []
        # Logic is, for every watched logfile:
            # get the size of the file
            # compare it against the previous size
            # If the size has changed send an email to the admin
        for name, logfile in self.watched_logs.items():
            print(f'Checking "{logfile}"')
            size = os.path.getsize(logfile)
            if name in self.log_details:
                if self.log_details[name] != size:
                    changed_logs.append(logfile)
            self.log_details[name] = size
        # Update log_details_file
        self.save_yaml(self.log_details_file, self.log_details)
        # If changed_logs is not empty, send an email about them
        if changed_logs:
            print('logs have changed!')
            sender = 'Phylodating_Logwatcher'
            receiver = 'bblab-admin@bccfe.ca'
            subject = 'New Phylodating Errors Detected'
            body = 'Logwatcher has detected new errors in the following logfiles:\n\n{}'.format('\n'.join(changed_logs))
            returncode = send_sfu_email(
                sender, receiver, subject, body, attachment_list=-1, cc_list=-1
            )
            print(returncode)


def main():
    logwatcher = Logwatcher()


if __name__ == '__main__':
    main()