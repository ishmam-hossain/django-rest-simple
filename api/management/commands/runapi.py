from django.core.management.base import BaseCommand

from subprocess import Popen
from sys import stdout, stdin, stderr
import time


class Command(BaseCommand):
    help = 'Single command app start'
    commands = [
        'pip install -r requirements.txt',
        'redis-server',
        'python manage.py makemigrations',
        'python manage.py migrate',
        'python manage.py runserver',

    ]

    def handle(self, *args, **options):
        process_list = []

        for command in self.commands:
            self.stdout.write(self.style.SUCCESS(f"#executing --> {command}"))
            process = Popen(command, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)
            process.wait()
            process_list.append(process)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            for process in process_list:
                process.kill()

