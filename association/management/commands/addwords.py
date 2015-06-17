from association.models import Language, Word
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Adds a list of words.'

    def add_arguments(self, parser):
        parser.add_argument('language_code', type=str)
        parser.add_argument('word_list', type=str)

    def handle(self, *args, **options):
        try:
            language = Language.objects.get(code=options['language_code'].strip())
        except Language.DoesNotExist:
            self.stdout.write('Language code does not exist. Abborting...')
            return

        f = open(options['word_list'], 'r')
        for line in f:
            word, created = Word.objects.get_or_create(name=line.strip())
            word.languages.add(language)
            word.save()
        f.close()
        self.stdout.write('Successfully added new words.')