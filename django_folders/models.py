# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models


class Folder(models.Model):
    name = models.CharField("Name", max_length=50)
    parent = models.ForeignKey(
        'self', blank=True, null=True,
        related_name='children',
        verbose_name="Überordner"
    )

    def clean(self):
        if self.id and self.parent and self.parent.id == self.id:
            raise ValidationError("Kann nicht Überordner von sich selbst sein")

    def get_ancestors(self):
        try:
            ancestors = self.parent.get_ancestors()
        except AttributeError:
            ancestors = []
        else:
            ancestors = ancestors + [self.parent]
        return ancestors

    def get_form_choice_tuple(self):
        return (self.pk, self.get_form_choice_name())

    def get_form_choice_name(self):
        number_of_dashes = len(self.get_ancestors())
        dashes = '- ' * number_of_dashes
        return '%s%s' % (dashes, self.name)

    def __lt__(self, other):
        # This will not affect querysets!
        # Made for ordering of form field choices.
        # Explicit __lt__ is needed for python 3 where __cmp__ disappears.
        return self.__cmp__() < other.__cmp__()

    def __cmp__(self):
        ancestors = self.get_ancestors() + [self]
        return ''.join([a.name for a in ancestors]).lower()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Ordner"
        verbose_name_plural = "Ordner"


class FolderMixin(models.Model):
    folder = models.ForeignKey(
        Folder, blank=True, null=True,
        verbose_name="Ordner"
    )

    class Meta:
        abstract = True
