from django.urls import path
from .views import DashboardView, TransactionCreateView, ReportView, TransactionDeleteView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('transaction/new/', TransactionCreateView.as_view(), name='transaction_create'),
    path('transaction/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
    path('reports/', ReportView.as_view(), name='reports'),
]
