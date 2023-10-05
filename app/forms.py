from django import forms
from .models import Category, Course, Topic, Lesson


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("category", "title", "featured_image", "featured_video",
                  "what_you_will_learn", "price", "discount", "status")


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ("title", "summary")


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ("title", "content", "attachment")
