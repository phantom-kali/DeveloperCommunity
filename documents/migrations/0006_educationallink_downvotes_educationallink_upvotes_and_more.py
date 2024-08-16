# Generated by Django 4.2.11 on 2024-08-16 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0005_alter_educationallink_title_linkreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationallink',
            name='downvotes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='educationallink',
            name='upvotes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.SmallIntegerField(choices=[(1, 'Upvote'), (-1, 'Downvote')])),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.educationallink')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'link')},
            },
        ),
    ]
