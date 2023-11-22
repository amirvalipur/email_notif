from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from jalali_date import date2jalali, datetime2jalali
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class CustomUserManager(BaseUserManager):
    def create_user(self, email_address, password, name=None, family=None):
        if not email_address:
            raise ValueError('آدرس ایمیل باید وارد شود')
        user = self.model(
            email_address=self.normalize_email(email_address),
            name=name,
            family=family
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email_address, password, name=None, family=None):
        user = self.create_user(
            email_address=email_address,
            name=name,
            family=family,
            password=password
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user


# _______________________________________________________________________________

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email_address = models.EmailField(unique=True, verbose_name='آدرس ایمیل')
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='نام')
    family = models.CharField(max_length=50, blank=True, null=True, verbose_name='نام خانوادگی')
    register_date = models.DateField(auto_now_add=True, verbose_name='تاریخ ثبت نام')
    is_active = models.BooleanField(default=False, verbose_name='فعال بودن')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین بودن')

    USERNAME_FIELD = 'email_address'
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email_address}'

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    @property
    def is_staff(self):
        return self.is_admin

    # تبدیل تاریخ میلادی به شمسی
    def convert_date_time(self):
        jalali_date = date2jalali(self.register_date).strftime('%Y/%m/%d')
        return jalali_date

    convert_date_time.short_description = 'تاریخ ثبت نام'


# _______________________________________________________________________________

class Email(models.Model):
    user = models.ManyToManyField(CustomUser, through='UserEmail')
    subject = models.CharField(max_length=100, verbose_name='موضوع')
    message = models.TextField(default='', verbose_name='متن', blank=True, null=True)
    slug = models.SlugField(max_length=50, null=True)

    def __str__(self):
        return f'{self.subject}'

    def send_email(self, subject, message, html_content, to):
        from_email = settings.EMAIL_HOST_USER
        message = EmailMultiAlternatives(subject, message, from_email, to)
        message.attach_alternative(html_content, 'text/html')
        message.send()

    class Meta:
        verbose_name = 'ایمیل'
        verbose_name_plural = 'ایمیل ها'


# _______________________________________________________________________________
class UserEmail(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_email1', verbose_name='کاربر',
                             null=True)
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='user_email2', verbose_name='ایمیل',
                              null=True)
    send_datetime = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال ایمیل')

    def convert_date_time(self):
        jalali_date = datetime2jalali(self.send_datetime).strftime('( %H:%M ) %Y/%m/%d')
        return jalali_date

    convert_date_time.short_description = 'زمان ارسال ایمیل'

    def __str__(self):
        return f'{self.user}\t{self.email}'

    class Meta:
        verbose_name = 'ایمیل ارسالی به کاربر'
        verbose_name_plural = 'ایمیل های ارسالی به کاربران'
