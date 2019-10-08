from django.shortcuts import render

def about_us(request):
    return render(request, 'about_us.html')

def register(request):
    return render(request, 'register.html')

def protocol(request):
    return render(request, 'protocol.html')

def hello(request):
    return render(request, 'hello.html')
