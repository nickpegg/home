from django.contrib import admin
from models import *

class EventInline(admin.TabularInline):
    model = Event

class BeerAdmin(admin.ModelAdmin):
    inlines = [EventInline, ]
    
admin.site.register(Beer, BeerAdmin)

admin.site.register(Event)
admin.site.register(Tap)
admin.site.register(Fermenter)
