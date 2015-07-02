from app.models import AssociationHistory, Profile
from association.models import Association, Language, Word
from csv import reader
from django.core.management.base import BaseCommand
from os.path import exists

class Command(BaseCommand):
    help = 'Adds a list of words.'

    def add_arguments(self, parser):
        parser.add_argument('-w', action='store', nargs=3, dest='w', type=str, help='word to merge: lang code, word1, word2')
        parser.add_argument('-f', action='store', dest='file', type=str, help='csv file with words to merge (each line: lang code;word1;word2)')

    def handle(self, *args, **options):
        if options['w']:
            self.stdout.write('%s' % options['w'])
            try:
                language = Language.objects.get(code=options['w'][0].strip())
            except Language.DoesNotExist:
                self.stdout.write('Language code does not exist. Abborting...')
                return

            try:
                word1 = Word.objects.get(name=options['w'][1].strip())
            except Word.DoesNotExist:
                self.stdout.write('Word1 does not exist. Abborting...')
                return

            try:
                word2 = Word.objects.get(name=options['w'][2].strip())
            except Word.DoesNotExist:
                self.stdout.write('Word2 does not exist. Abborting...')
                return
            self.merge_words(language, word1, word2)

        if options['file']:
            path = options['file']
            if not exists(path):
                self.stdout.write('File "%s" not found. Abborting...' % path)
            self.stdout.write('Loading file "%s".' % path)
            with open(path, 'r') as csvfile:
                csvreader = reader(csvfile, delimiter=';', quotechar='"')
                for line in csvreader:
                    try:
                        language = Language.objects.get(code=line[0].strip())
                    except Language.DoesNotExist:
                        self.stdout.write('Language code does not exist. Continuing...')
                        continue

                    try:
                        word1 = Word.objects.get(name=line[1].strip())
                    except Word.DoesNotExist:
                        self.stdout.write('Word1 does not exist. Continuing...')
                        continue

                    try:
                        word2 = Word.objects.get(name=line[2].strip())
                    except Word.DoesNotExist:
                        self.stdout.write('Word2 does not exist. Continuing...')
                        continue
                    self.merge_words(language, word1, word2)
                csvfile.close()
            self.stdout.write('File read complete.')

    def merge_words(self, language, word1, word2):
        self.stdout.write('Merging "%s" into "%s".' % (word2, word1))

        try:
            association = Association.objects.get(word=word1, association=word2)
            self.stdout.write('Found association "%s", removing it...' % association)

            for history in AssociationHistory.objects.filter(association=association):
                self.delete_history(history)
            association.delete()
        except Association.DoesNotExist:
            pass

        try:
            association = Association.objects.get(word=word2, association=word1)
            self.stdout.write('Found association "%s", removing it...' % association)

            for history in AssociationHistory.objects.filter(association=association):
                self.delete_history(history)
            association.delete()
        except Association.DoesNotExist:
            pass

        self.stdout.write('Merging associations of "%s" into "%s"' % (word2, word1))
        for association in Association.objects.filter(word=word2):
            self.stdout.write('Found association "%s", merging it...' % association)
            w1a, created = Association.objects.get_or_create(word=word1, association=association.association)

            if created:
                self.stdout.write('Created association "%s".' % w1a)
            w1a.count += (association.count - 1)
            w1a.save()
            association.delete()
        word2.delete()
        self.stdout.write('Merge of "%s" into "%s" complete.' % (word2, word1))

    def delete_history(self, history):
        self.stdout.write('Found association history "%s", removing it...' % history)
        profile = Profile.objects.get(user=history.user)
        profile.points -= history.points
        profile.save()
        history.delete()
