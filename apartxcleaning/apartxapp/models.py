from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_worker = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    doc_picture = models.ImageField(upload_to='doc_pictures', default='noavatar.jpg', blank=True)

    def __str__(self):
        return self.user.username


#Connection
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class FreeTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.TextField(blank=True)
    profession = models.CharField(max_length=255, default="Cleaner")
    city = models.CharField(max_length=255, default="Astana")
    price = models.IntegerField(blank=True, null=True)
    free_times = models.ManyToManyField(FreeTime, blank=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Photo(models.Model):
    image = models.ImageField(upload_to='photo_reports', blank=True)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, null=True, blank=True, on_delete=models.SET_NULL)
    time = models.DateTimeField()
    location = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    checklist = models.TextField()
    requested_by = models.ManyToManyField(Worker, related_name='requested_orders', blank=True)
    accepted = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    photofraud1 = models.ImageField(upload_to='photo_frauds', blank=True)
    photofraud2 = models.ImageField(upload_to='photo_frauds', blank=True)
    photofraud3 = models.ImageField(upload_to='photo_frauds', blank=True)
    photofraud4 = models.ImageField(upload_to='photo_frauds', blank=True)
    photoreport = models.ManyToManyField(Photo, blank=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id}"

