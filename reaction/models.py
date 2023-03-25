from random import choice
from string import ascii_lowercase

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import format_html

from reaction import settings

User = get_user_model()


class React(models.Model):
    slug = models.CharField(max_length=20, unique=True)
    emoji = models.CharField(max_length=5)
    source = models.ImageField(upload_to='react_source', null=True, blank=True)

    def __str__(self):
        return f'{self.emoji} ({self.slug})'

    def source_file(self):
        return format_html(f"<img style='height:20px' src='{self.source.url}' alt='{self.emoji}'>") if self.source else 'X'


class ReactionSettings(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(primary_key=True, help_text='This value will be used in render_reaction tag')
    react_type = models.CharField(max_length=1, choices=(('e', 'emoji'), ('s', 'source')), default='e')
    react_emoji = models.ManyToManyField(React, related_name='react_emojis')

    class Meta:
        verbose_name = 'Reaction Settings'
        verbose_name_plural = 'Reaction Settings'

    def __str__(self):
        return f'{self.name} - [{self.slug}]'


class ReactionQuerySet(models.QuerySet):
    def get_reacts(self):
        reacts = React.objects.all()
        return {react: self.filter(react=react) for react in reacts}


class Reaction(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    settings = models.ForeignKey(ReactionSettings, null=True, on_delete=models.SET_NULL)
    urlhash = models.CharField(max_length=50, unique=True, editable=False)

    objects = ReactionQuerySet.as_manager()

    def __str__(self):
        return f'{self.content_type} - {self.content_object}'

    @staticmethod
    def generate_urlhash():
        return ''.join(choice(ascii_lowercase) for _ in range(settings.URLHASH_LENGTH))

    def set_unique_urlhash(self):
        if not self.urlhash:
            self.urlhash = self.generate_urlhash()
            while self.__class__.objects.filter(urlhash=self.urlhash).exists():
                self.urlhash = self.generate_urlhash()

    def save(self, *args, **kwargs):
        self.set_unique_urlhash()
        super(Reaction, self).save(*args, **kwargs)


class UserReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    react = models.ForeignKey(React, related_name='reactions', on_delete=models.CASCADE)
    reaction = models.ForeignKey(Reaction, on_delete=models.CASCADE, related_name='reactions')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.react.emoji}'

    def save(self, *args, **kwargs):
        allowed_reacts = [react.id for react in Reaction.objects.get(id=self.reaction.id).settings.react_emoji.all()]
        if self.react.id in allowed_reacts:
            super(UserReaction, self).save(*args, **kwargs)
        else:
            raise PermissionError('React not allowed!')
