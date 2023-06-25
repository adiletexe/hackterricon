from django.contrib import admin
from .models import UserProfile, Customer, Worker, Order, FreeTime

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(Worker)
admin.site.register(Order)
admin.site.register(FreeTime)