from rest_framework import mixins, viewsets

from .serializers import UserSerializer
from users.models import User
from .pagination import paginador_user

class UserListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    pagination_class = paginador_user
    def get_queryset(self):
        return User.objects.all()

class UserCRUDView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
