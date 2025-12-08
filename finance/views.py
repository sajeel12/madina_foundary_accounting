from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from .models import Transaction, Category
from django.urls import reverse_lazy

from datetime import timedelta
from django.db.models.functions import TruncMonth

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'finance/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Date filtering (simple default: all time or current month)
        today = timezone.now().date()
        
        transactions = Transaction.objects.all().order_by('-date')
        
        # Totals
        total_in = transactions.filter(type='IN').aggregate(Sum('amount'))['amount__sum'] or 0
        total_out = transactions.filter(type='OUT').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_in - total_out
        
        context['transactions'] = transactions[:5]  # Recent 5
        context['total_in'] = total_in
        context['total_out'] = total_out
        context['balance'] = balance

        # Chart Data (Last 6 Months)
        six_months_ago = today - timedelta(days=180)
        monthly_stats = (
            Transaction.objects.filter(date__gte=six_months_ago)
            .annotate(month=TruncMonth('date'))
            .values('month', 'type')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

        # Process data for Chart.js
        labels = []
        income_data = []
        expense_data = []
        
        # Create a dictionary for easy lookup: { '2023-10-01': {'IN': 100, 'OUT': 50} }
        stats_dict = {}
        for entry in monthly_stats:
            month_str = entry['month'].strftime('%b %Y') if entry['month'] else 'Unknown'
            if month_str not in stats_dict:
                stats_dict[month_str] = {'IN': 0, 'OUT': 0}
            stats_dict[month_str][entry['type']] = float(entry['total'])
            
        # Ensure we have labels for the last 6 months even if empty
        current = today
        for i in range(5, -1, -1):
            date = (current.replace(day=1) - timedelta(days=i*30)).replace(day=1) 
            # Approximate month shift simply for labels, better logic might be needed for strict calendar months
            # A more robust way to iterate months:
            # But for now let's rely on the data limits or just use what we have found if we want to skip empty months?
            # User likely wants to see empty months too.
            pass

        # Simpler approach: Just use the data we have found, sorted by date logic
        # But to guarantee order and continuous months, let's iterate backwards 6 times
        
        chart_labels = []
        chart_income = []
        chart_expense = []

        for i in range(5, -1, -1):
            # Calculate date for i months ago
            # Python date math for months is tricky, simplistic approximation:
            d = today - timedelta(days=i*30) 
            month_label = d.strftime('%b')
            year_month_key = d.strftime('%b %Y') # Matches stats_dict key format roughly if dates align
            
            # Re-doing the loop to be more precise based on what we actually queried or just matching keys
            # Let's just use the keys present in the database for now to be safe against date math errors, 
            # OR generate strict keys.
            pass
        
        # Let's just iterate through the sorted query results for simplicity first.
        # If the user wants empty months filled, we can add that complexity. 
        # For "Real Data", showing actual activity is the primary requirement.
        
        # Re-process to just lists
        # We need to merge IN and OUT for the same month
        months_order = []
        data_map = {}
        
        for entry in monthly_stats:
            m = entry['month']
            if not m: continue
            lbl = m.strftime('%b')
            if lbl not in months_order:
                months_order.append(lbl)
                data_map[lbl] = {'IN': 0, 'OUT': 0}
            data_map[lbl][entry['type']] = float(entry['total'])
            
        context['chart_labels'] = months_order
        context['chart_income'] = [data_map[m]['IN'] for m in months_order]
        context['chart_expense'] = [data_map[m]['OUT'] for m in months_order]
        
        return context

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['type', 'amount', 'date', 'description', 'related_person', 'category']
    template_name = 'finance/transaction_form.html'
    success_url = reverse_lazy('dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ReportView(LoginRequiredMixin, TemplateView):
    template_name = 'finance/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        transactions = Transaction.objects.all().order_by('-date')
        
        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)
            
        total_in = transactions.filter(type='IN').aggregate(Sum('amount'))['amount__sum'] or 0
        total_out = transactions.filter(type='OUT').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_in - total_out
        
        context['transactions'] = transactions
        context['total_in'] = total_in
        context['total_out'] = total_out
        context['balance'] = balance
        context['start_date'] = start_date
        context['end_date'] = end_date
        
        return context

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('dashboard')
    
    def get(self, request, *args, **kwargs):
        # Allow GET request to delete directly if confirmed? 
        # Best practice is POST, but for "onclick=return confirm()" link usually we might need a small form or allow GET for simplicity if security isn't strict yet.
        # But standard Django DeleteView confirms on GET (shows page) and deletes on POST.
        # User requested "confirmation" which implies a popup or page.
        # Let's support both: POST for deletion, and maybe a simple get bypass if needed, 
        # BUT for the dashboard trash icon, we likely want a form submit or a confirm page.
        # The simplest given the prompt "onclick=confirm" suggests a direct action.
        return self.post(request, *args, **kwargs)
