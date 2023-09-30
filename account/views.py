from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterRecruiterSerializer,RegisterUserSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ForgotPasswordCompleteSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from profilee.models import ProfileUser, ProfileRecruiter


User = get_user_model()


class RegisterRecruiterView(APIView):
    @swagger_auto_schema(request_body=RegisterRecruiterSerializer()) 
    def post(self, request):
        data = request.data
        serializer = RegisterRecruiterSerializer(data=data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()           
        return Response('Вы успешно зарегистрировались', status=201)
    
class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer()) 
    def post(self, request):
        data = request.data
        serializer = RegisterUserSerializer(data=data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()           
        return Response('Вы успешно зарегистрировались', status=201)

class ActivationRecruiterView(APIView):
    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response('Пользователь не найден', status=400)
        user.activation_code = ''
        user.is_active = True
        user.is_staff = True
        ProfileRecruiter.objects.create(user=user)  #=================================== фиксация
        user.save()
        return Response ('Аккаунт активирован', status =200)    
    



class ActivationUserView(APIView):
    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response('Пользователь не найден', status=400)
        user.activation_code = ''
        user.is_active = True
        ProfileUser.objects.create(user=user) #=================================== фиксация
        user.save()
        return Response ('Аккаунт активирован', status =200) 






class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('пароль успешно обновлен')





class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('Вам было отпавлено сообщение для восстановления')





class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Пароль успешно изменен')


