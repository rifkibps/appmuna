from django.db import models
from django.core.validators import FileExtensionValidator
from . import validators


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
   subject_group = models.CharField(max_length=1, null=False, blank=False, choices=groups, verbose_name='Kelompok Subject')
   show_state = models.CharField(max_length=1, null=False, blank=False, choices=status, verbose_name='Tampilkan Subject')

   def __str__(self):
      return f"{self.pk}. {self.get_subject_group_display()} | {self.name}"

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
      return f"{self.pk} | {self.name}"
   
class BackendPeriodNameItemsModel(models.Model):
   
   period_id = models.ForeignKey(BackendPeriodsModel, on_delete=models.CASCADE, null=False, related_name='period_item')
   item_period = models.CharField(max_length=256, null=False, blank=False, verbose_name='Item Periode Waktu' )

   def __str__(self):
      return f"{self.pk} | {self.period_id}-{self.item_period} {self.period_id.name} | {self.item_period}"


# Unit Name Model
class BackendUnitsModel(models.Model):
   
   class Meta:
        verbose_name = 'Satuan Data Statistik'
        verbose_name_plural = 'Satuan Data Statistik'   

   name = models.CharField(max_length=256, null=False, blank=False, verbose_name='Nama Satuan' )
   desc = models.TextField(null=True, blank=True, verbose_name='Keterangan Satuan' )

   def __str__(self):
      return f"{self.name}"
   

# Indikator Model
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

   level_choices = (
      ('0', 'Indikator Biasa'),
      ('1', 'Indikator Strategis'),
      ('2', 'Indikator Pembangunan'),
   )

   summarize_status = (
      ('0', 'none'),
      ('1', 'sum'),
      ('2', 'avg'),
   )


   subject_id = models.ForeignKey(BackendSubjectsModel, on_delete=models.CASCADE, null=False, related_name='subject_indicator', verbose_name='Subjek Statistik')
   subject_csa_id = models.ForeignKey(BackendSubjectsSCAModel, on_delete=models.CASCADE, null=True, blank=True, related_name='subject_csa_indicator', verbose_name='Subjek CSA')
   name =  models.CharField(max_length=512, null=False, blank=False, verbose_name='Nama Indikator' )
   desc =  models.TextField(null=False, blank=False, verbose_name='Deskripsi Indikator' )
   footer_desc =  models.CharField(max_length=512, null=False, blank=False, verbose_name='Keterangan Indikator' )
   col_group_id = models.ForeignKey(BackendCharacteristicsModel, on_delete=models.CASCADE, null=True, blank=True, related_name='cols_indicator', verbose_name='Kelompok Karakteristik' )
   row_group_id = models.ForeignKey(BackendRowsModel, on_delete=models.CASCADE, null=False, related_name='rows_indicator', verbose_name='Kelompok Judul Baris')
   time_period_id = models.ForeignKey(BackendPeriodsModel, on_delete=models.CASCADE, null=False, related_name='period_indicator', verbose_name='Periode Data')
   unit_id = models.ForeignKey(BackendUnitsModel, on_delete=models.CASCADE, null=True, blank=True, related_name='unit_indicator', verbose_name='Satuan')
   decimal_point = models.IntegerField(null=False, blank=False, default=2, verbose_name='Jumlah Desimal')
   summarize_status = models.CharField(max_length=1, choices = summarize_status, default= '0',null=False, blank=False, verbose_name='Ringkasan Data')
   stat_category = models.CharField(max_length=1, choices = cats, null=False, blank=False, verbose_name='Kategori Statistik')
   show_state = models.CharField(max_length=1, choices = state, null=False, blank=False, verbose_name='Tampilkan Indikator')
   level_data = models.CharField(max_length=1, choices = level_choices, default= '0',null=False, blank=False, verbose_name='Level Data')
   created_at = models.DateField(auto_now_add = True, editable=False)
   updated_at = models.DateField(auto_now = True, editable=False)
   
   def __str__(self):
      return f"{self.id}. {self.subject_id.name} | {self.name}"

