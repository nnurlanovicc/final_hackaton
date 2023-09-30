from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .tasks import send_activation_code_celery_to_recruiter,send_activation_code_celery_to_user
# from .utils import send_activation_code_to_recruiter, send_activation_code_to_user

User = get_user_model()


class RegisterRecruiterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=4, required=True)

    class Meta:
        model  = CustomUser
        fields = ('email', 'password', 'password_confirm',)


    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop ('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError ('Пароли не совпадают')
        return attrs


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # send_activation_code_to_recruiter(user.email, user.activation_code)
        send_activation_code_celery_to_recruiter.delay(user.email, user.activation_code)
        return user
    

class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=4, required=True)

    class Meta:
        model  = CustomUser
        fields = ('email', 'password', 'password_confirm',)


    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop ('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError ('Пароли не совпадают')
        return attrs


    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        # send_activation_code_to_user(user.email, user.activation_code)
        send_activation_code_celery_to_user.delay(user.email, user.activation_code)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=4, required=True)
    new_password = serializers.CharField(min_length=4, required=True)
    new_password_confirm = serializers.CharField(min_length=4, required=True)

    def validate_old_password(self, old_password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Введите корректный пароль')
        return old_password
    
    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        if new_password == old_password:
            raise serializers.ValidationError('Старый и новый пароли совпадают')
        return attrs
    
    def set_new_password(self):
        new_passwords = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_passwords)
        user.save()


    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Такого пользователя нет')
        return email

    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.save()
        send_mail(
            'Восстановление пароля',
            f'Ваш код восстановления: {user.activation_code}',
            'from_nurs@gmail.com',
            [user.email]
        )


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirm')

        if not User.objects.filter(email=email,activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден или неправильный код')
        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()
        


'=============================================  последняя фиксация ============================================='
