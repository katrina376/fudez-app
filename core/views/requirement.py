from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins, status, parsers
from rest_framework.decorators import detail_route, list_route, permission_classes
from rest_framework.response import Response

from core.models import AdvanceRequirement, RegularRequirement
from core.serializers import AdvanceRequirementSerializer, SimpleAdvanceRequirementSerializer, FullAdvanceRequirementSerializer, RegularRequirementSerializer, SimpleRegularRequirementSerializer, FullRegularRequirementSerializer, ApproveSerializer, RejectSerializer

from .decorators import lock_if_submitted, pass_if_submitted
from .permissions import IsReviewer, IsRelatedOrReadOnly, IsOwnerOrReadOnly, IsApplicant


class AdvanceRequirementViewSet(viewsets.ModelViewSet):
    queryset = AdvanceRequirement.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsRelatedOrReadOnly)

    serializer_map = {
        'raw': AdvanceRequirementSerializer,
        'simple': SimpleAdvanceRequirementSerializer,
        'full': FullAdvanceRequirementSerializer,
    }

    def get_permissions(self):
        if self.action == 'create':
            return [IsApplicant()]
        elif self.action in ['update', 'partial_update', 'delete', 'submit']:
            return [IsOwnerOrReadOnly()]
        else:
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            if self.action == 'list':
                return self.serializer_map['simple']
            else:
                pk = self.kwargs['pk']
                instance = self.get_object()
                if IsRelatedOrReadOnly().has_object_permission(self.request, self, instance):
                    return self.serializer_map['full']
                else:
                    return self.serializer_map['simple']
        else:
            return self.serializer_map['raw']

    def get_serializer_context(self):
        return {'request': self.request}

    @lock_if_submitted
    def update(self, request, pk=None):
        return super(AdvanceRequirementViewSet, self).update(request, pk)

    @lock_if_submitted
    def partial_update(self, request, pk=None):
        return super(AdvanceRequirementViewSet, self).partial_update(request, pk)

    @lock_if_submitted
    def delete(self, request, pk=None):
        return super(AdvanceRequirementViewSet, self).delete(request, pk)

    @detail_route(methods=['patch'], url_path='submit', permission_classes=(IsOwnerOrReadOnly,))
    def submit(self, request, pk=None):
        requirement = get_object_or_404(self.get_queryset(), pk=pk)
        requirement.submit()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['patch'], url_path='approve', permission_classes=(IsReviewer,))
    @pass_if_submitted
    def approve(self, request, pk=None):
        requirement = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = ApproveSerializer(data=request.data, context=self.get_serializer_context())

        if serializer.is_valid():
            requirement.approve(**serializer.validated_data)
            return Response(status=status.HTTP_200_OK,
                            data={})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

    @detail_route(methods=['patch'], url_path='reject', permission_classes=(IsReviewer,))
    @pass_if_submitted
    def reject(self, request, pk=None):
        requirement = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = RejectSerializer(data=request.data, context=self.get_serializer_context())

        if serializer.is_valid():
            requirement.reject(**serializer.validated_data)
            return Response(status=status.HTTP_200_OK,
                            data={})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)


class RegularRequirementViewSet(AdvanceRequirementViewSet):
    queryset = RegularRequirement.objects.all()
    parser_classes = (parsers.MultiPartParser,
                      parsers.FormParser, parsers.JSONParser)

    serializer_map = {
        'raw': RegularRequirementSerializer,
        'simple': SimpleRegularRequirementSerializer,
        'full': FullRegularRequirementSerializer,
    }
