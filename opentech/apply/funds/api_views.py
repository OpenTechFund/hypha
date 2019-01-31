from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters import rest_framework as filters

from opentech.api.pagination import StandardResultsSetPagination
from opentech.apply.activity.models import Activity, COMMENT
from opentech.apply.activity.messaging import messenger, MESSAGES

from .models import ApplicationSubmission, RoundsAndLabs
from .serializers import (
    CommentSerializer,
    CommentCreateSerializer,
    RoundLabSerializer,
    SubmissionActionSerializer,
    SubmissionListSerializer,
    SubmissionDetailSerializer,
)
from .permissions import IsApplyStaffUser
from .workflow import PHASES


class RoundLabFilter(filters.ModelChoiceFilter):
    def filter(self, qs, value):
        if not value:
            return qs

        return qs.filter(Q(round=value) | Q(page=value))


class SubmissionsFilter(filters.FilterSet):
    round = RoundLabFilter(queryset=RoundsAndLabs.objects.all())
    status = filters.MultipleChoiceFilter(choices=PHASES)
    active = filters.BooleanFilter(method='filter_active')

    class Meta:
        model = ApplicationSubmission
        fields = ('status', 'round', 'active')

    def filter_active(self, value):
        if value is None:
            return qs

        if value:
            return qs.active()
        else:
            return qs.inactive()


class SubmissionList(generics.ListAPIView):
    queryset = ApplicationSubmission.objects.current()
    serializer_class = SubmissionListSerializer
    permission_classes = (
        permissions.IsAuthenticated, IsApplyStaffUser,
    )
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SubmissionsFilter
    pagination_class = StandardResultsSetPagination


class SubmissionDetail(generics.RetrieveAPIView):
    queryset = ApplicationSubmission.objects.all()
    serializer_class = SubmissionDetailSerializer
    permission_classes = (
        permissions.IsAuthenticated, IsApplyStaffUser,
    )


class SubmissionAction(generics.RetrieveAPIView):
    queryset = ApplicationSubmission.objects.all()
    serializer_class = SubmissionActionSerializer
    permission_classes = (
        permissions.IsAuthenticated, IsApplyStaffUser,
    )

    def post(self, request, *args, **kwargs):
        action = request.data.get('action')
        if not action:
            raise ValidationError('Action must be provided.')
        obj = self.get_object()
        try:
            obj.perform_transition(action, self.request.user, request=self.request)
        except DjangoPermissionDenied as e:
            raise PermissionDenied(str(e))
        return Response(status=status.HTTP_200_OK)


class RoundLabDetail(generics.RetrieveAPIView):
    queryset = RoundsAndLabs.objects.all()
    serializer_class = RoundLabSerializer
    permission_classes = (
        permissions.IsAuthenticated, IsApplyStaffUser,
    )

    def get_object(self):
        return super().get_object().specific

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['show_workflow'] = True
        return serializer_class(*args, **kwargs)


class RoundLabList(generics.ListAPIView):
    queryset = RoundsAndLabs.objects.specific()
    serializer_class = RoundLabSerializer
    permission_classes = (
        permissions.IsAuthenticated, IsApplyStaffUser,
    )
    pagination_class = StandardResultsSetPagination


class CommentFilter(filters.FilterSet):
    since = filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    before = filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = Activity
        fields = ['submission', 'visibility', 'since', 'before']


class CommentList(generics.ListAPIView):
    queryset = Activity.comments.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticated, IsApplyStaffUser,
    )
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CommentFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return super().get_queryset().visible_to(self.request.user)


class CommentListCreate(generics.ListCreateAPIView):
    queryset = Activity.comments.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (
        permissions.IsAuthenticated, IsApplyStaffUser,
    )
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('visibility',)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return super().get_queryset().filter(
            submission=self.kwargs['pk']
        ).visible_to(self.request.user)

    def perform_create(self, serializer):
        obj = serializer.save(
            type=COMMENT,
            user=self.request.user,
            submission_id=self.kwargs['pk']
        )
        messenger(
            MESSAGES.COMMENT,
            request=self.request,
            user=self.request.user,
            submission=obj.submission,
            related=obj,
        )
