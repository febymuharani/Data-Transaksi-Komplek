from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Transaksi, Anggota
from .forms import TransaksiForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.db.models import Sum

@login_required
def index(request):
    total_pemasukan = Transaksi.objects.filter(jenis_transaksi='Pemasukan').aggregate(total=Sum('jumlah'))['total'] or 0
    total_pengeluaran = Transaksi.objects.filter(jenis_transaksi='Pengeluaran').aggregate(total=Sum('jumlah'))['total'] or 0

    context = {
        'total_pemasukan': total_pemasukan,
        'total_pengeluaran': total_pengeluaran,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def anggota(request):
    Nama = Anggota.objects.all()
    context = {
        'nama': Nama
    }
    return render(request, 'dashboard/anggota.html', context)

@login_required
def transaksi(request):
    items = Transaksi.objects.raw('SELECT * FROM dashboard_transaksi')

    if request.method == 'POST':
        form = TransaksiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-transaksi')
    else:
        form = TransaksiForm()

    context = {
        'items': items,
        'form': form
    }
    return render(request, 'dashboard/transaksi.html', context)

def TransaksiDelete(request, pk):
    Delete = Transaksi.objects.get(id=pk)
    if request.method == 'POST':
        Delete.delete()
        return redirect('dashboard-transaksi')
    return render(request, 'dashboard/transaksi_delete.html')

def TransaksiUpdate(request, pk):
    transaksi = Transaksi.objects.get(id=pk)
    if request.method == 'POST':
        form = TransaksiForm(request.POST, instance=transaksi)
        if form.is_valid():
            form.save()
            return redirect('dashboard-transaksi')
    else:
        form = TransaksiForm(instance=transaksi)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/transaksi_update.html', context)

def transaksi_dashboard(request):
    transaksi = Transaksi.objects.all()
    pengeluaran_total = transaksi.filter(jenis_transaksi='Pengeluaran').aggregate(total=models.Sum('jumlah'))['total'] or 0
    pemasukan_total = transaksi.filter(jenis_transaksi='Pemasukan').aggregate(total=models.Sum('jumlah'))['total'] or 0

    context = {
        'pengeluaran_total': pengeluaran_total,
        'pemasukan_total': pemasukan_total,
        'transaksi': transaksi,
    }
    return render(request, 'transaksi_dashboard.html', context)

@login_required
def generate_pdf(request, pk):
    transaksi = get_object_or_404(Transaksi, pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="transaksi_{pk}.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle('Transaksi Report')

    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Bukti Transaksi Pembayaran")

    headers = ['ID', 'Tanggal', 'Jenis Transaksi', 'Anggota', 'Jumlah', 'Keterangan']
    data = [
        headers,
        [
            str(transaksi.id),
            str(transaksi.tanggal),
            transaksi.jenis_transaksi,
            str(transaksi.anggota),
            str(transaksi.jumlah),
            transaksi.keterangan
        ]
    ]

    # Calculate column widths based on the length of data
    col_widths = []
    for i in range(len(headers)):
        # Find the maximum length of text in the column
        max_length = max(len(header) for header in headers)
        max_length = max(max_length, len(data[1][i]))
        # Apply a factor to convert text length to inches, adjust factor if needed
        col_widths.append((max_length + 2) * 0.25 * inch)  # Add extra space for padding

    table = Table(data)
    table.setStyle(TableStyle(
        [
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]
    ))

    width, height = letter
    table_width, table_height = table.wrapOn(pdf, width - 80, height - 150)
    table.drawOn(pdf, 40, height - table_height - 100)

    pdf.save()
    return response