# Generated by Django 5.0.1 on 2024-01-17 05:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_alter_backendcharacteristicsmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backendindicatorsmodel',
            name='subject_csa_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject_csa_indicator', to='backend.backendsubjectsscamodel'),
        ),
    ]
