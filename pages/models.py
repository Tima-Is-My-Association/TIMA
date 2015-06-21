from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

class TextFieldSingleLine(models.TextField):
    pass

class Page(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(max_length=2048, unique=True)
    title = TextFieldSingleLine()
    text = models.TextField()

    def get_absolute_url(self):
        return reverse('page', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        else:
            orig = Page.objects.get(pk=self.id)
            if orig.title != self.title:
                self.slug = slugify(self.title)

        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)