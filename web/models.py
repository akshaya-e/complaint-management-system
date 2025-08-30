from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

#from django.utils import timezone


# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    personal_details = models.TextField(blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Customer(models.Model):
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=150, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2, help_text="%")

    def __str__(self):
        return self.name

class Complaint(models.Model):
    LEVEL_CHOICES = [("L1", "Level 1"), ("L2", "Level 2"), ("L3", "Level 3")]
    STATUS_PENDING = "pending"
    STATUS_CLOSED = "closed"
    STATUS_NOT_CLOSED = "not_closed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CLOSED, "Closed"),
        (STATUS_NOT_CLOSED, "Not Closed"),
    ]
    #STATUS_CHOICES = [("PENDING","Pending"), ("CLOSED","Closed"), ("NOT_CLOSED","Not Closed")]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default="L1")
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    assigned_to = models.OneToOneField(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="PENDING")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_complaints")
    created_at = models.DateTimeField(auto_now_add=True)
    #reassigned = models.BooleanField(default=False)
    
    '''def save(self, *args, **kwargs):
        if self.pk:  # Check if this complaint already exists
            orig = Complaint.objects.get(pk=self.pk)
            if orig.assigned_to and self.assigned_to != orig.assigned_to:
                raise ValidationError("This complaint is already assigned and cannot be reassigned.")
        super().save(*args, **kwargs)'''

    def __str__(self):
        return f"Complaint #{self.pk} - {self.customer} - {self.product}"



    

class Remark(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="remarks")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Remark on {self.complaint} by {self.user}"
    

class ComplaintUpdate(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CLOSED", "Closed"),
        ("NOT_CLOSED", "Not Closed"),
    ]
    complaint = models.ForeignKey("Complaint", on_delete=models.CASCADE, related_name="updates")
    remark = models.TextField()
    status_snapshot = models.CharField(max_length=12, choices=STATUS_CHOICES)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for Complaint #{self.complaint.pk} at {self.created_at}"
