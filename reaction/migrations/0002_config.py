from django.db import migrations


def InitialReact(apps, schema_editor):
    React = apps.get_model('reaction', 'React')
    React.objects.create(slug='like', emoji='👍')
    React.objects.create(slug='dislike', emoji='👎')
    React.objects.create(slug='heart', emoji='❤️')


def InitialReactionSettings(apps, schema_editor):
    ReactionSettings = apps.get_model('reaction', 'ReactionSettings')
    reaction_settings = ReactionSettings.objects.create(name='Default Config', slug='default-config', react_type='e')
    # Set some emojis to settings
    reacts = apps.get_model('reaction', 'React').objects.filter(slug__in=['like', 'dislike'])
    reaction_settings.react_emoji.set(reacts)


class Migration(migrations.Migration):
    dependencies = [
        ('reaction', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(InitialReact),
        migrations.RunPython(InitialReactionSettings),
    ]
