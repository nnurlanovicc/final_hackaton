from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import viewsets, filters
from .permissions import IsAuthor, IsReqruiter, IsAdmin
from .models import Post, Job_type,Job_level
from .serializers import PostListSerializer, PostDetailSerializer, Job_levelSerializer, Job_typeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from review.models import Like, FavoriteItem, Rating, Comment
from rest_framework.decorators import action
from review.serializers import LikeSerializer, FavoriteCreateSerializer, RatingSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from profilee.models import ProfileUser
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class Job_levelView(viewsets.ModelViewSet):
    queryset = Job_level.objects.all()
    serializer_class = Job_levelSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ('create','update','partial_update','destroy'):
            permissions = [IsAdmin]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class Job_typeView(viewsets.ModelViewSet):
    queryset = Job_type.objects.all()
    serializer_class = Job_typeSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ('create','update','partial_update','destroy'):
            permissions = [IsAdmin]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class PermissionMixin:
    def get_permissions(self):
        if self.action in ('create'):
            permissions = [IsAuthenticated, IsReqruiter]
        elif self.action in ('update','partial_update','destroy'):
            permissions = [IsAuthor]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]



class PostView(PermissionMixin,viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['vacancy','salary','experience']
    search_fields = ['vacancy','salary']
    ordering_fields = ['created_at', 'vacancy','actuality'] 
    
    @method_decorator(cache_page(60*2))
    def list(self,request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    


    @method_decorator(cache_page(60*0.75))
    def retrieve(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.views += 1
        post.save()
        serializer = self.get_serializer_class()(post)
        return Response(serializer.data, status=200)


    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = PostListSerializer
        return super().get_serializer_class()
        


    @action(methods=['POST'], detail=True,permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                like = Like.objects.get(post=post, author=user)
                like.delete()
                message = 'unlike'
            except Like.DoesNotExist:
                Like.objects.create(post=post, author=user)
                message = 'liked'
            return Response(message, status=201)
        

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        post = self.get_object()
        user = request.user
        serializer = FavoriteCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                fav_post = FavoriteItem.objects.get(post=post, author=user)
                fav_post.delete()
                message = 'deleted from favorites'
            except FavoriteItem.DoesNotExist:
                FavoriteItem.objects.create(post=post, author=self.request.user)
                message = 'added to favorites'
            return Response(message, status=201)
    
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
    

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def apply(self, request, pk=None):
        post = self.get_object()
        user_email = request.user.email
        resume = ProfileUser.objects.filter(user=request.user).first()
        user_resume = resume.user_resume.path 
        recruiter_email = post.author.email
        if post.actuality == True:
            try:
                subject = 'Отклик на ваканцию'
                message = f'Пользователь ITJOB: {user_email} отправил вам свое резюме'
                from_email = user_email
                recipient_list = [recruiter_email]

                email = EmailMessage(subject, message, from_email, recipient_list)
                email.attach_file(user_resume)
                email.send()

                return Response('Успешно отправлено', status=200)
            except Exception as e:
                return Response('Произошла ошибка при отправке электронной почты', status=500)
        else:
            return Response('ваканция не актуальна')



    @action(methods=['POST', 'PATCH'], detail=True, permission_classes=[IsAuthenticated])
    def rating(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if post.author == user:
            return Response('Автор поста не может оценивать свой собственный пост',status=400)
        try:
            rating = Rating.objects.get(post=post, author=user)
        except Rating.DoesNotExist:
            rating = None
        if request.method == 'POST':
            serializer = RatingSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                if rating:
                    return Response('Вы уже оставляли рейтинг для этого поста', status=400)
                serializer.save(post=post, author=user)
                return Response('Спасибо за рейтинг', status=201)
        elif request.method == 'PATCH':
            if not rating:
                return Response('Вы еще не оставляли рейтинг для этого поста', status=400)
            serializer = RatingSerializer(instance=rating, data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response('Рейтинг успешно обновлен', status=200)


    @action(methods=['POST', 'PATCH','DELETE'], detail=True, permission_classes=[IsAuthenticated])
    def comment(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            comment = Comment.objects.get(post=post,author=user)
        except Comment.DoesNotExist:
            comment = None
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save(post=post, author=user)
                return Response('Комментарий создан', status=201)
        elif request.method == 'PATCH':
            if not comment:
                return Response('Вы еще не оставляли комментарий для этого поста', status=400)
            serializer = CommentSerializer(instance=comment,data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response('Комментарий успешно обновлен', status=200)
        elif request.method == 'DELETE':
            if not comment:
                return Response('Вы еще не оставляли комментарий для этого поста', status=400)
            comment.delete()
            return Response('Комментарий успешно удален', status=204)





            



