from django.contrib import admin
from .models import HealthTip, MedicationReminder,ChatMessage

admin.site.register(HealthTip)
admin.site.register(MedicationReminder)
admin.site.register(ChatMessage)