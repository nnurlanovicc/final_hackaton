from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Comment,Rating
from .serializers import CommentSerializer,RatingSerializer,FavoriteListSerializer,FavoriteCreateSerializer
from .permissions import IsAuthor
from rest_framework_simplejwt.authentication import JWTAuthentication


class FavoriteListView(ListAPIView):
    serializer_class= FavoriteListSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication]


    def get_queryset(self):
        return self.request.user.favorites.all()


class FavoriteDeleteView(DestroyAPIView):
    lookup_field_kwarg = 'pk'
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication]


    def get_queryset(self):
        return self.request.user.favorites.all()
    



















# class FavoriteCreateView(CreateAPIView):
#     serializer_class = FavoriteCreateSerializer
#     permission_classes = [IsAuthenticated,]
#     authentication_classes = [JWTAuthentication]


#     def perform_create(self,serializer):
#         serializer.save(author=self.request.user)