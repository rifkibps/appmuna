# Generated by Django 5.0.1 on 2024-07-21 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0038_alter_backendindicatorsmodel_summarize_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='backendunitsmodel',
            name='is_agg',
            field=models.CharField(choices=[('0', 'Tidak dapat diagregasikan'), ('1', 'Dapat Diagrregasikan')], default='1', max_length=1, verbose_name='Satuan dapat diagregasikan?'),
        ),
        migrations.AlterField(
            model_name='backendindicatorsmodel',
            name='summarize_status',
            field=models.CharField(choices=[('0', 'none'), ('1', 'sum'), ('2', 'avg'), ('3', 'percent')], default='0', max_length=1, verbose_name='Ringkasan Data'),
        ),
    ]