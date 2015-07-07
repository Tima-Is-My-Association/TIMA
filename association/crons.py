from association.functions.oai_pmh import generate_metadata
from django.core.mail import mail_admins
from django_cron import CronJobBase, Schedule

class UpdateMetadataCronJob(CronJobBase):
    RUN_AT_TIMES = ['0:00']
    MIN_NUM_FAILURES = 3

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'association.update_metadata_cron_job'

    def do(self):
        statistics = generate_metadata()
        message = 'Hi.\n\nThe OAI PMH deliviers:\n\n * sets: %s of which %s where just added\n * headers: %s of which %s where just added and %s are deleted\n\nTIMA' % (statistics['sets']['all'], statistics['sets']['new'], statistics['headers']['all'], statistics['headers']['new'], statistics['headers']['deleted'])
        mail_admins('Update Metadata', message)
