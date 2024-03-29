# Generated by Django 5.0.1 on 2024-01-16 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackendCharacteristicsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Nama Karakteristik')),
            ],
        ),
        migrations.CreateModel(
            name='BackendPeriodsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Nama Periode Waktu')),
            ],
        ),
        migrations.CreateModel(
            name='BackendRowsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Nama Judul Baris')),
            ],
        ),
        migrations.CreateModel(
            name='BackendSubjectsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Nama Subject')),
                ('subject_group', models.CharField(choices=[('1', 'Sosial dan Kependudukan'), ('2', 'Ekonomi dan Perdagangan'), ('3', 'Pertanian dan Pertambangan')], max_length=1, verbose_name='Kelompok Subject')),
                ('show_state', models.CharField(choices=[('1', 'Ya'), ('2', 'Tidak')], max_length=1, verbose_name='Tampilkan Subject')),
            ],
        ),
        migrations.CreateModel(
            name='BackendSubjectsSCAModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Nama Subject CSA')),
                ('subject_group', models.CharField(choices=[('1', 'Sosial Demografi dan Sosial'), ('2', 'Statistik Ekonomi'), ('3', 'Statistik Lingkungan Hidup dan Multi - Domain')], max_length=1, verbose_name='Kelompok Subject CSA')),
                ('show_state', models.CharField(choices=[('1', 'Ya'), ('2', 'Tidak')], max_length=1, verbose_name='Tampilkan Subject CSA')),
            ],
        ),
        migrations.CreateModel(
            name='BackendUnitsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Nama Satuan')),
            ],
        ),
        migrations.CreateModel(
            name='BackendCharacteristicItemsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_char', models.CharField(max_length=256, verbose_name='Item Karakteristik')),
                ('char_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristic_items', to='backend.backendcharacteristicsmodel')),
            ],
        ),
        migrations.CreateModel(
            name='BackendPeriodNameItemsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_period', models.CharField(max_length=256, verbose_name='Item Periode Waktu')),
                ('period_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='period_item', to='backend.backendperiodsmodel')),
            ],
        ),
        migrations.CreateModel(
            name='BackendRowsItemsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.IntegerField(verbose_name='No Urut Baris')),
                ('item_row', models.CharField(max_length=256, verbose_name='Item Judul Baris')),
                ('row_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='row_items', to='backend.backendrowsmodel')),
            ],
        ),
        migrations.CreateModel(
            name='BackendStatsNewsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, verbose_name='Judul Berita Statistik')),
                ('content', models.TextField(verbose_name='Konten Berita')),
                ('file', models.FileField(upload_to='stats_news', verbose_name='File Berita')),
                ('thumbnail', models.FileField(upload_to='thumbnail-statsnews', verbose_name='Thumbnail Berita')),
                ('show_state', models.CharField(choices=[('1', 'Ya'), ('2', 'Tidak')], max_length=1, verbose_name='Tampilkan Berita')),
                ('num_visits', models.IntegerField(editable=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_stat_news', to='backend.backendsubjectsmodel')),
                ('subject_csa_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_csa_stat_news', to='backend.backendsubjectsscamodel')),
            ],
        ),
        migrations.CreateModel(
            name='BackendInfographicsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, verbose_name='Judul Infografis')),
                ('desc', models.TextField(verbose_name='Deskripsi Infografis')),
                ('file', models.FileField(upload_to='infographics', verbose_name='File Infografis')),
                ('show_state', models.CharField(choices=[('1', 'Ya'), ('2', 'Tidak')], max_length=1, verbose_name='Tampilkan Infografis')),
                ('num_visits', models.IntegerField(editable=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_infographic', to='backend.backendsubjectsmodel')),
                ('subject_csa_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_csa_infographic', to='backend.backendsubjectsscamodel')),
            ],
        ),
        migrations.CreateModel(
            name='BackendIndicatorsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='Nama Indikator')),
                ('desc', models.TextField(verbose_name='Deskripsi Indikator')),
                ('footer_desc', models.CharField(max_length=512, verbose_name='Keterangan Indikator')),
                ('decimal_point', models.IntegerField(default=2, verbose_name='Jumlah Desimal')),
                ('stat_category', models.CharField(choices=[('1', 'Dasar'), ('2', 'Sektoral')], max_length=1, verbose_name='Kategori Statistik')),
                ('show_state', models.CharField(choices=[('1', 'Ya'), ('2', 'Tidak')], max_length=1, verbose_name='Tampilkan Indikator')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('col_group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cols_indicator', to='backend.backendcharacteristicsmodel')),
                ('time_period_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='period_indicator', to='backend.backendperiodsmodel')),
                ('row_group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows_indicator', to='backend.backendrowsmodel')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_indicator', to='backend.backendsubjectsmodel')),
                ('subject_csa_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_csa_indicator', to='backend.backendsubjectsscamodel')),
                ('unit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_indicator', to='backend.backendunitsmodel')),
            ],
        ),
        migrations.CreateModel(
            name='BackendVideoGraphicsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, verbose_name='Judul Videografis')),
                ('desc', models.TextField(verbose_name='Deskripsi Videografis')),
                ('file', models.FileField(upload_to='videographics', verbose_name='File Videografis')),
                ('thumbnail', models.FileField(upload_to='thumbnail-videographics', verbose_name='Thumbnail Videografis')),
                ('show_state', models.CharField(choices=[('1', 'Ya'), ('2', 'Tidak')], max_length=1, verbose_name='Tampilkan Videografis')),
                ('num_visits', models.IntegerField(editable=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('subject_csa_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_csa_videographic', to='backend.backendsubjectsscamodel')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_videographic', to='backend.backendsubjectsmodel')),
            ],
        ),
    ]
