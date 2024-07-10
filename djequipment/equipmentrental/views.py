from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from equipmentrental.models import Equipment, Photo
from equipmentrental.cart import is_reserved


def index(request):
    session = request.session.session_key
    message = ''
    equipment = Equipment.objects.filter(status='ready').order_by('-id')
    reserved = Equipment.objects.none()
    for equip in equipment:
        if is_reserved(equip.id):
            reserv = Equipment.objects.filter(id=equip.id)
            reserved = reserved.union(reserv)
    equipment = equipment.difference(reserved)
    for equip in equipment:
        equip.photo = Photo.objects.filter(equipment=equip).first()

    paginator = Paginator(equipment, 3)
    page = request.GET.get('page')
    try:
        equipment = paginator.page(page)
    except PageNotAnInteger:
        equipment = paginator.page(1)
    except EmptyPage:
        equipment = paginator.page(paginator.num_pages)

    if not equipment:
        message = 'All equipments are reserved or booked, try again later.'
    context = {'equipments': equipment, 'message': message}
    return render(request, 'index.html', context)


def detail_equipment(request, equipment_id):
    equipment = Equipment.objects.get(id=equipment_id)
    photos = Photo.objects.filter(equipment=equipment)
    context = {'equipment': equipment, 'photos': photos}
    return render(request, 'detail_equipment.html', context)


