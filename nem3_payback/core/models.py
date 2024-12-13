from django.db import models

class UserUpload(models.Model):
    user_email = models.EmailField()  # For tracking the user's email
    file = models.FileField(upload_to='uploads/')  # File upload
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp

class SystemConfiguration(models.Model):
    battery_capacity_kwh = models.DecimalField(max_digits=6, decimal_places=3)
    solar_panel_capacity_kw = models.DecimalField(max_digits=6, decimal_places=3)
    user_upload = models.ForeignKey(UserUpload, on_delete=models.CASCADE)  # Relationship
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

class RateSchedule(models.Model):
    hour = models.IntegerField()
    rate_code = models.CharField(max_length=10)
    rate_dollars_kwh = models.DecimalField(max_digits=6, decimal_places = 4)

class Results(models.Model):
    nem_version = models.CharField(max_length=10)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    rate_code = models.CharField(max_length=10)

class HourlyReading(models.Model):
    type = models.CharField(max_length=10)# Generation
    timestamp = models.DateTimeField(null = True)
    start_interval = models.DateTimeField(null = True)
    end_interval = models.DateTimeField(null = True)
    reading_kwh = models.DecimalField(max_digits=6, decimal_places = 4)
