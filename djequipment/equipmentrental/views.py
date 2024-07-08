from django.shortcuts import render
from equipmentrental.models import Equipment, Photo


def index(request):
    equipment = Equipment.objects.filter(status='ready').order_by('-id')
    for equip in equipment:
        equip.photo = Photo.objects.filter(equipment=equip).first()

    context = {'equipments': equipment}
    return render(request, 'index.html', context)
