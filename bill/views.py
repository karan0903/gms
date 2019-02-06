from django.shortcuts import render
from .forms import BillForm

def billNew(request):
    if request.method == 'POST':
        pass
    else:
        form = BillForm()
    return render(request, 'bill/bill.html', {'form':form})
