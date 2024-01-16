from django.db import models

# Characteristic Subject Model
class BackendSubjectsModel(models.Model):
   
   class Meta:
        verbose_name = 'Master Subject'
        verbose_name_plural = 'Master Subject'   

   groups = (
   
       ('1', 'Sosial dan Kependudukan'),
       ('2', 'Ekonomi dan Perdagangan'),
       ('3', 'Pertanian dan Pertambangan')
   )
   
   status = (
      ('1', 'Ya'),
      ('2', 'Tidak')
   )

   name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Nama Subject' )
   subject_group = models.CharField(max_length=1, choices=groups, verbose_name='Kelompok Subject')
   show_state = models.CharField(max_length=1, choices=status, verbose_name='Tampilkan Subject')

   def __str__(self):
      return f"{self.name} | {self.get_subject_group_display}"

# Characteristic Subject CSA Model
class BackendSubjectsSCAModel(models.Model):
      
   class Meta:
        verbose_name = 'Master Subject SCA'
        verbose_name_plural = 'Master Subject SCA'   

   groups = (
       ('1', 'Sosial Demografi dan Sosial'),
       ('2', 'Statistik Ekonomi'),
       ('3', 'Statistik Lingkungan Hidup dan Multi - Domain')
   )
   
   status = (
      ('1', 'Ya'),
      ('2', 'Tidak')
   )

   name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Nama Subject CSA' )
   subject_group = models.CharField(max_length=1, choices=groups, verbose_name='Kelompok Subject CSA')
   show_state = models.CharField(max_length=1, choices=status, verbose_name='Tampilkan Subject CSA')

   def __str__(self):
      return f"{self.name} | {self.get_subject_group_display}"


# Characteristic Model
class BackendCharacteristicsModel(models.Model):
      
   class Meta:
        verbose_name = 'Master Karakteristik'
        verbose_name_plural = 'Master Karakteristik'   

   name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Nama Karakteristik' )

   def __str__(self):
      return f"{self.name}"
   
class BackendCharacteristicItemsModel(models.Model):
   
   char_id = models.ForeignKey(BackendCharacteristicsModel, on_delete=models.CASCADE, null=False, related_name='characteristic_items')
   item_char = models.CharField(max_length=256, null=False, blank=False, verbose_name='Item Karakteristik' )

   def __str__(self):
      return f"{self.char_id.name} | {self.item_char}"


# Rows Name Model
class BackendRowsModel(models.Model):
      
   class Meta:
        verbose_name = 'Master Judul Baris'
        verbose_name_plural = 'Master Judul Baris'   

   name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Nama Judul Baris' )

   def __str__(self):
      return f"{self.name}"
   
class BackendRowsItemsModel(models.Model):
   
   row_id = models.ForeignKey(BackendRowsModel, on_delete=models.CASCADE, null=False, related_name='row_items')
   order_num = models.IntegerField(null=False, blank=False, verbose_name='No Urut Baris' )
   item_row = models.CharField(max_length=256, null=False, blank=False, verbose_name='Item Judul Baris' )

   def __str__(self):
      return f"{self.row_id.name} | {self.item_row}"


# Period Name Model
class BackendPeriodsModel(models.Model):
   
   class Meta:
        verbose_name = 'Periode Waktu Statistik'
        verbose_name_plural = 'Periode Waktu Statistik'   

   name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Nama Periode Waktu' )

   def __str__(self):
      return f"{self.name}"
   
class BackendPeriodNameItemsModel(models.Model):
   
   period_id = models.ForeignKey(BackendPeriodsModel, on_delete=models.CASCADE, null=False, related_name='period_item')
   item_period = models.CharField(max_length=256, null=False, blank=False, verbose_name='Item Periode Waktu' )

   def __str__(self):
      return f"{self.row_id.name} | {self.item_row}"

# Unit Name Model
class BackendUnitsModel(models.Model):
   
   class Meta:
        verbose_name = 'Satuan Data Statistik'
        verbose_name_plural = 'Satuan Data Statistik'   

   name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Nama Satuan' )

   def __str__(self):
      return f"{self.name}"
   

