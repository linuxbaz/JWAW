from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import mixins, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from attendant.models import Student, Absent, School, Like, Document
from attendant.permissions import IsParentUser, IsManagerUser
from attendant.serializers import StudentApiSerializer, AbsentApiSerializer, SchoolApiSerializer, LikeApiSerializer, \
    DocumentApiSerializer, UserSerializer, CreateUserSerializer, LoginUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class AllPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class student_view(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentApiSerializer
    pagination_class = AllPaginator
    permission_classes = [IsAdminUser | IsManagerUser | IsParentUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class absent_view(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  GenericAPIView):
    queryset = Absent.objects.all()
    serializer_class = AbsentApiSerializer
    pagination_class = AllPaginator
    permission_classes = [IsAdminUser | IsManagerUser | IsParentUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class school_view(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  GenericAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolApiSerializer
    pagination_class = AllPaginator
    permission_classes = [IsAdminUser | IsManagerUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class like_view(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeApiSerializer
    pagination_class = AllPaginator
    permission_classes = [IsAdminUser | IsManagerUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class document_view(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    GenericAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentApiSerializer
    pagination_class = AllPaginator
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class register_view(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    GenericAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class login_view(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class user_view(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = AllPaginator
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


