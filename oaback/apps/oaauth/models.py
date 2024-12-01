from enum import unique

from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password
from shortuuidfield import ShortUUIDField

# 用户状态的三种选择
class UserStatusChoices(models.IntegerChoices):
    ACTIVED = 1
    UNACTIVE = 2
    LOCKED = 3

class OAUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, realname, email, password, **extra_fields):
        """
        创建用户
        """
        if not realname:
            raise ValueError("必须设置真实姓名!")
        email = self.normalize_email(email)
        user = self.model(realname=realname, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, realname, email=None, password=None, **extra_fields):
        """
        创建普通用户
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(realname, email, password, **extra_fields)

    def create_superuser(self, realname, email=None, password=None, **extra_fields):
        """
        创建超级用户
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("status", UserStatusChoices.ACTIVED)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("超级用户必须设置is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("超级用户必须设置is_superuser=True.")

        return self._create_user(realname, email, password, **extra_fields)

# Create your models here.
class OAUser(AbstractBaseUser, PermissionsMixin):
    """
    重写的用户类
    """
    uid = ShortUUIDField(primary_key=True)
    realname = models.CharField(max_length=150,unique=False)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True, blank=False)
    is_staff = models.BooleanField(default=True)
    status = models.IntegerField(default=UserStatusChoices.UNACTIVE, choices=UserStatusChoices)
    #只用关注status,无需is_active
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    department = models.ForeignKey('OADepartment', null=True, on_delete=models.SET_NULL, related_name='staffs', related_query_name='staffs')

    objects = OAUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"    # 这是用来鉴权的, 他会把值作为指定字段来做验证
    REQUIRED_FIELDS = ["realname", "password"] # 指定哪些字段必要, 其他FIELD中的除外

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.realname

    def get_short_name(self):
        return self.realname

    # 指定模型排序
    # class Meta:
    #     ordering = ['-data_joined']

class OADepartment(models.Model):
    name = models.CharField(max_length=100)
    intro = models.CharField(max_length=200)

    leader = models.OneToOneField(OAUser, null=True, on_delete=models.SET_NULL, related_name="leader_department", related_query_name="leader_department")
    manager = models.ForeignKey(OAUser, null=True, on_delete=models.SET_NULL, related_name="manager_department", related_query_name="manager_department")