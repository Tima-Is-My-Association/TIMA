from app.models import AssociationHistory
from association.models import Language, Word
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat
from oai_pmh.models import DCRecord, Header, MetadataFormat, Set

def generate_metadata():
    for language in Language.objects.all():
        set_spec, created = Set.objects.get_or_create(spec='languages:%s' % language.code.lower())
        if created:
            set_spec.name=language.name
            set_spec.save()

    oai_dc = MetadataFormat.objects.get(prefix='oai_dc')
    for word in Word.objects.all():
        header, created = Header.objects.get_or_create(identifier='tima:word:%s' % word.id)
        if created:
            header.metadata_formats.add(oai_dc)
            header.sets.add(Set.objects.get(spec='languages:%s' % word.language.code.lower()))
            header.save()

        record, created = DCRecord.objects.get_or_create(header=header)
        record.dc_title = word.name
        record.dc_creator = 'TIMA'
        record.dc_subject = 'Word'
        record.dc_description = None
        record.dc_publisher = 'TIMA'
        record.dc_contributor = ';'.join(['%s' % history.user for history in AssociationHistory.objects.filter(association__word=word)])
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
