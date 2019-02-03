from django.shortcuts import render

def landing_page(request):
    return render(request, 'management/landing_page.html')
