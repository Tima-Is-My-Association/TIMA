from app.models import Profile, AssociationHistory
from association.models import Language, Word
from django.db.models import CharField, Q, Value as V
from django.db.models.functions import Concat
from oai_pmh.models import DCRecord, Header, MetadataFormat, Set

def generate_metadata():
    statistic = {'sets':{'new': 0, 'all': 0}, 'headers':{'all': 0, 'new': 0, 'deleted': 0}}
    for language in Language.objects.all():
        set_spec, created = Set.objects.get_or_create(spec='languages:%s' % language.code.lower())
        if created:
            set_spec.name=language.name
            set_spec.save()
            statistic['sets']['new'] += 1
        statistic['sets']['all'] += 1

    oai_dc = MetadataFormat.objects.get(prefix='oai_dc')
    for profile in Profile.objects.all():
        header, created = Header.objects.get_or_create(identifier='tima:citizen_scientists:%s' % profile.user.username)
        if created:
            header.metadata_formats.add(oai_dc)
            for language in profile.languages.all():
                header.sets.add(Set.objects.get(spec='languages:%s' % language.code.lower()))
            header.save()
            statistic['headers']['new'] += 1
        else:
            if header.deleted:
                header.deleted = False;
                header.metadata_formats.add(oai_dc)
                header.save()

        history_list = AssociationHistory.objects.filter(user=profile.user)

        record, created = DCRecord.objects.get_or_create(header=header)
        record.dc_title = profile.user.username
        record.dc_creator = None
        record.dc_subject = 'Citizen scientists'
        record.dc_description = None
        record.dc_publisher = 'TIMA'
        record.dc_contributor = None
        record.dc_type = 'Dataset'
        record.dc_format = None
        record.dc_identifier = 'tima:citizen_scientists:%s' % profile.user.username
        record.dc_source = None
        record.dc_language = None
        record.dc_relation = ';'.join(['tima:word:%s' % word.id for word in Word.objects.filter(Q(word__associationhistory__user=profile.user) | Q(association__associationhistory__user=profile.user)).distinct()])
        record.dc_coverage = profile.cultural_background
        record.dc_rights = 'http://creativecommons.org/licenses/by/4.0/'
        record.save()

    for header in Header.objects.filter(identifier__startswith='tima:citizen_scientists:').exclude(identifier__in=Profile.objects.annotate(identifier=Concat(V('tima:user:'), 'user__username')).values_list('identifier', flat=True)):
        if not header.deleted:
            header.deleted = True
            header.metadata_formats.clear()
            try:
                header.dcrecord.delete()
            except DCRecord.DoesNotExist:
                pass
            header.save()
    statistic['headers']['deleted'] = Header.objects.filter(identifier__startswith='tima:citizen_scientists:').filter(deleted=True).count()
    statistic['headers']['all'] = Header.objects.filter(identifier__startswith='tima:citizen_scientists:').count()

    return statistic