# Indikator Content Model
class BackendContentIndicatorsModel(models.Model):
   
   class Meta:
        verbose_name = 'Master Konten Tabel'
        verbose_name_plural = 'Master Konten Tabel'   

   indicator_id = models.ForeignKey(BackendIndicatorsModel, on_delete=models.PROTECT, null=False, related_name='content_indicator')
   year = models.CharField(max_length=5, null=False, blank=False, verbose_name='Tahun Indikator')
   item_period = models.CharField(max_length=255, null=False, blank=False, verbose_name='Periode Waktu')
   item_char = models.CharField(max_length=255, null=True, blank=True, verbose_name='Item Karakteristik Waktu')
   item_row = models.CharField(max_length=255, null=False, blank=False, verbose_name='Item Judul Baris')
   value = models.DecimalField(null=True, blank=True, verbose_name = 'Nilai', decimal_places = 10, max_digits=50)
   created_at = models.DateField(auto_now_add = True, editable=False)
   updated_at = models.DateField(auto_now = True, editable=False)
   
   def __str__(self):
      return f"{self.indicator_id.name} | {self.year}"
   

class BackendIndicatorsMeaningModel(models.Model):
   class Meta:
        verbose_name = 'Master Interpretasi Tabel'
        verbose_name_plural = 'Master Interpretasi Tabel'  


   indicator_id = models.ForeignKey(BackendIndicatorsModel, on_delete=models.PROTECT, null=False, related_name='meaning_indicator')
   year = models.CharField(max_length=5, null=False, blank=False, verbose_name='Tahun Indikator')
   item_period = models.CharField(max_length=255, null=False, blank=False, verbose_name='Periode Waktu')
   context = models.TextField(null=False, blank=False, verbose_name = 'Interpretasi Data')
   created_at = models.DateField(auto_now_add = True, editable=False)
   updated_at = models.DateField(auto_now = True, editable=False)
   
   def __str__(self):
      return f"{self.pk}. {self.indicator_id.name} | {self.year}" 

class BackendContentStatisModel(models.Model):
      class Meta:
        verbose_name = 'Master Konten Tabel Statis'
        verbose_name_plural = 'Master Konten Tabel Statis'   

      state = (
         ('1', 'Ya'),
         ('2', 'Tidak')
      )

      cats = (
         ('1', 'Dasar'),
         ('2', 'Sektoral')
      )
      
      subject_id = models.ForeignKey(BackendSubjectsModel, on_delete=models.CASCADE, null=False, related_name='subject_content_static')
      subject_csa_id = models.ForeignKey(BackendSubjectsSCAModel, on_delete=models.CASCADE, null=True, blank=True, related_name='subject_csa_content_static')
      title =  models.CharField(max_length=512, null=False, blank=False, verbose_name='Judul Tabel' )
      year = models.CharField(max_length=5, null=False, blank=False, verbose_name='Tahun Tabel')
      content = models.TextField(null=False, blank=False, verbose_name='Konten HTML' )
      footer_desc =  models.CharField(max_length=512, null=False, blank=False, verbose_name='Keterangan Tabel' )
      stat_category = models.CharField(max_length=1, choices = cats, null=False, blank=False, verbose_name='Kategori Statistik')
      show_state = models.CharField(max_length=1, choices = state, null=False, blank=False, verbose_name='Tampilkan Infografis')
      created_at = models.DateField(auto_now_add = True, editable=False)
      updated_at = models.DateField(auto_now = True, editable=False)

      def __str__(self):
         return f"{self.id} {self.subject_id.name} | {self.title}"

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
   subject_csa_id = models.ForeignKey(BackendSubjectsSCAModel, on_delete=models.CASCADE, null=True, blank=True, related_name='subject_csa_infographic')
   title =  models.CharField(max_length=512, null=False, blank=False, verbose_name='Judul Infografis' )
   desc =  models.TextField(null=False, blank=False, verbose_name='Deskripsi Infografis' )
   thumbnail = models.ImageField(null=True, blank=True, upload_to='thumbnail-infographics', validators=[validators.validate_file_size], verbose_name='Thumbnail Infographics')
   file = models.FileField(null=False, blank=False, upload_to='infographics', verbose_name='File Infografis', validators=[FileExtensionValidator(allowed_extensions=["pdf"]), validators.validate_file_size])
   show_state = models.CharField(max_length=1, choices = state, null=False, blank=False, verbose_name='Tampilkan Infografis')
   num_visits = models.IntegerField(null=False, blank=False, default=0, editable=False)
   created_at = models.DateField(auto_now_add = True, editable=False)
   updated_at = models.DateField(auto_now = True, editable=False)

   def __str__(self):
      return f"{self.id} {self.subject_id.name} | {self.title}"
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
   subject_csa_id = models.ForeignKey(BackendSubjectsSCAModel, on_delete=models.CASCADE, null=True, blank=True, related_name='subject_csa_videographic')
   title =  models.CharField(max_length=512, null=False, blank=False, verbose_name='Judul Videografis')
   desc =  models.TextField(null=False, blank=False, verbose_name='Deskripsi Videografis')
   link = models.CharField(max_length=512, null=True, blank=True, verbose_name='Link Youtube')
   file = models.FileField(null=True, blank=True, upload_to='videographics', verbose_name='File Videografis', validators=[FileExtensionValidator(allowed_extensions=["mp4", "mkv"]), validators.validate_video_file_size])
   thumbnail = models.ImageField(null=False, blank=False, upload_to='thumbnail-videographics', validators=[validators.validate_file_size], verbose_name='Thumbnail Videografis')
   show_state = models.CharField(max_length=1, choices = state, null=False, blank=False, verbose_name='Tampilkan Videografis')
   num_visits = models.IntegerField(null=False, blank=False, default=0, editable=False)
   created_at = models.DateField(auto_now_add = True, editable=False)
   updated_at = models.DateField(auto_now = True, editable=False)

   def __str__(self):
      return f"{self.id} {self.subject_id.name} | {self.title}"

