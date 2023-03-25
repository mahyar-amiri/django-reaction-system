# Django Reaction System

[![PyPI version](https://img.shields.io/pypi/v/django-reaction-system.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/django-reaction-system)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/django-reaction-system?color=092E20&logo=django)](https://pypi.org/project/django-reaction-system)
[![GitHub](https://img.shields.io/github/license/mahyar-amiri/django-reaction-system)](LICENSE)

## Table of Contents

* [Installation](#installation)
* [Configuration](#configuration)
* [Usage](#usage)
* [Settings](#settings)
    * [Global Settings](#global-settings)
    * [Config Settings](#config-settings)
* [Front-End](#front-end)

## Installation

1. Install using pip

   ```shell
   python -m pip install django-reaction-system
   ```

   or Clone the repository then copy `reaction` folder and paste in project folder.

   ```shell
   git clone https://github.com/mahyar-amiri/django-reaction-system.git
   ```

## Configuration

1. Add `reaction.apps.ReactionConfig` to installed_apps after `django.contrib.auth` in the `settings.py` file. Add `MEDIA_URL` and `MEDIA_ROOT`.

   ```python
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
   ```

2. Add `path('reaction/', include('reaction.urls')),` and media root to urlpatterns in the project `urls.py` file.

   ```python
   # urls.py

   from django.urls import path, include
   from django.conf import settings
   from django.conf.urls.static import static

   urlpatterns = [
        path('reaction/', include('reaction.urls')),
   ]
   
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

3. Connect `reactions` to target model. In `models.py` add the field `reactions` as a GenericRelation field to the
   required model.

   **NOTE:** Please note that the field name must be `reactions` **NOT** `reaction`.

   ```python
   # models.py
   
   from django.db import models
   from django.contrib.contenttypes.fields import GenericRelation
   from reaction.models import Reaction
   
   class Article(models.Model):
       title = models.CharField(max_length=20)
       content = models.TextField()
       # the field name should be reactions
       reactions = GenericRelation(Reaction)

   ```

4. Do migrations
   ```shell
   python manage.py migrate
   ```

## Usage

1. In the template (e.g. post_detail.html) add the following template tags where obj is the instance of post model.
   ```html
   {% load reaction_tags %}
   ```

2. Add the following template tag to load stylesheet.
   ```html
   {% render_reaction_import %}
   ```

3. Add the following template tags where you want to render reactions.
   ```html
   {% render_reaction request obj settings_slug='default-config' %}  {# Render all the reactions belong to the passed object "obj" #}
   ```
   if your context_object_name is not `obj` (e.g. article) replace obj with context_object_name.
   ```html
   {% render_reaction request obj=article settings_slug='default-config' %}
   ```

4. Add `render_reaction_script` tag at the end of the last `render_reaction` tag.
   ```html
   {% render_reaction_import %}

   {% render_reaction request=request obj=article settings_slug='default-config' %}
   {% render_reaction request=request obj=article settings_slug='second-config' %}
   
   {% render_reaction_script %}
   ```

## Settings

### Global Settings

You can customize global settings by adding keywords to `REACTION_SETTINGS` dictionary in project `settings.py`.

```python
# setting.py
REACTION_SETTINGS = {
    # generated urlhash length
    'URLHASH_LENGTH': 8,
    # if True, tailwindcss and jquery package will be loaded from static files.
    'OFFLINE_IMPORTS': True
}
```

### Config Settings

This settings can be configured in admin panel. Set your config in `ReactionSettings` model. You can use multi config all at once.

```python
REACT_TYPE = 'e'  # 'e' for emoji and 's' for source
REACT_EMOJI  # List of allowed emojis linked to React model
```

## Front-End

<details>
<summary>Tailwind Colors Customization</summary>
<p>

```text
colors: {
   // LIGHT
   'react-default-bg-light': '#f3f4f6',
   'react-default-border-light': '#e5e7eb',
   'react-selected-bg-light': '#dbeafe',
   'react-selected-border-light': '#bfdbfe',
   'react-count-text-light': '#000000',
   // DARK
   'react-default-bg-dark': '#334155',
   'react-default-border-dark': '#6b7280',
   'react-selected-bg-dark': '#64748b',
   'react-selected-border-dark': '#1e293b',
   'react-count-text-dark': '#f3f4f6',
}
```

</p>
</details>


<details>
<summary>Templates Folder Tree</summary>
<p>

```text
templates
   ├── reaction
   │    ├── reaction.html
   │    └── reaction_form.html
   │
   └── utils
        ├── IMPORTS.html
        └── SCRIPTS.html
```

</p>
</details>

<details>
<summary>Static Folder Tree</summary>
<p>

```text
static
   ├── css
   │    ├── style.css
   │    └── style.min.css
   ├── js
   │    ├── reaction.js
   │    ├── reaction.min.js
   │    └── jquery.min.js
   └── tailwindcss
        ├── style.css
        └── tailwind.config.js
```

</p>
</details>
