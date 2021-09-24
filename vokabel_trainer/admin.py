from django.contrib import admin

from vokabel_trainer.models import Liste, Vokabel, Abfrage

# Register your models here.
admin.site.register(Liste)

admin.site.register(Vokabel)

admin.site.register(Abfrage)