# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse

from blanc_basic_assets.fields import AssetForeignKey


@python_2_unicode_compatible
class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blanc-events:category-event-list', args=[self.slug])


@python_2_unicode_compatible
class Event(models.Model):
    category = models.ForeignKey('blanc_events.Category')
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = AssetForeignKey('assets.Image', null=True, blank=True)
    image_height = models.PositiveIntegerField(editable=False, null=True)
    image_width = models.PositiveIntegerField(editable=False, null=True)
    summary = models.TextField(help_text='A short sentence description of the event.')
    start = models.DateTimeField(help_text='Start time/date.')
    end = models.DateTimeField(help_text='End time/date.')
    final_date = models.DateTimeField(editable=False, null=True, db_index=True)
    published = models.BooleanField(
        default=True,
        db_index=True,
        help_text='Post will be hidden unless this option is selected'
    )
    current_version = models.ForeignKey('glitter.Version', blank=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('start',)
        permissions = (
            ('edit_page', 'Can edit page'),
            ('publish_page', 'Can publish page'),
            ('view_protected_page', 'Can view protected page'),
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Set final date to the end, for one off events
        self.final_date = self.end
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blanc-events:detail', kwargs={
            'year': self.start.year,
            'month': str(self.start.month).zfill(2),
            'day': str(self.start.day).zfill(2),
            'slug': self.slug,
        })


