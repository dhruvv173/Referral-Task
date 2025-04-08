from django.db import models
import uuid

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=15, unique=True)
    city = models.CharField(max_length=30)
    referral_code = models.CharField(max_length=10, unique=True, blank=True)
    referred_by = models.ForeignKey('self', null = True, blank = True, on_delete=models.SET_NULL)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)
    
    def generate_referral_code(self):
        return str(uuid.uuid4())[:8].upper()
    
    def __str__(self):
        return self.email