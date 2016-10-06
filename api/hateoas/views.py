from collections import OrderedDict

from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination

class ExtraLinksAwarePageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data, links=[]):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('_links', links),
        ]))

def create_link(desc, href, method=None):
    result = {
        'desc': desc,
        'href': href,
    }
    if method:
        result['method'] = method

    return result

class HateoasListView(ListModelMixin, GenericViewSet):
    pagination_class = ExtraLinksAwarePageNumberPagination

    def get_list_links(self, request):
        return {}

    def get_paginated_response(self, data, links=None):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data, links)

    def linkify_list_data(self, request, data):
        return data

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.linkify_list_data(request, serializer.data)
            return self.get_paginated_response(data, links=self.get_list_links(request))

        serializer = self.get_serializer(queryset, many=True)
        data = self.linkify_list_data(request, serializer.data)

        return Response(OrderedDict([
            ('results', data),
            ('_links', self.get_list_links(request))
        ]))

class HateoasRetrieveView(RetrieveModelMixin, GenericViewSet):
    def get_retrieve_links(self, request, instance):
        return {}

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['_link'] = self.get_retrieve_links(request, instance)
        return Response(data)

class HateoasUpdateView(UpdateModelMixin, GenericViewSet):
    def get_retrieve_links(self, request, instance):
        return {}

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = serializer.data
        data['links'] = self.get_update_links(request, instance)
        return Response(data)

class HateoasCreateView(CreateModelMixin, GenericViewSet):
    def get_create_links(self, request, instance):
        return {}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data['_links'] = self.get_create_links(request, serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

class HateoasDestroyView(DestroyModelMixin, GenericViewSet):
    def get_destroy_links(self, request, instance):
        return {}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {'_links': self.get_destroy_links(request, instance)}
        self.perform_destroy(instance)
        return Response(data, status=status.HTTP_204_NO_CONTENT)
