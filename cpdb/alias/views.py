from elasticsearch import NotFoundError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import AliasSerializer
from .constants import ALIAS_MAPPINGS
from .utils import set_aliases
from shared.utils import formatted_errors


class AliasViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def update(self, request, alias_type, pk):
        try:
            doc_type_class, model_class = ALIAS_MAPPINGS[alias_type]
        except KeyError:
            return Response({f'message': f'Cannot find type "{alias_type}"'}, status=status.HTTP_404_NOT_FOUND)

        aliases = AliasSerializer(data=request.data)
        if not aliases.is_valid():
            return Response({'message': formatted_errors(aliases.errors)}, status=status.HTTP_400_BAD_REQUEST)

        validated_aliases = aliases.validated_data['aliases']
        try:
            set_aliases(doc_type_class, model_class, pk, validated_aliases)
        except (NotFoundError, model_class.DoesNotExist):
            return Response({
                'message': f'Cannot find any "{alias_type}" record with pk={pk}'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Aliases successfully updated', 'aliases': validated_aliases})
