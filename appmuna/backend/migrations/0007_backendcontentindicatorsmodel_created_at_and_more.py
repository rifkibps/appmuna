# Generated by Django 5.0.1 on 2024-01-25 02:11

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_backendunitsmodel_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='backendcontentindicatorsmodel',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='backendcontentindicatorsmodel',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='backendcontentindicatorsmodel',
            name='item_char',
            field=models.CharField(max_length=1, verbose_name='Item Karakteristik Waktu'),
        ),
        migrations.AlterField(
            model_name='backendcontentindicatorsmodel',
            name='item_row',
            field=models.CharField(max_length=1, verbose_name='Item Judul Baris'),
        ),
        migrations.AlterField(
            model_name='backendcontentindicatorsmodel',
            name='value',
            field=models.FloatField(null=True, verbose_name='Nilai'),
        ),
        migrations.AlterField(
            model_name='backendindicatorsmodel',
            name='subject_csa_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject_csa_indicator', to='backend.backendsubjectsscamodel', verbose_name='Subjek CSA'),
        ),
        migrations.AlterField(
            model_name='backendindicatorsmodel',
            name='subject_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_indicator', to='backend.backendsubjectsmodel', verbose_name='Subjek Statistik'),
        ),
    ]
