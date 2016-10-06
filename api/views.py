from django.contrib.auth.models import User, Group
from api.models import *
from rest_framework import reverse, viewsets
from serializers import *
from hateoas.views import create_link, HateoasListView, HateoasRetrieveView


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MachineGroupViewSet(HateoasListView, HateoasRetrieveView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    def get_list_links(self, request):
        return [
            {
                'desc': 'Self',
                'href': request.build_absolute_uri(request.path),
                'method': 'GET',
            },
        ]

    def linkify_list_data(self, request, data):
        for machine in data:
            detail_link = request.build_absolute_uri(reverse('machine-detail', kwargs={'pk': machine['id']}))
            machine['_links'] = [
                create_link('Machine detail', detail_link, 'GET')
            ]
        return data

    def get_retrieve_links(self, request, instance):
        self_link = request.build_absolute_uri(request.path)
        signoff_link = request.build_absolute_uri(reverse('member-signoffs-list', kwargs={'machine_pk': instance.pk}))
        reservation_link =- request.build_absolute_uri(reverse('member-reservations-list', kwargs={'machine_pk': instance.pk}))

        return [
            create_link('Self', self_link, 'GET'),
            create_link('List of Reservations', reservation_link, 'GET'),
            create_link('List of Signoffs', signoff_link, 'GET'),
        ]

class MemberViewSet(HateoasListView, HateoasRetrieveView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get_list_links(self, request):
        return [
            {
                'desc':'Self',
                'href':request.build_absolute_uri(request.path),
                'method': 'GET'
            }
        ]

    def linkify_list_data(self, request, data):
        for member in data:
            detail_link = request.build_absolute_uri(reverse('member-detail', kwargs={'pk':member['pk']}))
            member['_links'] = [
                create_link('Member detail', detail_link, 'GET')
            ]
        return data

    def get_retrieve_links(self, request, instance):
        self_link = request.build_absolute_uri(request.path)
        signoff_link = request.build_absolute_uri(reverse('member-signoff-list', kwargs={'member_pk': instance.pk}))
        reservation_link = request.build_absolute_uri(reverse('member-reservation-list', kwargs={'member_pk':instance.pk}))

        return [
            create_link('Self', self_link, 'GET'),
            create_link('list of signoffs', signoff_link, 'GET'),
            create_link('list of reservations', reservation_link, 'GET')
        ]
