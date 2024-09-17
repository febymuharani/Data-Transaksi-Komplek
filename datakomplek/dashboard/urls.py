from django.urls import path
from . import views 
from .views import  generate_pdf


urlpatterns = [
    path('dashboard/', views.index, name='dashboard-index'),
    path('anggota/', views.anggota, name='dashboard-anggota'),
    path('transaksi/', views.transaksi, name='dashboard-transaksi'),
    path('transaksi/delete/<int:pk>', views.TransaksiDelete, name='dashboard-transaksi-delete'),
    path('transaksi/update/<int:pk>', views.TransaksiUpdate, name='dashboard-transaksi-update'),
    path('generate_pdf/<int:pk>/', views.generate_pdf, name='generate_pdf'),
]