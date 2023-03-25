Django Reaction System
======================

Installation
------------

1. Install using pip

   .. code:: shell

      python -m pip install django-reaction-system

   or Clone the repository then copy ``reaction`` folder and paste in
   project folder.

   .. code:: shell

      git clone https://github.com/mahyar-amiri/django-reaction-system.git

Configuration
-------------

1. Add ``reaction.apps.ReactionConfig`` to installed_apps after
   ``django.contrib.auth`` in the ``settings.py`` file. Add
   ``MEDIA_URL`` and ``MEDIA_ROOT``.

   .. code:: python

      # setting.py

      INSTALLED_APPS = [
          'django.contrib.admin',
          'django.contrib.auth',
          'django.contrib.contenttypes',
          'django.contrib.sessions',
          'django.contrib.messages',
          'django.contrib.staticfiles',

          # MY APPS
          'reaction.apps.ReactionConfig',
      ]

      ...

      MEDIA_URL = '/media/'
      MEDIA_ROOT = BASE_DIR / 'media'

2. Add ``path('reaction/', include('reaction.urls')),`` and media root to
   urlpatterns in the project ``urls.py`` file.

   .. code:: python

      # urls.py

      from django.urls import path, include
      from django.conf import settings
      from django.conf.urls.static import static

      urlpatterns = [
           path('reaction/', include('reaction.urls')),
      ]

      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

3. Connect ``reaction`` to target model. In ``models.py`` add the field
   ``reactions`` as a GenericRelation field to the required model.

   **NOTE:** Please note that the field name must be ``reactions`` **NOT**
   ``reaction``.

   .. code:: python

      # models.py

      from django.db import models
      from django.contrib.contenttypes.fields import GenericRelation
      from reaction.models import Reaction

      class Article(models.Model):
          title = models.CharField(max_length=20)
          content = models.TextField()
          # the field name should be reactions
          reactions = GenericRelation(Reaction)

4. Do migrations

   .. code:: shell

      python manage.py migrate

Usage
-----

1. In the template (e.g. post_detail.html) add the following template
   tags where obj is the instance of post model.

   .. code:: html

      {% load reaction_tags %}

2. Add the following template tag to load stylesheet.

   .. code:: html

      {% render_reaction_import %}

3. Add the following template tags where you want to render reactions.

   .. code:: html

      {% render_reaction request obj settings_slug='default-config' %}  {# Render all the reactions belong to the passed object "obj" #}

   if your context_object_name is not ``obj`` (e.g. article) replace obj
   with context_object_name.

   .. code:: html

      {% render_reaction request obj=article settings_slug='default-config' %}

4. Add ``render_reaction_script`` tag at the end of the last
   ``render_reaction`` tag.

   .. code:: html

      {% render_reaction_import %}

      {% render_reaction request=request obj=article settings_slug='default-config' %}
      {% render_reaction request=request obj=article settings_slug='second-config' %}

      {% render_reaction_script %}