# Indikatior Model
class BackendIndicatorsModel(models.Model):
   
   class Meta:
        verbose_name = 'Master Tabel Statistik'
        verbose_name_plural = 'Master Tabel Statistik'   

   cats = (
      ('1', 'Dasar'),
      ('2', 'Sektoral')
   )
   state = (
      ('1', 'Ya'),
      ('2', 'Tidak')
   )

   subject_id = models.ForeignKey(BackendSubjectsModel, on_delete=models.CASCADE, null=False, related_name='subject_indicator')
   subject_csa_id = models.ForeignKey(BackendSubjectsSCAModel, on_delete=models.CASCADE, null=False, related_name='subject_csa_indicator')
   name =  models.CharField(max_length=512, null=False, blank=False, verbose_name='Nama Indikator' )
   desc =  models.TextField(null=False, blank=False, verbose_name='Deskripsi Indikator' )
   footer_desc =  models.CharField(max_length=512, null=False, blank=False, verbose_name='Keterangan Indikator' )
   col_group_id = models.ForeignKey(BackendCharacteristicsModel, on_delete=models.CASCADE, null=False, related_name='cols_indicator')
   row_group_id = models.ForeignKey(BackendRowsModel, on_delete=models.CASCADE, null=False, related_name='rows_indicator')
   time_period_id = models.ForeignKey(BackendPeriodsModel, on_delete=models.CASCADE, null=False, related_name='period_indicator')
   unit_id = models.ForeignKey(BackendUnitsModel, on_delete=models.CASCADE, null=False, related_name='unit_indicator')
   decimal_point = models.IntegerField(null=False, blank=False, default=2, verbose_name='Jumlah Desimal')
   stat_category = models.CharField(max_length=1, choices = cats, null=False, blank=False, verbose_name='Kategori Statistik')
   show_state = models.CharField(max_length=1, choices = state, null=False, blank=False, verbose_name='Tampilkan Indikator')
   created_at = models.DateField(auto_now_add = True, editable=False)
   updated_at = models.DateField(auto_now = True, editable=False)
   
   def __str__(self):
      return f"{self.subject_id.name} | {self.name}"


# infografis Model
class BackendInfographicsModel(models.Model):
   
   class Meta:
        verbose_name = 'Master Infografis'
        verbose_name_plural = 'Master Infografis'

   state = (
      ('1', 'Ya'),
      ('2', 'Tidak')
    )
   
   subject_id = models.ForeignKey(BackendSubjectsModel, on_delete=models.CASCADE, null=False, related_name='subject_infographic')
   subject_csa_id = models.ForeignKey(BackendSubjectsSCAModel, on_delete=models.CASCADE, null=False, related_name='subject_csa_infographic')
   title =  models.CharField(max_length=512, null=False, blank=False, verbose_name='Judul Infografis' )
   desc =  models.TextField(null=False, blank=False, verbose_name='Deskripsi Infografis' )
   file = models.FileField(null=False, blank=False, upload_to='infographics', verbose_name='File Infografis')
   show_state = models.CharField(max_length=1, choices = state, null=False, blank=False, verbose_name='Tampilkan Infografis')
   num_visits = models.IntegerField(null=False, blank=False, editable=False)
   created_at = models.DateField(auto_now_add = True, editable=False)
   updated_at = models.DateField(auto_now = True, editable=False)

# videografis Model
class BackendVideoGraphicsModel(models.Model):
   
   class Meta:
        verbose_name = 'Master Videografis'
        verbose_name_plural = 'Master Videografis'

   state = (
      ('1', 'Ya'),
      ('2', 'Tidak')
    )
   
   subject_id = models.ForeignKey(BackendSubjectsModel, on_delete=models.CASCADE, null=False, related_name='subject_videographic')
   subject_csa_id = models.ForeignKey(BackendSubjectsSCAModel, on_delete=models.CASCADE, null=False, related_name='subject_csa_videographic')
   title =  models.CharField(max_length=512, null=False, blank=False, verbose_name='Judul Videografis')
   desc =  models.TextField(null=False, blank=False, verbose_name='Deskripsi Videografis')
   file = models.FileField(null=False, blank=False, upload_to='videographics', verbose_name='File Videografis')
   thumbnail = models.FileField(null=False, blank=False, upload_to='thumbnail-videographics', verbose_name='Thumbnail Videografis')
   show_state = models.CharField(max_length=1, choices = state, null=False, blank=False, verbose_name='Tampilkan Videografis')
   num_visits = models.IntegerField(null=False, blank=False, editable=False)
   created_at = models.DateField(auto_now_add = True, editable=False)
   updated_at = models.DateField(auto_now = True, editable=False)

# Berita Statistik Model
class BackendStatsNewsModel(models.Model):

   class Meta:
        verbose_name = 'Berita Statistik'
        verbose_name_plural = 'Berita Statistik'
   
   state = (
      ('1', 'Ya'),
      ('2', 'Tidak')
    )
   
   subject_id = models.ForeignKey(BackendSubjectsModel, on_delete=models.CASCADE, null=False, related_name='subject_stat_news')
   subject_csa_id = models.ForeignKey(BackendSubjectsSCAModel, on_delete=models.CASCADE, null=False, related_name='subject_csa_stat_news')

   title =  models.CharField(max_length=512, null=False, blank=False, verbose_name='Judul Berita Statistik')
   content =  models.TextField(null=False, blank=False, verbose_name='Konten Berita')
   file = models.FileField(null=False, blank=False, upload_to='stats_news', verbose_name='File Berita')
   thumbnail = models.FileField(null=False, blank=False, upload_to='thumbnail-statsnews', verbose_name='Thumbnail Berita')
   show_state = models.CharField(max_length=1, choices = state, null=False, blank=False, verbose_name='Tampilkan Berita')
   num_visits = models.IntegerField(null=False, blank=False, editable=False)
   created_at = models.DateField(auto_now_add = True, editable=False)
   updated_at = models.DateField(auto_now = True, editable=False)