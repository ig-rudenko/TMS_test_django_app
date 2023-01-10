from django.shortcuts import render


def custom_handler404(request, *args, **kwargs):
    return render(request, "errors/404.html")
