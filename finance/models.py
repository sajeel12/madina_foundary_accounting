from django.db import models
from django.utils import timezone

class Category(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Cash In'),
        ('OUT', 'Cash Out'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Cash In'),
        ('OUT', 'Cash Out'),
    ]
    
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True)
    related_person = models.CharField(max_length=100, blank=True, null=True, help_text="Person money is going to or coming from")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.amount:.2f} on {self.date}"
