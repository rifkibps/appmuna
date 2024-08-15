# Generated by Django 5.0.1 on 2024-08-15 03:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0046_backenddashboardsummarizemodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='backenddashboardsummarizemodel',
            options={'verbose_name': 'Highlight Dashboard Items', 'verbose_name_plural': 'Highlight Dashboard Items'},
        ),
        migrations.AlterModelOptions(
            name='backenddataconsultresponsmodel',
            options={'verbose_name': 'Respons Konsultasi Data', 'verbose_name_plural': 'Respons Konsultasi Data'},
        ),
        migrations.AlterField(
            model_name='backenddashboardsummarizemodel',
            name='indicator_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='table_reference', to='backend.backendindicatorsmodel'),
        ),
        migrations.AlterField(
            model_name='backenddashboardsummarizemodel',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=50, null=True, verbose_name='Nilai'),
        ),
    ]
