# Generated by Django 4.2.11 on 2024-08-16 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0004_alter_document_file_alter_document_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationallink',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.CreateModel(
            name='LinkReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='documents.educationallink')),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]