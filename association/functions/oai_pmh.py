from app.models import AssociationHistory
from association.models import Language, Word
from django.db.models import CharField, Value as V
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
    statistic['sets']['all'] = Set.objects.all().count()

    oai_dc = MetadataFormat.objects.get(prefix='oai_dc')
    for word in Word.objects.all():
        header, created = Header.objects.get_or_create(identifier='tima:word:%s' % word.id)
        if created:
            header.metadata_formats.add(oai_dc)
            header.sets.add(Set.objects.get(spec='languages:%s' % word.language.code.lower()))
            header.save()
            statistic['headers']['new'] += 1

        record, created = DCRecord.objects.get_or_create(header=header)
        record.dc_title = word.name
        record.dc_creator = 'TIMA'
        record.dc_subject = 'Word'
        record.dc_description = None
        record.dc_publisher = 'TIMA'
        record.dc_contributor = ';'.join([user for user in AssociationHistory.objects.filter(association__word=word).values_list('user__username', flat=True) if user])
        record.dc_type = 'Dataset'
        record.dc_format = None
        record.dc_identifier = 'tima:word:%s' % word.id
        record.dc_source = None
        record.dc_language = word.language.name
        record.dc_relation = ';'.join(['tima:word:%s' % word.id for word in word.word.all()] + ['tima:word:%s' % word.id for word in word.association.all()])
        record.dc_coverage = None
        record.dc_rights = 'http://creativecommons.org/licenses/by/4.0/'
        record.save()

    for header in Header.objects.exclude(identifier__in=Word.objects.annotate(identifier=Concat(V('tima:word:'), 'id')).values_list('identifier', flat=True)):
        if not header.deleted:
            header.deleted = True
            header.metadata_formats.clear()
            try:
                header.dcrecord.delete()
            except DCRecord.DoesNotExist:
                pass
            header.save()
    statistic['headers']['deleted'] = Header.objects.filter(deleted=True).count()
    statistic['headers']['all'] = Header.objects.all().count()

    return statistic