# Berita Statistik Model
class BackendStatsNewsModel(models.Model):

   class Meta:
        verbose_name = 'Berita Statistik' 
        verbose_name_plural = 'Berita Statistik'
   
   state = (
      ('1', 'Ya'),
      ('2', 'Tidak')
    )
   
   subject_id = models.ForeignKey(BackendSubjectsModel, on_delete=models.CASCADE, null=False, related_name='subject_stat_news', verbose_name='Subjek Statistik')
   subject_csa_id = models.ForeignKey(BackendSubjectsSCAModel, on_delete=models.CASCADE, null=True, blank=True, related_name='subject_csa_stat_news', verbose_name='Subjek CSA')

   title =  models.CharField(max_length=512, null=False, blank=False, verbose_name='Judul Berita Statistik')
   author = models.CharField(max_length=128, null=False, blank=False, default="BPS Kabupaten Muna", verbose_name='Penulis')
   content =  models.TextField(null=False, blank=False, verbose_name='Konten Berita')
   file = models.FileField(null=False, blank=False, upload_to='stats_news', verbose_name='File Berita', validators=[FileExtensionValidator(allowed_extensions=["pdf"]), validators.validate_file_size])
   thumbnail = models.ImageField(null=False, blank=False, upload_to='thumbnail-statsnews', validators=[validators.validate_file_size], verbose_name='Thumbnail Berita')
   show_state = models.CharField(max_length=1, choices = state, null=False, blank=False, verbose_name='Tampilkan Berita')
   num_visits = models.IntegerField(null=False, blank=False, default=0, editable=False)
   created_at = models.DateField(auto_now_add = True, editable=False)
   updated_at = models.DateField(auto_now = True, editable=False)

   def __str__(self):
      return f"{self.subject_id.name} | {self.title} | {self.created_at.strftime('%d/%m/%Y')}"
   

class BackendDataConsultModel(models.Model):

   class Meta:
      verbose_name = 'Konsultasi Data' 
      verbose_name_plural = 'Konsultasi Data'

   state = (
      ('0', 'Belum Diproses'),
      ('1', 'Sedang Diproses'),
      ('2', 'Selesai'),
      ('3', 'Dibatalkan'),
   )
   
   name =  models.CharField(max_length=128, null=False, blank=False, verbose_name='Nama')
   contact =  models.CharField(max_length=13, null=False, blank=False, verbose_name='Nomor Telp')
   email =  models.CharField(max_length=128, null=False, blank=False, verbose_name='Email Pemohon')
   subject = models.CharField(max_length=512, null=False, blank=False, verbose_name='Subjek Pesan')
   message = models.TextField(null=False, blank=False, verbose_name='Pesan')
   created_at = models.DateField(auto_now_add = True, editable=False)
   state_solved = models.CharField(max_length=1, choices = state, default="0", null=False, blank=False, verbose_name='Status Pesan')
   
   def __str__(self):
      return f"{self.id}. {self.name} ({self.email}) - {self.created_at.strftime('%d/%m/%Y')}"

