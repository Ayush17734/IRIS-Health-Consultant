
from django.db import models
from django.contrib.auth.models import User


from django.db import models
from django.contrib.auth.models import User
import datetime

class HealthTip(models.Model):
    date = models.DateField(default=datetime.date.today)
    tip = models.TextField()

    def __str__(self):
        return f"{self.date}: {self.tip}"

class MedicationReminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"


from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.CharField(max_length=10)  # 'user' or 'bot'
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.sender}: {self.message[:30]}"

