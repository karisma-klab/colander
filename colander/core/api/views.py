from django.http import Http404, HttpResponse
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from colander.core.api.serializers import (
    ArtifactSerializer,
    ArtifactTypeSerializer,
    CaseSerializer,
    DeviceSerializer,
    DeviceTypeSerializer,
    ObservableSerializer,
    ObservableTypeSerializer,
    PiRogueExperimentSerializer,
)
from colander.core.models import (
    Artifact,
    ArtifactType,
    Device,
    DeviceType,
    Observable,
    ObservableType,
    PiRogueExperiment,
    UploadRequest,
)
from colander.core.serializers.upload_request_serializers import UploadRequestSerializer


class ApiCaseViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CaseSerializer

    def get_queryset(self):
        queryset = self.request.user.all_my_cases
        # queryset = Case.objects.filter(case__in=cases)

        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class ApiDeviceTypeViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceTypeSerializer
    queryset = DeviceType.objects.all()


class ApiArtifactViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ArtifactSerializer

    def get_queryset(self):
        cases = self.request.user.all_my_cases
        return Artifact.objects.filter(case__in=cases)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    @action(detail=True)
    def download(self, request, pk):
        try:
            artifact = Artifact.objects.get(pk=pk, owner=request.user)
        except Artifact.DoesNotExist:
            raise Http404
        response = HttpResponse(artifact.file, content_type=artifact.mime_type)
        response['Content-Disposition'] = 'attachment; filename=' + artifact.name
        return response


class ApiArtifactTypeViewSet(mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ArtifactTypeSerializer
    queryset = ArtifactType.objects.all()


class ApiUploadRequestViewSet(mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "put"]
    serializer_class = UploadRequestSerializer

    def get_queryset(self):
        return UploadRequest.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class ApiDeviceViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       # mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        cases = self.request.user.all_my_cases
        queryset = Device.objects.filter(case__in=cases)

        case_id = self.request.query_params.get('case_id')
        if case_id is not None:
            queryset = queryset.filter(case=case_id)

        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class ApiPiRogueExperimentViewSet(mixins.CreateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  # mixins.UpdateModelMixin,
                                  mixins.ListModelMixin,
                                  GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PiRogueExperimentSerializer

    def get_queryset(self):
        cases = self.request.user.all_my_cases
        return PiRogueExperiment.objects.filter(case__in=cases)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class ApiObservableViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           # mixins.UpdateModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ObservableSerializer

    def get_queryset(self):
        cases = self.request.user.all_my_cases
        queryset = Observable.objects.filter(case__in=cases)

        case_id = self.request.query_params.get('case_id')
        if case_id is not None:
            queryset = queryset.filter(case=case_id)

        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class ApiObservableTypeViewSet(mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ObservableTypeSerializer
    queryset = ObservableType.objects.all()
