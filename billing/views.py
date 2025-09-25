from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Bill, Expense

@login_required
def user_dashboard(request):
    # if user picks a date, use it; else fallback to today
    picked_date = request.GET.get("date")
    if picked_date:
        try:
            date = timezone.datetime.strptime(picked_date, "%Y-%m-%d").date()
        except ValueError:
            date = timezone.now().date()
    else:
        date = timezone.now().date()

    bills = Bill.objects.filter(date=date)
    expenses = Expense.objects.filter(created_at=date)

    bills_total = sum(b.total for b in bills)
    expenses_total = sum(e.amount for e in expenses)

    context = {
        "bills": bills,
        "expenses": expenses,
        "bills_total": bills_total,
        "expenses_total": expenses_total,
        "date": date,
        "picked_date": picked_date or date.strftime("%Y-%m-%d")
    }
    return render(request, "user_dashboard.html", context)



def today_summary(request):
    today = timezone.now().date()
        
    bills = Bill.objects.filter(date=today)
    expenses = Expense.objects.filter(created_at=today)
    
    bills_total = sum(b.total for b in bills)
    expenses_total = sum(e.amount for e in expenses)
    
    context = {
        'bills': bills,
        'expenses': expenses,
        'bills_total': bills_total,
        'expenses_total': expenses_total,
        'today': today
    }
    return render(request, 'today_summary.html', context)


@login_required
def monthly_summary(request):
    now = timezone.now()
    month = request.GET.get("month")
    year = request.GET.get("year")

    if month and year:
        try:
            month = int(month)
            year = int(year)
        except ValueError:
            month = now.month
            year = now.year
    else:
        month = now.month
        year = now.year

    bills = Bill.objects.filter(date__year=year, date__month=month)
    expenses = Expense.objects.filter(created_at__year=year, created_at__month=month)

    bills_total = sum(b.total for b in bills)
    expenses_total = sum(e.amount for e in expenses)

    context = {
        "bills": bills,
        "expenses": expenses,
        "bills_total": bills_total,
        "expenses_total": expenses_total,
        "month": month,
        "year": year,
        "month_range": range(1, 13),             # 1 to 12
        "year_range": range(2023, 2031),         # example: 2023 to 2030
    }
    return render(request, "monthly_summary.html", context)