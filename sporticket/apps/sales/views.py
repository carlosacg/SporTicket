from django.shortcuts import render


def index_sale(request):
    return render(request, 'sales/createSale.html')