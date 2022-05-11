from django.contrib import admin

# Register your models here.
from DrugSearch.models import Lek, SzczegolyRefundacji

admin.site.register(Lek)
admin.site.register(SzczegolyRefundacji)