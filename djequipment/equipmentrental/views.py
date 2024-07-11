from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from equipmentrental.models import Equipment, Photo, Booked
from equipmentrental.cart import is_reserved, users_cart, cart_get, cart_add, cart_remove
from equipmentrental.forms import BookingForm


def index(request):
    session = request.session.session_key
    message = ''
    equipment = Equipment.objects.filter(status='ready').order_by('id')
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
    reserved_until = cart_get(equipment.id)[1]
    photos = Photo.objects.filter(equipment=equipment)
    context = {'equipment': equipment, 'photos': photos, 'reserved_until': reserved_until}
    return render(request, 'detail_equipment.html', context)


def cart_view(request):
    session = request.session.session_key
    message = ''
    equipment = Equipment.objects.none()
    reserved = users_cart(session)
    if not reserved:
        message = f'User {session} You have not reserved any equipments.'
        context = {'message': message}
        return render(request, 'cart.html', context)
    for reserv in reserved:
        equip = Equipment.objects.filter(id=reserv['id']).filter(status='ready')
        equipment = equipment.union(equip)
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

    booked = Booked.objects.filter(sessionid=session)

    if not equipment:
        message = 'All equipments are reserved or booked, try again later.'
    context = {'equipments': equipment, 'message': message, 'reserved': reserved, 'booked': booked}
    return render(request, 'cart.html', context)


def add_cart(request, equipment_id):
    session = request.session.session_key
    cart_add(equipment_id, session)
    return redirect('cart')


def remove_cart(request, equipment_id):
    cart_remove(equipment_id)
    return redirect('cart')


def booking(request):
    session = request.session.session_key
    message = ''
    reserved = users_cart(session)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            comment = form.cleaned_data["comment"]
            if not reserved:
                message = f'User {session} You have not reserved any equipments.'
                context = {'message': message}
                return render(request, 'cart.html', context)
            for reserv in reserved:
                equipment = Equipment.objects.get(id=reserv['id'])
                booked = Booked(equipment=equipment, phone_number=phone_number, comment=comment, sessionid=session)
                booked.save()
                equipment.status = 'booked'
                equipment.save()
                return redirect('cart')
    else:
        form = BookingForm
    context = {'form': form}
    return render(request, 'booking.html', context)
