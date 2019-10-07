
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from clients.models import Client
import datetime


class Member(models.Model):

    SECTORS = [
        (0, ''),
        (10, 'Institution Chef'),
        (12, 'Banqueting Chef'),
        (20, 'Pub Chef'),
        (25, 'GastroPub Chef'),
        (35, 'Fine Dining Level Chef'),
        (50, 'Rosette Level Chef'),
        (80, 'Michelin Level Chef'),
    ]

    LEVELS = [
        (0, ''),
        (1, 'Demi Chef'),
        (2, 'CDP  Chef'),
        (3, 'Sous Chef'),
        (4, 'Head Chef'),
        (5, 'Exec Chef'),
    ]

    YEARS = [
        (i, i) for i in range(1, 41)
    ]

    member = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=24, blank=True)
    phone = models.CharField(max_length=48, blank=True)
    sector = models.IntegerField(choices=SECTORS, default=0)
    level = models.IntegerField(choices=LEVELS, default=0)
    years = models.IntegerField(choices=YEARS, default=0)
    score = models.IntegerField(null=True)
    bio = models.TextField(max_length=540, blank=True)
    join_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.member.username}, {self.member.first_name} {self.member.last_name}, {self.nickname}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Member.objects.create(member=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.member.save()


class Job(models.Model):

    STATUS = (
        ('<i class="fas fa-hourglass-end mr-2 text-success fa-lg"></i>', 'Pending Agreement'),
        ('<i class="far fa-check-circle mr-2 text-success fa-lg"></i>', 'Available'),
        ('<i class="far fa-times-circle mr-2 text-secondary fa-lg"></i>', 'Filled'),
        ('<i class="far fa-check-circle mr-2 text-warning fa-lg"></i>', 'Partially Filled'),
        ('<i class="fas fa-calendar-times mr-2 text-danger fa-lg"></i>', 'Expired'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    google_maps = models.URLField()

    job_role = models.CharField(max_length=48)
    job_start_date = models.DateField()

    job_pay_rate = models.FloatField()
    job_pay_period = models.CharField(max_length=48)

    job_desc = models.TextField(max_length=320)
    job_status = models.CharField(
        max_length=180,
        choices=STATUS,
        default='Available',
    )

    job_created = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.client}, {self.job_role}, {self.job_created.strftime("%d/%b/%Y")}'
