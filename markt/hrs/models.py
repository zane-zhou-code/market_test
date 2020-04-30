from django.db import models

class Dept(models.Model):
    """部门类"""
    no = models.IntegerField(primary_key=True, db_column='dno', verbose_name='部门编号')
    name = models.CharField(max_length=20, db_column='dname', verbose_name='部门名称')
    location = models.CharField(max_length=10, db_column='dloc', verbose_name='部门所在地')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_dept'

class Emp(models.Model):
    """员工类"""
    no = models.IntegerField(primary_key=True, db_column='eno', verbose_name='员工编号')
    name = models.CharField(max_length=20, db_column='ename', verbose_name='员工姓名')
    job = models.CharField(max_length=10, verbose_name='职位')
    # 多对一外键关联（自参照）
    mgr = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='主管')
    sal = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='月薪')
    comm = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='补贴')
    # 多对一外键关联(参照部门模型)
    dept = models.ForeignKey(Dept, db_column='dno', on_delete=models.PROTECT, verbose_name='所在部门')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_emp'

class Subject(models.Model):
    """学科"""
    no = models.IntegerField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=20, verbose_name='名称')
    intro = models.CharField(max_length=511, default='', verbose_name='介绍')
    create_date = models.DateField(null=True, verbose_name='成立日期')
    is_hot = models.BooleanField(default=False, verbose_name='是否热门')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_subject'
        verbose_name = '学科'
        verbose_name_plural = '学科'


class Teacher(models.Model):
    """老师"""
    no = models.AutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=20, verbose_name='姓名')
    detail = models.CharField(max_length=1023, default='', blank=True, verbose_name='详情')
    photo = models.CharField(max_length=1023, default='', verbose_name='照片')
    good_count = models.IntegerField(default=0, verbose_name='好评数')
    bad_count = models.IntegerField(default=0, verbose_name='差评数')
    subject = models.ForeignKey(to=Subject, on_delete=models.PROTECT, db_column='sno', verbose_name='所属学科')

    class Meta:
        db_table = 'tb_teacher'
        verbose_name = '老师'
        verbose_name_plural = '老师'

class User(models.Model):
    """用户"""
    no = models.AutoField(primary_key=True, verbose_name='编号')
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='用户密码')
    email = models.CharField(max_length=35, verbose_name='邮箱')
    tel = models.IntegerField(max_length=20, verbose_name='手机号')
    # regdate = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'




