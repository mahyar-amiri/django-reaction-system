from django import template
from django.contrib.contenttypes.models import ContentType

from reaction import settings
from reaction.models import Reaction, ReactionSettings

register = template.Library()


@register.inclusion_tag('reaction/reaction_form.html')
def render_reaction(request, obj, settings_slug):
    app_name = type(obj)._meta.app_label
    model_name = type(obj).__name__.lower()
    object_id = obj.id
    content_type = ContentType.objects.get(app_label=app_name, model=model_name)
    reaction_settings = ReactionSettings.objects.get(slug=settings_slug)
    reaction = Reaction.objects.get_or_create(content_type=content_type, object_id=object_id, settings=reaction_settings)[0]
    context = {
        'object': obj,
        'request': request,
        'reaction': reaction,
    }
    return context


@register.filter
def number(value, floating_points=None):
    converters = {
        3: 'K',
        6: 'M',
        9: 'B',
    }

    if floating_points is not None and (10 ** 12 > value >= 1000):
        for exponent, converter in converters.items():
            large_number = 10 ** exponent
            if value >= large_number * 1000:
                continue
            return f'{value / large_number:,.{floating_points}f} {converter}'
    else:
        return f'{value:,}'


@register.inclusion_tag('utils/IMPORTS.html')
def render_reaction_import():
    return {'offline_imports': settings.OFFLINE_IMPORTS}


@register.inclusion_tag('utils/SCRIPTS.html')
def render_reaction_script():
    pass
