from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, FormView, DeleteView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime

from .models import Table, Reservation
from .forms import AvailabilityForm

# Create your views here.


class ReservationList(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "reservation_list.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser:
            reservation_list = Reservation.objects.all()
            return reservation_list
        else:
            reservation_list = Reservation.objects.filter(
                user=self.request.user)
            return reservation_list


class ReservationView(LoginRequiredMixin, FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        table_list = Table.objects.all()
        available_tables = []
        for table in table_list:
            if check_availability(table, data['booking_date'], data['booking_time'], data['guests']):
                available_tables.append(table)

        if len(available_tables) > 0:
            table = available_tables[0]
            make_reservation = Reservation.objects.create(
                user=self.request.user,
                table=table,
                booking_date=data['booking_date'],
                booking_time=data['booking_time'],
                guests=data['guests']
            )
            make_reservation.save()
            return HttpResponse(make_reservation)
        else:
            return HttpResponse('No tables available')


def check_availability(table, booking_date, booking_time, guests):
    avail_list = []
    reservation_list = Reservation.objects.filter(table=table)
    for reservation in reservation_list:
        if reservation.booking_date == booking_date and reservation.booking_time == booking_time:
            avail_list.append(False)
    return all(avail_list)


def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    reservation.delete()
    messages.success(request, 'Your reservation has been cancelled!')
    return redirect(reverse('ReservationList'))


def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if request.method == 'POST':
        form = AvailabilityForm(
            request.POST, request.FILES, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your reservation has been successfully updated!')
            return redirect('ReservationList')
    else:
        form = AvailabilityForm(instance=reservation)

    template = 'reservation/edit_reservation.html'
    context = {
        'form': form,
        'reservation': reservation,
    }

    return render(request, template, context)
