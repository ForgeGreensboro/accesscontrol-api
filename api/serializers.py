from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import models

from theforge import relations, profiles

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Member
        fields = ('memberId', 'cardToken', 'reservations', 'signOffs')

class MachineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Machine
        fields = ('requiresSignOff', 'reservations')

class SignOffSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SignOff
        fields = ('level')

class ShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Shop
        fields = ('description')

class LockOutSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.LockOut
        fields = ('lockOutDate', 'lockOutPerson')

class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Reservation
        fields = ('reservationStart', 'reservationEnd')
