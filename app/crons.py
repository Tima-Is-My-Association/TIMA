# -*- coding: utf-8 -*-

from app.models import Newsletter
from django.core.mail import send_mass_mail
from django.utils import timezone
from django_cron import CronJobBase, Schedule

class NewsletterCronJob(CronJobBase):
    RUN_AT_TIMES = ['0:00']
    MIN_NUM_FAILURES = 3

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'app.newsletter_cron_job'

    def do(self):
        if not timezone.now().weekday() == 5:
            return

        messages = []
        for newsletter in Newsletter.objects.all():
            user = newsletter.user
            if user.email:
                message = 'Greetings 👋 %s!\n\nThis is the weekly TIMA newsletter with information about your selected words.\n\n' % user.username
                for word in newsletter.words.all():
                    s = ' * %s\n  - top 10 associations (%s -> *):\n      %s\n  - top 10 occurrences as association (* -> %s):\n      %s' % (word, word, '\n      '.join(['%s (%s)' % (a.association, a.count) for a in word.word.all().order_by('-count')[:10]]), word, '\n      '.join(['%s (%s)' % (a.word, a.count) for a in word.association.all().order_by('-count')[:10]]))
                    message += '%s\n\n' % s
                message += 'Thank you,\nyour TIMA team.'
                messages.append(('[TIMA] Weekly words newsletter', message, 'tima@jnphilipp.org', [newsletter.user.email]))

        send_mass_mail(messages)
