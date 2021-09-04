from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from addresses.api.serializers import AddressSerializer


class AddressApi(GenericViewSet):
    permission_classes = (IsAuthenticated,)

    @action(methods=['post'], detail=False)
    def add_address(self, request):
        data = request.data
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": serializer.data, "message": "Done", "status": True},
                            status=status.HTTP_201_CREATED)
        return Response({"result": serializer.errors, "message": "Done", "status": False},
                        status=status.HTTP_400_BAD_REQUEST)

