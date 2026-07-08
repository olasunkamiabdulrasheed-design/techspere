from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Event, EventRegistration


def event_list(request):
    upcoming = Event.objects.filter(is_active=True, event_date__gte=timezone.now())
    past = Event.objects.filter(is_active=True, event_date__lt=timezone.now())
    return render(request, 'events/event_list.html', {
        'upcoming': upcoming,
        'past': past,
    })


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_registered = False
    if request.user.is_authenticated:
        is_registered = EventRegistration.objects.filter(event=event, participant=request.user).exists()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered,
    })


@login_required
def event_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        event_type = request.POST.get('event_type')
        description = request.POST.get('description')
        location = request.POST.get('location')
        event_date = request.POST.get('event_date')
        prize = request.POST.get('prize')
        max_participants = request.POST.get('max_participants')

        if title and description and event_date:
            Event.objects.create(
                organizer=request.user,
                title=title,
                event_type=event_type,
                description=description,
                location=location,
                event_date=event_date,
                prize=prize,
                max_participants=max_participants or None,
            )
            return redirect('event_list')
    return render(request, 'events/event_create.html')


@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not event.is_full:
        EventRegistration.objects.get_or_create(event=event, participant=request.user)
    return redirect('event_detail', pk=event.pk)


@login_required
def event_unregister(request, pk):
    event = get_object_or_404(Event, pk=pk)
    EventRegistration.objects.filter(event=event, participant=request.user).delete()
    return redirect('event_detail', pk=event.pk)