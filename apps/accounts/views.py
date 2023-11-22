from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist


# ثبت نام
# پارامتر ها : (
#       ایمیل
#       رمز عبور و تکرار آن
#       نام (اختیاری)
# نام خانوادگی(اختیاری)
# (
class RegisterView(APIView):
    def post(self, request):
        de_ser_data = CustomUserSerializer(data=request.POST)
        if de_ser_data.is_valid():
            # ثبت نام کاربر
            try:
                CustomUser.objects.create_user(
                    email_address=de_ser_data.validated_data['email_address'],
                    name=de_ser_data.validated_data['name'],
                    family=de_ser_data.validated_data['family'],
                    password=de_ser_data.validated_data['password']
                )
            except:
                CustomUser.objects.create_user(
                    email_address=de_ser_data.validated_data['email_address'],
                    password=de_ser_data.validated_data['password']
                )
            # ساخت توکن برای کاربر جدید
            try:
                user = CustomUser.objects.get(email_address=de_ser_data.validated_data['email_address'])
                user.is_active = True
                user.save()
                Token.objects.get_or_create(user=user)
                user_token = Token.objects.get(user_id=user.id)
            except ObjectDoesNotExist as error:
                return Response(error, status.HTTP_404_NOT_FOUND)
            # ارسال ایمیل حاوی نام کاربری و توکن
            try:
                register_email = Email.objects.get(slug='register')
                subject = register_email.subject
                message = register_email.message
            except ObjectDoesNotExist as error:
                return Response(error)

            html_content = render_to_string(
                'register.html',
                {
                    'email_address': de_ser_data.validated_data['email_address'],
                    'token': user_token,
                })
            send_to = [de_ser_data.validated_data['email_address']]
            register_email.send_email(subject, message, html_content, send_to)

            UserEmail.objects.create(
                user=user,
                email=register_email,
            )
            return Response(data=de_ser_data.data, status=status.HTTP_200_OK)
        else:
            return Response(data=de_ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


# _____________________________________________________________________

# ورود به حساب کاربری با کلید(توکن)
class LoginView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        ser_data = CustomUserSerializer(instance=user)

        # ارسال ایمیل حاوی پیام ورود به حساب کاربری
        try:
            login_email = Email.objects.get(slug='login')
            subject = login_email.subject
            message = login_email.message
        except ObjectDoesNotExist as error:
            return Response(error)
        html_content = render_to_string(
            'login.html',
            {
                'email_address': user.email_address,
            })
        send_to = [user.email_address]
        login_email.send_email(subject, message, html_content, send_to)
        UserEmail.objects.create(
            user=user,
            email=login_email,
        )
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


# تغییر رمز عبور
# پارامتر ها : (
#       کلید
#       رمز عبور و تکرار آن
# (
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        de_ser_data = ChangePasswordSerializer(data=request.POST)
        if de_ser_data.is_valid():
            # تغییر رمز عبور کاربر
            user = request.user
            new_password = de_ser_data.validated_data['password']
            user.set_password(new_password)
            user.save()

            # ارسال ایمیل حاوی پیام تغییر رمز عبور
            try:
                change_pass_email = Email.objects.get(slug='change-password')
                subject = change_pass_email.subject
                message = change_pass_email.message
            except ObjectDoesNotExist as error:
                return Response(error)
            html_content = render_to_string(
                'change_password.html',
                {
                    'email_address': user.email_address,
                })
            send_to = [user.email_address]
            change_pass_email.send_email(subject, message, html_content, send_to)
            UserEmail.objects.create(
                user=user,
                email=change_pass_email,
            )
            return Response('Your password has been successfully changed')
        else:
            return Response(de_ser_data.errors, status.HTTP_400_BAD_REQUEST)


# _____________________________________________________________________

# دریافت توکن جدید
# پارامتر ها : (
#       ایمیل
#       رمز عبور
# (
class RememberTokenView(APIView):
    def post(self, request):
        de_ser_data = RememberTokenSerializer(data=request.POST)
        if de_ser_data.is_valid():
            if CustomUser.objects.filter(email_address=de_ser_data.validated_data['email_address']).exists():
                user = authenticate(username=de_ser_data.validated_data['email_address'],
                                    password=de_ser_data.validated_data['password'])
                if user:
                    user_token = Token.objects.get(user=user)
                    Token.delete(user_token)
                    Token.objects.create(user=user)
                    new_token = Token.objects.get(user=user)
                    # ارسال ایمیل حاوی کلید جدید
                    try:
                        remember_token_email = Email.objects.get(slug='remember-token')
                        subject = remember_token_email.subject
                        message = remember_token_email.message
                    except ObjectDoesNotExist as error:
                        return Response(error)
                    html_content = render_to_string('remember_token.html',
                                                    {
                                                        'email_address': de_ser_data.validated_data['email_address'],
                                                        'new_token': new_token,
                                                    })
                    send_to = [user.email_address]
                    remember_token_email.send_email(subject, message, html_content, send_to)
                    UserEmail.objects.create(
                        user=user,
                        email=remember_token_email,
                    )
                    return Response(str(new_token), status=status.HTTP_200_OK)
                else:
                    return Response('username or password is incorrect', status.HTTP_400_BAD_REQUEST)
            else:
                return Response('user not found', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(de_ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
