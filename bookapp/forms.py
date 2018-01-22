# -*- encoding: utf-8 -*-
# @Time    : 2018-01-22 22:39
# @Author  : mike.liu
# @File    : forms.py
from django import forms
from tornado.platform.twisted import _

from bookapp.models import *


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = ['borrower','available','borrow_date','return_date'] # uncomment this line and specify any field to exclude it from the form

    def __init__(self,*args,**kwargs):
        super(BookForm,self).__init__(*args,**kwargs)

class AccountForm(forms.ModelForm):

    email = forms.EmailField(label=("邮件"),max_length=30,widget=forms.TextInput(attrs={'size':30,}))
    username = forms.CharField(label=('昵称'),max_length=30,widget=forms.TextInput(attrs={'size':20,}))
    password = forms.CharField(label=('密码'),max_length=30,widget=forms.TextInput(attrs={'20':20,}))

    def clean_username(self):
        '''验证重复昵称'''
        users = User.objects.filter(username__iexact=self.cleaned_data["username"])
        if not users:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("该昵称已经被使用"))

    def clean_email(self):
        '''验证重复Email'''
        emails = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if not emails:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_("该邮箱已经被使用"))
