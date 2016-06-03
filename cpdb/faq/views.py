from rest_framework import viewsets
from rest_framework.response import Response

from faq.models import FAQPage
from faq.serializers import FAQSerializer


class FAQViewSet(viewsets.GenericViewSet):
    queryset = FAQPage.objects.all()
    serializer_class = FAQSerializer

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):  # pragma: no cover
        pass

    def get_serializer_context(self):
        return {
            'request': self.request,
            'view': self
        }