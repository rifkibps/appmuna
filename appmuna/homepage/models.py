from django.db import models

# Create your models here.
class DataRequestForm(models.Model):
   
   status = (
       ('0', 'Menunggu Persetujuan'),
       ('1', 'Memproses Permintaan Data'),
       ('2', 'Data Belum Tersedia (Belum Rilis)'),
       ('3', 'Permohonan Data Ditolak')
   )
   
   title = models.CharField(max_length=256, null=False, blank=False, verbose_name='Deskripsi Permohonan Data' )
   name_person = models.CharField(max_length=256, null=False, blank=False, verbose_name='Nama Pemohon')
   contact_person = models.CharField(max_length=15, blank=False, verbose_name='Kontak Pemohon')

   agency_person = models.CharField(max_length=256, blank=False, verbose_name='Instansi Pemohon')
   desc = models.TextField(null=False, blank=False, verbose_name='Deskripsi Data')
   app_letter = models.FileField(null=False, blank=False, upload_to='requst_form_letter', verbose_name='Surat Permohonan')
   request_at = models.DateTimeField(auto_now_add=True, editable=False)
   approved_at = models.DateTimeField(null=True, editable=False)
   status = models.CharField(max_length=1, choices=status, default=0, verbose_name='Status Permohonan')

   def __str__(self):
      return f"{self.desc} | {self.agency}"


class MessagesRequestData(models.Model):

   request = models.ForeignKey(DataRequestForm, on_delete=models.CASCADE,  related_name='msg_req_form')
   msg = models.CharField(max_length=15, blank=False, verbose_name='Pesan untuk Pemohon')

   def __str__(self):
      return f"{self.request.desc} [{self.msg}]"

class FAQModels(models.Model):

   class Meta:
      verbose_name = 'FAQ' 
      verbose_name_plural = 'FAQ'

   question = models.CharField(max_length=256, null=False, blank=False, verbose_name='Pertanyaan' )
   answer = models.TextField(null=False, blank=False, verbose_name='Jawaban')
   created_at = models.DateField(auto_now_add = True, editable=False)
   
   def __str__(self):
      return f"{self.pk}. {self.question}"
      