from applications.models import Application
from django.contrib.auth import authenticate
from django.core.management.base import BaseCommand
from getpass import getpass

class Command(BaseCommand):
    help = 'Adds a list of words.'

    def add_arguments(self, parser):
        parser.add_argument('application', type=str)

    def handle(self, *args, **options):
        username = input('username: ')
        password = getpass('password: ')
        user = authenticate(username=username, password=password)
        if user:
            if not user.is_staff:
                self.stdout.write("you're not an admin.")
                return

            try:
                application = Application.objects.get(name=options['application'].strip())
                application.generate_tokens()
                application.save()
                self.stdout.write('new client_id: "%s"' % application.client_id)
                self.stdout.write('new secret: "%s"' % application.secret)
            except Application.DoesNotExist:
                self.stdout.write('application with name "%s" not found.' % options['application'].strip())
        else:
            self.stdout.write('enter a correct username and password to authenticate.')
