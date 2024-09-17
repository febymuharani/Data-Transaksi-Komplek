from django import forms
from .models import Transaksi

class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['anggota','tanggal','jenis_transaksi','jumlah','keterangan']


        