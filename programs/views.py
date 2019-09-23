from django.shortcuts import render


# Create your views here.
def secure_passwords(request):
    return render(request, 'programs/secure_passwords.html', {})


def malware(request):
    return render(request, 'programs/malware.html', {})
