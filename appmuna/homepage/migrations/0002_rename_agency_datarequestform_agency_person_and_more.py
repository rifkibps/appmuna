# Generated by Django 5.0.1 on 2024-01-16 07:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datarequestform',
            old_name='agency',
            new_name='agency_person',
        ),
        migrations.RenameField(
            model_name='datarequestform',
            old_name='contact',
            new_name='contact_person',
        ),
        migrations.RenameField(
            model_name='datarequestform',
            old_name='name',
            new_name='name_person',
        ),
        migrations.RemoveField(
            model_name='datarequestform',
            name='desc_data',
        ),
        migrations.AddField(
            model_name='datarequestform',
            name='approved_at',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='datarequestform',
            name='request_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datarequestform',
            name='title',
            field=models.CharField(default=16012024, max_length=256, verbose_name='Deskripsi Permohonan Data'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datarequestform',
            name='desc',
            field=models.TextField(verbose_name='Deskripsi Data'),
        ),
    ]