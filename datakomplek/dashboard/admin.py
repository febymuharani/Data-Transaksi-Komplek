from django.contrib import admin
from .models import Anggota, Transaksi
from django.contrib.auth.models import Group
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def download_pdf(modeladmin, request, queryset):
    model_name = modeladmin.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={model_name}.pdf'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle('PDF Report')

    # Menambahkan teks "Bukti Transaksi Pembayaran"
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Bukti Transaksi Pembayaran")

    # Menyiapkan data untuk tabel
    headers = [field.verbose_name for field in modeladmin.model._meta.fields]
    data = [headers]

    for obj in queryset:
        data_row = [str(getattr(obj, field.name)) for field in modeladmin.model._meta.fields]
        data.append(data_row)

    # Menambahkan tabel ke PDF
    table = Table(data)
    table.setStyle(TableStyle(
        [
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]
    ))

    width, height = letter
    table_width, table_height = table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 40, height - table_height - 100)  # Penyesuaian posisi tabel dengan ruang untuk teks

    pdf.save()
    return response

download_pdf.short_description = "Download Selected Items as PDF."

@admin.register(Anggota)
class AnggotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'alamat', 'telpon')

@admin.register(Transaksi)
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('id', 'tanggal', 'jenis_transaksi', 'anggota', 'jumlah', 'keterangan')
    actions = [download_pdf]

admin.site.unregister(Group)
admin.site.site_header = 'FEBY MUHARANI'
