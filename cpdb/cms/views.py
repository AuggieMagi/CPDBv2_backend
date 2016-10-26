from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination

from cms.models import SlugPage, ReportPage, FAQPage
from cms.serializers import ReportPageSerializer, FAQPageSerializer, get_slug_page_serializer


class CMSPageViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def retrieve(self, request, pk=None):
        queryset = SlugPage.objects.all()
        cms_page = get_object_or_404(queryset, pk=pk)
        serializer_class = get_slug_page_serializer(cms_page)
        serializer = serializer_class(cms_page)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = SlugPage.objects.all()
        cms_page = get_object_or_404(queryset, pk=pk)
        serializer_class = get_slug_page_serializer(cms_page)
        serializer = serializer_class(cms_page, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'message': serializer.errors}, status_code=status.HTTP_400_BAD_REQUEST)


class BaseIdPageViewSet(viewsets.ViewSet):
    def list(self, request):
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(self.queryset, request, view=self)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def partial_update(self, request, pk=None):
        cms_page = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(cms_page, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'message': serializer.errors}, status_code=status.HTTP_400_BAD_REQUEST)


class ReportPageViewSet(BaseIdPageViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = ReportPage.objects.all()
    serializer_class = ReportPageSerializer
    pagination_class = LimitOffsetPagination


class FAQPageViewSet(BaseIdPageViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = FAQPage.objects.all()
    serializer_class = FAQPageSerializer
    pagination_class = LimitOffsetPagination
