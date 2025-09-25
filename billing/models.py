from django.db import models
from  django.contrib.auth.models import User
from django.utils import timezone


class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False)
    contact_number = models.CharField(max_length=20, blank=False)
    address = models.TextField(blank=False)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.supplier.name})"


class Bill(models.Model):
    PAYMENT_CHOICES = [
        ('CASH', 'Cash'),
        ('CREDIT', 'Credit'),
    ]
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True, null=True, default=None)
    date = models.DateField(auto_now_add=True)  # the actual “bill day”

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='CASH')
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return sum(item.total for item in self.items.all())

    def __str__(self):
        return f"Bill {self.id} - {self.supplier.name} ({self.date})"



class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.item.name} x {self.quantity} (Bill {self.bill.id})"

    


class Expense(models.Model):
    created_at = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=200, blank=False)
    category = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.name}"
