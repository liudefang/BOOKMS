from django.contrib import admin

# Register your models here.
from bookapp.models import *

class BookAdmin(admin.ModelAdmin):
 pass

admin.site.register(Book)