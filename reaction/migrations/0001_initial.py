# Generated by Django 4.1.7 on 2023-03-25 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='React',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=20, unique=True)),
                ('emoji', models.CharField(max_length=5)),
                ('source', models.ImageField(blank=True, null=True, upload_to='react_source')),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('urlhash', models.CharField(editable=False, max_length=50, unique=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='UserReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('react', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='reaction.react')),
                ('reaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='reaction.reaction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReactionSettings',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField(help_text='This value will be used in render_reaction tag', primary_key=True, serialize=False)),
                ('react_type', models.CharField(choices=[('e', 'emoji'), ('s', 'source')], default='e', max_length=1)),
                ('react_emoji', models.ManyToManyField(related_name='react_emojis', to='reaction.react')),
            ],
            options={
                'verbose_name': 'Reaction Settings',
                'verbose_name_plural': 'Reaction Settings',
            },
        ),
        migrations.AddField(
            model_name='reaction',
            name='settings',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reaction.reactionsettings'),
        ),
    ]