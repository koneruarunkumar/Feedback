from django.db import models

class ClientData(models.Model):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    user_id = models.CharField(max_length=20)
    fullName = models.CharField(max_length=40)
    email_id = models.EmailField(max_length=100)
    mobile = models.IntegerField()
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=30)

    # Make admin_code optional
    admin_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.fullName} ({self.user_type})"


class ClientFeedback(models.Model):
    Name = models.CharField(max_length=40)
    Concern = models.CharField(max_length=40)
    Help = models.CharField(max_length=40)
    YourFeedback = models.CharField(max_length=40)

    def __str__(self):
        return f"Feedback from {self.Name}"
