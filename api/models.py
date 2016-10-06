from __future__ import unicode_literals

from django.db import models

SIGN_OFF_LEVELS = (
    ('NONE', 'Not Signed Off'),
    ('SOLO', 'Can Use Without Supervision'),
    ('SUPERVISED', 'Can Use With Supervision'),
    ('DEPARTMENTHEAD', 'Can Use Without Supervision & Grant Sign Offs')
)

class Shop(models.Model):
    description = models.CharField(max_length=50, blank=False)

class Machine(models.Model):
    macAddress = models.CharField(max_length=6, unique=True, blank=False, db_index=True)
    requiresSignOff = models.BooleanField(default=False)
    description = models.CharField(max_length=50, blank=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

class Member(models.Model):
    cardToken = models.CharField(max_length=36, unique=True, db_index=True)
    signOffs = models.ManyToManyField(Machine, through='SignOff', related_name='signoff')
    reservations = models.ManyToManyField(Machine, through='Reservation', related_name='reservations')
    memberId = models.CharField(max_length=36, unique=True, db_index=True)

class SignOff(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE,related_name="signoff_member_machine")
    level = models.CharField(max_length=20, choices=SIGN_OFF_LEVELS)

class LockOut(models.Model):
    lockOutPerson = models.ForeignKey(Member, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    lockOutDate = models.DateTimeField(blank=False)
    reason = models.TextField(blank=False)

class Reservation(models.Model):
    reservationStart = models.DateTimeField(blank=False)
    reservationEnd = models.DateTimeField(blank=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="reservation_machine")

