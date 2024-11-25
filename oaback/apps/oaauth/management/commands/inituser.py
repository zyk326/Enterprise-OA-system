from django.core.management import BaseCommand
from apps.oaauth.models import OAUser, OADepartment

class Command(BaseCommand):
    def handle(self, *args, **options):
        boarder = OADepartment.objects.get(name='董事会')
        developer = OADepartment.objects.get(name='产品开发部')
        operator = OADepartment.objects.get(name='运营部')
        saler = OADepartment.objects.get(name='销售部')
        hr = OADepartment.objects.get(name='人事部')
        finance = OADepartment.objects.get(name='财务部')

        # 1.东东:属于董事会的Leader
        dongdong = OAUser.objects.create_superuser(email="dongdong@qq.com", realname='东东', password='111111', department = boarder)
        # 2.多多:董事会
        duoduo = OAUser.objects.create_superuser(email="duoduo@qq.com", realname='多多', password='111111', department = boarder)
        # 3，张三:产品开发部的leader
        zhangsan = OAUser.objects.create_user(email="zhangsan@qq.com", realname='张三', password='111111', department = developer)
        # 4.李四:运营部leader
        lisi = OAUser.objects.create_user(email="lisi@qq.com", realname='李四', password='111111', department = operator)
        # 5.王五:人事部的leader
        wangwu = OAUser.objects.create_user(email="wangwu@qq.com", realname='王五', password='111111', department = hr)
        # 6.赵六:财务部的leader
        zhaoliu = OAUser.objects.create_user(email="zhaoliu@qq.com", realname='赵六', password='111111', department=finance)
        # 7.孙七:销售部的leader
        sunqi = OAUser.objects.create_user(email="sungi@qq.com", realname='孙七', password='111111', department = saler)

        boarder.leader = dongdong
        boarder.manager = None

        developer.leader = zhangsan
        developer.manager = dongdong

        operator.leader = lisi
        operator.manager = dongdong

        saler.leader = sunqi
        saler.manager = dongdong

        hr.leader = wangwu
        hr.manager = duoduo

        finance.leader = zhaoliu
        finance.manager = duoduo

        boarder.save()
        developer.save()
        operator.save()
        saler.save()
        hr.save()
        finance.save()

        self.stdout.write("初始化用户成功!")