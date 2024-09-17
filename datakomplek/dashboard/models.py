from django.db import models

# Create your models here.

class Anggota(models.Model):
    nama = models.CharField(max_length=100)  
    alamat = models.TextField()  
    telpon = models.CharField(max_length=15)  

    def __str__(self):
        return self.nama  

class Transaksi(models.Model):
    CATEGORY = [
        ('Pengeluaran', 'Pengeluaran'),
        ('Pemasukan', 'Pemasukan'),
    ]

    tanggal = models.DateField()  
    jenis_transaksi = models.CharField(
        max_length=20, 
        choices=CATEGORY
    ) 
    anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE) 
    jumlah = models.IntegerField()
    keterangan = models.TextField()  

    def __str__(self):
        return f"{self.jenis_transaksi} - {self.jumlah} pada {self.tanggal}" 
