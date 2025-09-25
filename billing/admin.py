from django.contrib import admin
from .models import Supplier, Item, Bill, BillItem, Expense

# Simple models
admin.site.register(Supplier)
admin.site.register(Item)


# Custom Bill admin
@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'created_at', 'created_by')
    list_filter = ('created_at', 'supplier')
    search_fields = ('supplier__name',)
    ordering = ('-created_at',)


@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = ('bill', 'item', 'quantity', 'unit_price', 'total', 'created_at')
    list_filter = ('created_at', 'bill')
    ordering = ('-created_at',)           # newest first


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'name', 'category', 'amount', 'note')
    list_filter = ('created_at', 'category')
    ordering = ('-created_at',)   