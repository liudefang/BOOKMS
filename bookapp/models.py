from django.db import models
from django.contrib import admin
# Create your models here.
class Book(models.Model):
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = verbose_name

    isbn = models.CharField('ISBN', max_length=13, unique=True)
    title = models.CharField('书名', max_length=200)
    subtitle = models.CharField('副标题', max_length=200, blank=True)
    pages = models.IntegerField('页数', blank=True)
    author = models.CharField('作者', max_length=60)
    translator = models.CharField('译者', max_length=60, blank=True)
    price = models.CharField('定价', max_length=60, blank=True)
    publisher = models.CharField('出版社', max_length=200, blank=True)
    pubdate = models.CharField('出版日期', max_length=60, blank=True)
    cover_img = models.URLField('封面图', blank=True)
    summary = models.TextField('内容简介', blank=True, max_length=2000)
    author_intro = models.TextField('作者简介', blank=True, max_length=2000)
    create_time = models.DateField(auto_now=True)  # 创建时间（取当前系统时间）
    def __str__(self):
        return self.title

class Reader(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)            # 关联借书id
    account = models.CharField(max_length=64, blank=True)  # 账号
    name = models.CharField(max_length=64, blank=True)  # 姓名
    email = models.CharField(max_length=128, blank=True)  # 邮箱
    contact = models.IntegerField(max_length=16, blank=True)  # 联系方式
    status = models.IntegerField('借书状态', blank=True)  # 借书状态（0、未借书，1、借书，2、归还）
    Borrowbooks_time = models.DateField(auto_now=True)  # 借书时间（自动获取当前时间）
    Backbook_time = models.DateField()

    class Meta:
        unique_together = ("book", "account")
    def __str__(self):
        return self.email

class User(models.Model):
    account = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()

class UserAdmin(admin.ModelAdmin):
    list_display = ('account','password','email')

admin.site.register(User,UserAdmin)
