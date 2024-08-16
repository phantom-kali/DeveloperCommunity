# Generated by Django 4.2.11 on 2024-08-16 06:06

from django.db import migrations, models
import documents.models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_alter_document_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to=documents.models.get_unique_filename, validators=[documents.models.validate_file_size, documents.models.validate_file_type]),
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
