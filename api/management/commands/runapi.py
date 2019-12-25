from django.core.management.base import BaseCommand

from subprocess import Popen
from sys import stdout, stdin, stderr
import time
import os
import signal


class Command(BaseCommand):
    help = 'Single command app start'
    commands = [
        'python manage.py makemigrations',
        'python manage.py migrate',
        'redis-server',
        'python manage.py runserver',

    ]

    def handle(self, *args, **options):
        process_list = []

        for command in self.commands:
            self.stdout.write(self.style.SUCCESS(f"executing# {command}"))
            process = Popen(command, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)
            process_list.append(process)

        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            for process in process_list:
                os.kill(process.pid, signal.SIGKILL)
