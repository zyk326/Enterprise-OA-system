### 重写User
1. 使用包放入创建的app,在settings里面加载app,覆盖AUTH_USER_MODEL, 拿django.contrib.auth.models里的User,拷贝重写字段,迁移至数据库,使用python manage.py createsuperuser创建超级用户.  
2. 添加数据初始化命令:  
在所述app下创建management(package)-commands(package)-(yourcommand).py,你要使用django.core.management.base的BaseCommand去写handle.  