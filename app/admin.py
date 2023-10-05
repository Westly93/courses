from django.contrib import admin
from .models import Category, Course, Order, Topic, Lesson
# Register your models here.

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Order)
admin.site.register(Topic)
admin.site.register(Lesson)
