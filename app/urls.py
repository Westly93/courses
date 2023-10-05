from django.urls import path
from .views import (
    NewCategoryView, NewCourseView, NewLessonView,
    NewTopicView, CourseListView, InstructorCourseListView,
    EditCourseView, CourseTopicListView, TopicLessonListView,
    EditLessonView, EditTopicView, CourseDetailView, OrderDetailView
)


app_name = "app"
urlpatterns = [
    path('', CourseListView.as_view(), name="index"),
    path('orders/', OrderDetailView.as_view(), name="user_orders"),
    path('courses/', InstructorCourseListView.as_view(), name="instructor_courses"),
    path('courses/<int:id>/', CourseDetailView.as_view(), name="course_detail"),
    path('courses/<int:id>/topics/',
         CourseTopicListView.as_view(), name="course_topics"),
    path('courses/<int:id>/topics/<int:pk>/edit',
         EditTopicView.as_view(), name="edit_topic"),
    path('courses/<int:id>/topics/<int:pk>/lessons/',
         TopicLessonListView.as_view(), name="topic_lessons"),
    path('courses/<int:id>/topics/<int:pk>/lessons/<int:lesson_id>/edit',
         EditLessonView.as_view(), name="edit_lessons"),
    path('courses/<int:id>/edit/', EditCourseView.as_view(), name="edit_course"),
    path('courses/new_course/', NewCourseView.as_view(), name="new_course"),
    path('categories/new_category/',
         NewCategoryView.as_view(), name="new_category"),
    path('courses/<int:id>/topics/new_topic/',
         NewTopicView.as_view(), name="new_topic"),
    path('courses/<int:id>/topics/<int:pk>/new_lesson/',
         NewLessonView.as_view(), name="new_lesson"),
]
