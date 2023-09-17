from django.contrib import admin

from chambre.models import Chambre
from reservation.models import Reservation, HistoriqueReservation


# Register your models here.
admin.site.register(Chambre)
#admin.site.register(Reservation)
#admin.site.register(HistoriqueReservation)