#coding=utf-8
import UserProfile as UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.paginator import Paginator
from django.shortcuts import *
from django.http import HttpResponse
from django import forms
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
# Create your views here.
from django.template import RequestContext
from django.template.loader import get_template
from tornado.platform.twisted import _

from bookapp.forms import *
from bookapp.models import User

#创建图书
def create_book(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = BookForm()
    t = get_template('bookapp/create_book.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

#图书列表
def list_book(request):
    list_items = Book.objects.all()
    paginator = Paginator(list_items,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except:
        list_items = paginator.page(paginator.num_pages)

    t = get_template('bookapp/list_book.html')
    c = RequestContext(request.locals())
    return HttpResponse(t.render(c))

#查找图书
def search_book(request,query):
    search_items = Book.objects.filter(title__contains=query)
    paginator = Paginator(search_items,10)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        search_items = paginator.page(page)
    except:
        search_items = paginator.page(paginator.num_pages)
    t = get_template('bookapp/search_book.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

#管理图书
def manage_book(request):
    list_items = Book.objects.all()
    paginator = Paginator(list_items,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except:
        list_items = paginator.page(paginator.num_pages)

    t = get_template('bookapp/manage_book.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

#图书列表
def list_book(request):
    form = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST.copy())
        if form.is_valid():
            if(True == _login(request,form.cleaned_data["username"],form.cleaned_data["password"])):
                return HttpResponseRedirect('/bookapp/book/list/')

    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST.copy())
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(username,email,password)
            user.save()
            _login(request,username,password)  #注册完毕，直接登录
            return HttpResponseRedirect('/bookapp/book/list/')

        form = SearchForm()
        if request.method == "POST":
            form = SearchForm(request.POST.copy())
            if form.is_valid():
                query = form.cleaned_data["query"]
                search_items = Book.objects.filter(title__contains=query)

                paginator = Paginator(search_items,10)
                try:
                    page = int(request.GET.get('page','1'))
                except ValueError:
                    page = 1
                try:
                    search_items = paginator.page(page)
                except:
                    search_items = paginator.page(paginator.num_pages)
                t = get_template('bookapp/search_book.html')
                c = RequestContext(request,locals())
                return HttpResponse(t.render(c))

        list_items = Book.objects.all()
        paginator = Paginator(list_items,10)
        try:
            page = int(request.GET.get('page','1'))
        except ValueError:
            page = 1

        try:
            list_items = paginator.page(page)
        except:
            list_items = paginator.page(paginator.num_pages)

        t = get_template('bookapp/list_book.html')
        c = RequestContext(request,locals())
        return HttpResponse(t.render(c))

#查看图片
def view_book(request,id):
    item = Book.objects.get(id=id)
    t = get_template('bookapp/view_book.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))
#编辑图书
def edit_book(request,id):
    book_instance = Book.objects.get(id=id)
    form = BookForm(request.POST or None,instance = book_instance)

    if form.is_valid():
        form.save()

    t = get_template('bookapp/edit_book.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

#================================================================================================
#欢迎页
def welcome(request):
    t = get_template('welcome.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

def index(request):
    '''页面视图'''
    template_var = {"w":('欢迎您,游客!')}
    if request.user.is_authenticated():
        template_var["w"] = _("欢迎您%s!")%request.user.username
        t = get_template('bookapp/list_book.html')
        c = RequestContext(request,locals())
        return HttpResponse(t.render(c))

    def register(request):
        '''注册视图'''
        template_var={}
        form = RegisterForm()
        if request.method == "POST":
            form = RegisterForm(request.POST.copy())
            if form.is_valid():
                email = form.cleaned_data["email"]
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = User.objects.create_user(username,password,email)
                user.save()
                _login(request,username,password)  #注册完毕，直接登录
                return HttpResponseRedirect('/bookapp/book/list/')
        template_var["form"] = form
        t = get_template('registration/register.html')
        c = RequestContext(request,locals())
        return HttpResponse(t.render(c))

def login(request):
    '''登录视图'''
    template_var={}
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST.copy())
        if form.is_valid():
            if(True == _login(request,form.cleaned_data["username"],form.cleaned_data["password"])):
                return HttpResponseRedirect('/bookapp/book/list/')
    t = get_template('registration/login.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

def _login(request,username,password):
    '''登录核心方法'''
    ret = False
    user = authenticate(username=username,password=password)
    if user:
        if user.is_active:
            auth_login(request,user)
            messages.add_message(request,messages.INFO, _(u'Activation Success!'))
            ret = True
        else:
            messages.add_message(request,messages.INFO, _(u'Activation Failed!'))
    else:
        messages.add_message(request,messages.INFO,_(u'User not exist!'))
    return ret

def logout(request):
    '''注销视图'''
    auth_logout(request)
    return HttpResponseRedirect('/bookapp/book/list')

def account_edit(request):
    try:
        account_instance = UserProfile.objects.get(id=request.user.id)
    except UserProfile.DoesNotExist:
        account_instance = None
    form = AccountForm(request.POST or None,instance = account_instance)
    if form.is_valid():
        form.save()
        form = AccountForm()
    t = get_template('registration/account_edit.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))


