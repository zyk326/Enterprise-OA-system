# 环境配置
**前端：**    
**VsCode**
安装NVM  
npm create vue@3.10.3  
npm install vite-plugin-vue-setup-extend@0.4.0 --save-dev(name插件)  
vite.config.js里添加插件    
npm install axios@1.6.8 --save(axios请求库)  
配置.env.development文件   
npm install element-plus@2.7.0 --save(安装element-plus)  
npm install @wangeditor @wangeditor/editor-for-vue@5.1.23 --save(wangEditor5 富文本编辑器)  
npm install echarts@5.5.1 --save(安装前端图表echarts)  

---

**后端：**  
**PyCharm + Navicat + Another Redis Desktop Manager**
Python 3.12  
Django5  
restframework框架  
pip install django-cors-headers(跨域访问)   
pip install django-shortuuidfield(配置全球唯一字符串)  
pip install PyJWT(Token验证)  
pip install pillow(图片验证)  
pip install pycryptodome(邮件激活-aes加密)   
安装Redis [windows](https://github.com/tporadowski/redis/releases)(用作消息队列)   
>点击redis-server.exe运行    

pip install -U "celery[redis]"安装Celery(用作消费者)    
> 运行:Windows:celery -A [ProjectName] worker -l INFO  
> 运行:Linux:celery -A [ProjectName] worker -l INFO -P gevent   
>>pip install gevent(windows的celery支持库，使用windows运行celery需要安装gevent)     

pip install pandas(数据条目转换excel)  
pip install openpyxl(操作excel的支持库)    

### settings  
时区.  
数据库配置.  
安装rest_framework.  
关闭CSRF保护.  
配置中间件登录校验(手写校验,修改DRF的默认校验类)  
配置邮箱  
配置celery  
配置redis  

### 数据库  
Mysql:名称：zykoa(utf8mb4)  

### 测试超级用户
Email:zyk@barz.com  
Realname:郑友康  
Password:444444

---

# 部署  
### 本地部署  
**VMWare(CentOS/ubuntu-zykubuntu@me0)**  
> pro秘钥
>4A4RR-813DK-M81A9-4U35H-06KND  
>NZ4RR-FTK5H-H81C1-Q30QH-1V2LA  
>JU090-6039P-08409-8J0QH-2YR7F  
>4Y09U-AJK97-089Z0-A3054-83KLA  
>4C21U-2KK9Q-M8130-4V2QH-CF810  
>MC60H-DWHD5-H80U9-6V85M-8280D  

### linux
sudo apt-get install openssh-server(安装ssh服务)  
sudo service ssh start(启动ssh服务)   
apt install -y mysql-server-8.0 mysql-client(安装MySQL)  
apt install redis-server(安装redis)   
pip install -r requirements.txt(安装python依赖包,最好用虚拟环境)  
apt install ngnix(安装nginx)   
pip install uwsgi --ini uwsg.ini(安装uwsgi)   
 
47.120.78.236(公)  
172.22.38.222(私有)  
服务器要把端口打开        
更新源/etc/apt/sources.list => 清华源     
apt update更新内容      
/etc/resolv.conf => nameserver 8.8.8.8  

### 打包  
前端:  
npm run build

后端:  
添加settings里日志配置     
修改路由    
pip install django-environ(配置环境的包)      
配置uwsgi   
