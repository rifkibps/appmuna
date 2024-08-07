# Generated by Django 5.0.1 on 2024-02-07 13:50

import backend.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0024_alter_backenddatarequestsmodel_app_letter_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackendPublicationsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, verbose_name='Judul Publikasi')),
                ('catalog_no', models.CharField(max_length=128, verbose_name='Nama Pemohon')),
                ('publication_no', models.CharField(max_length=128, verbose_name='Nama Pemohon')),
                ('issn', models.CharField(max_length=128, verbose_name='Nama Pemohon')),
                ('release', models.CharField(max_length=128, verbose_name='Nama Pemohon')),
                ('abstract', models.CharField(max_length=128, verbose_name='Nama Pemohon')),
                ('file', models.FileField(blank=True, null=True, upload_to='publications', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), backend.validators.validate_publication_size], verbose_name='Unggah Publikasi')),
                ('revision_log', models.IntegerField(default=0, editable=False)),
                ('show_state', models.CharField(choices=[('1', 'Ya'), ('2', 'Tidak')], max_length=1, verbose_name='Tampilkan Publikasi')),
            ],
            options={
                'verbose_name': 'Master Buku Publikasi',
                'verbose_name_plural': 'Master Buku Publikasi',
            },
        ),
    ]
