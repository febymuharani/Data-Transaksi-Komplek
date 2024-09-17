from django.db import models

# Create your models here.

class Anggota(models.Model):
    nama = models.CharField(max_length=100)  # Nama anggota
    alamat = models.TextField()  # Alamat anggota
    telpon = models.CharField(max_length=15)  # Nomor telepon anggota

    def __str__(self):
        return self.nama  # Menampilkan nama anggota saat mencetak objek

class Transaksi(models.Model):
    CATEGORY = [
        ('Pengeluaran', 'Pengeluaran'),
        ('Pemasukan', 'Pemasukan'),
    ]

    tanggal = models.DateField()  # Tanggal transaksi
    jenis_transaksi = models.CharField(
        max_length=20, 
        choices=CATEGORY
    )  # Jenis transaksi, menggunakan pilihan yang telah ditentukan
    anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)  # Hubungan dengan Anggota
    jumlah = models.IntegerField()  # Jumlah transaksi
    keterangan = models.TextField()  # Keterangan tambahan

    def __str__(self):
        return f"{self.jenis_transaksi} - {self.jumlah} pada {self.tanggal}"  # Format output yang lebih informatif
