from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

class TextFieldSingleLine(models.TextField):
	pass

class Language(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    name = TextFieldSingleLine(unique=True)
    slug = models.SlugField(unique=True)
    code = TextFieldSingleLine(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            if not self.slug:
                self.slug = slugify(self.code)
        else:
            orig = Language.objects.get(pk=self.id)
            if orig.name != self.name:
                self.slug = slugify(self.name)
                if not self.slug:
                    self.slug = slugify(self.code)
        super(Language, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Word(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    name = TextFieldSingleLine()
    count = models.BigIntegerField(default=0)
    language = models.ForeignKey(Language, related_name='words')

    def get_absolute_url(self):
        return reverse('word', args=[self.id])

    def to_json(self, request, limit=None):
        json = {'word': self.name,
                'language': self.language.code,
                'identifier': 'tima:word:%s' % self.id,
                'url': request.build_absolute_uri(self.get_absolute_url()),
                'json_url': '%s?word=%s' % (request.build_absolute_uri(reverse('words_export')), self.id)}

        associations = self.word.all().order_by('-count')
        if limit != None:
            associations = associations[:int(limit)]
        if associations:
            json['associations'] = [{'word': a.association.name,
                        'language': a.association.language.code,
                        'identifier': 'tima:word:%s' % a.association.id,
                        'url': request.build_absolute_uri(a.association.get_absolute_url()),
                        'json_url': '%s?word=%s' % (request.build_absolute_uri(reverse('words_export')), a.association.id),
                        'count': a.count
                        } for a in associations]
        return json

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'language')

class Association(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    word = models.ForeignKey(Word, related_name='word')
    association = models.ForeignKey(Word, related_name='association')
    count = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.word.count += 1
        self.word.save()
        self.count += 1
        super(Association, self).save(*args, **kwargs)

    def to_json(self, request):
        return {'word': self.word.to_json(request, limit=0),
                'association': self.association.to_json(request, limit=0),
                'count': self.count}

    def __str__(self):
        return '%s -> %s' % (self.word, self.association)

    class Meta:
        ordering = ('word', 'association')
