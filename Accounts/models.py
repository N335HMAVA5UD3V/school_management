from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.core.validators import MinValueValidator

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('STAFF', 'Office Staff'),
        ('LIBRARIAN', 'Librarian'),
    ]
    full_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STAFF')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    address = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    guardian_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class LibraryHistory(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    book_name = models.CharField(max_length=200)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50, 
        choices=[('BORROWED', 'Borrowed'), ('RETURNED', 'Returned')]
    )

    def save(self, *args, **kwargs):
        # Automatically set return_date to 14 days after borrowed_date if not provided
        if not self.return_date:
            self.return_date = self.borrowed_date + timedelta(days=14)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book_title} - {self.student}"

class FeesHistory(models.Model):
    FEE_TYPE_CHOICES = [
        ('TUITION', 'Tuition Fee'),
        ('LIBRARY', 'Library Fee'),
        ('EXAM', 'Examination Fee'),
        ('SPORTS', 'Sports Fee'),
        ('MISC', 'Miscellaneous Fee'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('PARTIAL', 'Partial'),
    ]

    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    fee_type = models.CharField(
        max_length=50,
        choices=FEE_TYPE_CHOICES
    )
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_date = models.DateField()
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING'
    )

    def __str__(self):
        return f"{self.student} - {self.get_fee_type_display()} ({self.payment_status})"