class BackendDataConsultResponsModel(models.Model):

   class Meta:
      verbose_name = 'Renspons Konsultasi Data' 
      verbose_name_plural = 'Renspons Konsultasi Data'

   adm_state = (
      ('1', 'Ya'),
      ('2', 'Tidak')
   )

   data_consult = models.ForeignKey(BackendDataConsultModel, on_delete=models.CASCADE, null=False, related_name='data_consult_respons', verbose_name='Data Consult Issue')
   message = models.TextField(null=False, blank=False, verbose_name='Feedback Pesan')
   is_from_admin = models.CharField(max_length=1, choices = adm_state, default="2", null=False, blank=False, verbose_name='Is from admin?')
   created_at = models.DateField(auto_now_add = True, editable=False)


class BackendDataRequestsModel(models.Model):
    
   class Meta:
      verbose_name = 'Permohonan Data' 
      verbose_name_plural = 'Permohonan Data'
   
   state = (
      ('1', 'Menunggu Konfirmasi PIC'),
      ('2', 'Diproses'),
      ('3', 'Disetujui'),
      ('4', 'Ditolak'),
      ('5', 'Dibatalkan')
    )

   name_person =  models.CharField(max_length=128, null=False, blank=False, verbose_name='Nama Pemohon')
   contact_person =  models.CharField(max_length=128, null=False, blank=False, verbose_name='Kontak Pemohon')
   email_person =  models.CharField(max_length=128, null=False, blank=False, verbose_name='Email Pemohon')
   agency_person = models.CharField(max_length=128, null=False, blank=False, verbose_name='Instansi Pemohon')

   subject_request =  models.CharField(max_length=128, null=False, blank=False, verbose_name='Judul Permohonan Data')
   desc_data =  models.TextField(null=False, blank=False, verbose_name='Deskripsi Data yang Dimaksudkan')
   app_letter = models.FileField(null=True, blank=True, upload_to='letter_data_request', verbose_name='Unggah Surat Permohonan', validators=[FileExtensionValidator(allowed_extensions=["pdf"]), validators.validate_file_size])
   request_at = models.DateField(auto_now_add = True, editable=False)
   approved_at = models.DateField(null=True, blank=True, verbose_name='Tanggal Disetujui')
   show_state = models.CharField(max_length=1, choices = state, default="3", null=False, blank=False, verbose_name='Status Permohonan Data')

   def __str__(self):
      return f"{self.id} {self.name_person} | {self.agency_person} | {self.contact_person}"


class BackendPublicationsModel(models.Model):
    
   class Meta:
      verbose_name = 'Master Buku Publikasi' 
      verbose_name_plural = 'Master Buku Publikasi'
   
   state = (
      ('1', 'Ya'),
      ('2', 'Tidak')
    )

   title =  models.CharField(max_length=512, null=False, blank=False, verbose_name='Judul Publikasi')
   catalog_no = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nomor Catalog')
   publication_no = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nomor Publikasi')
   issn = models.CharField(max_length=50, null=True, blank=True, verbose_name='Nomor ISSN/ISBN')
   release = models.DateField(null=False, blank=False, verbose_name='Tanggal Release')
   abstract = models.TextField(null=False, blank=False, verbose_name='Abstrak')
   thumbnail = models.ImageField(null=True, blank=True, upload_to='thumbnail-publications', validators=[validators.validate_file_size], verbose_name='Thumbnail Publication')
   file = models.FileField(null=False, blank=False, upload_to='publications', verbose_name='File Publikasi', validators=[FileExtensionValidator(allowed_extensions=["pdf"]), validators.validate_publication_size])
   revision_log = models.IntegerField(null=False, blank=False, default=0)
   show_state = models.CharField(max_length=1, choices = state, null=False, blank=False, verbose_name='Tampilkan Publikasi')

   def __str__(self):
      return f"{self.id} {self.title} | {self.catalog_no} | {self.publication_no}"