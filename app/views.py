from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from .forms import LessonForm, CategoryForm, CourseForm, TopicForm
from .models import Course, Topic, Lesson, Order


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        context = {
            "courses": courses
        }
        return render(request, 'app/index.html', context)

    def post(self, request, *args, **kwargs):
        pass


class NewCourseView(View):
    def get(self, request, *args, **kwargs):
        print(request.user)
        form = CourseForm()
        context = {
            "form": form
        }
        return render(request, "app/new_course.html", context)

    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('app:index')
        context = {
            "form": form
        }
        return render(request, "app/new_course.html", context)


class NewCategoryView(View):
    def get(self, request, *args, **kwargs):
        form = CategoryForm()
        context = {
            "form": form
        }
        return render(request, "app/new_category.html", context)

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app:index')
        context = {
            "form": form
        }
        return render(request, "app/new_category.html", context)


class NewTopicView(View):
    def get(self, request, id, *args, **kwargs):
        course = get_object_or_404(Course, pk=id)
        form = TopicForm()
        context = {
            "form": form,
            "course": course
        }
        return render(request, "app/new_topic.html", context)

    def post(self, request, id, *args, **kwargs):
        course = get_object_or_404(Course, pk=id)
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.course = course
            topic.save()
            return redirect('app:course_topics', course.id)
        context = {
            "form": form
        }
        return render(request, "app/new_topic.html", context)


class EditTopicView(View):
    def get(self, request, id, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=id)
        topic = get_object_or_404(Topic, pk=pk)
        if not topic in course.topics.all():
            return HttpResponse("You cant be here ")
        form = TopicForm(instance=topic)
        context = {
            "form": form
        }
        return render(request, "app/new_topic.html", context)

    def post(self, request, id, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=id)
        topic = get_object_or_404(Topic, pk=pk)
        form = TopicForm(request.POST, request.FILES, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('app:course_topics', course.id)
        context = {
            "form": form
        }
        return render(request, "app/new_topic.html", context)


class NewLessonView(View):
    def get(self, request, id, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=id)
        topic = get_object_or_404(Topic, pk=pk)
        form = LessonForm()
        context = {
            "form": form
        }
        return render(request, "app/new_lesson.html", context)

    def post(self, request, id, pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=id)
        topic = get_object_or_404(Topic, pk=pk)
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.topic = topic
            lesson.course = course
            lesson.save()
            return redirect('app:topic_lessons', course.id, topic.id)
        context = {
            "form": form
        }
        return render(request, "app/new_lesson.html", context)


class EditLessonView(View):
    def get(self, request, id, pk, lesson_id, *args, **kwargs):
        course = get_object_or_404(Course, pk=id)
        topic = get_object_or_404(Topic, pk=pk)
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        if not topic in course.topcs.all() and not lesson in topic.lessons.all():
            return HttpResponse("You can not be here")
        form = LessonForm(instance=lesson)
        context = {
            "form": form
        }
        return render(request, "app/new_lesson.html", context)

    def post(self, request, id, pk, lesson_id, *args, **kwargs):
        course = get_object_or_404(Course, pk=id)
        topic = get_object_or_404(Topic, pk=pk)
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('app:topic_lessons')
        context = {
            "form": form,
            "course": course,
            "lesson": lesson,
            "topic": topic
        }
        return render(request, "app/new_lesson.html", context)


class InstructorCourseListView(View):
    def get(self, request, *args, **kwargs):
        courses = Course.objects.filter(instructor=request.user)
        context = {
            'courses': courses,
        }
        return render(request, 'app/instructor_courses.html', context)


class CourseTopicListView(View):
    def get(self, request, id, *args, **kwargs):
        course = get_object_or_404(Course, pk=id)
        context = {
            'course': course,
        }
        return render(request, 'app/course_topics.html', context)


class TopicLessonListView(View):
    def get(self, request, id, pk,  *args, **kwargs):
        course = get_object_or_404(Course, pk=id)
        topic = get_object_or_404(Topic, pk=pk)
        if not topic in course.topics.all():
            return HttpResponse("No such topic for this course")
        context = {
            'course': course,
            'topic': topic
        }
        return render(request, 'app/topic_lessons.html', context)


class EditCourseView(View):
    def get(self, request, id, *args, **kwargs):
        course = get_object_or_404(Course, pk=id)
        form = CourseForm(instance=course)
        context = {
            "form": form
        }
        return render(request, "app/new_course.html", context)

    def post(self, request, id, *args, **kwargs):
        course = get_object_or_404(Course, pk=id)
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('app:instructor_courses')
        context = {
            "form": form
        }
        return render(request, "app/new_course.html", context)


class OrderDetailView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        user_orders = Order.objects.filter(student=user, is_paid=False)
        total = sum([
            order.course.price for order in user_orders
        ])
        context = {
            "user_orders": user_orders,
            "total": total
        }
        return render(request, "app/user_orders.html", context)


class CourseDetailView(View):
    def get(self, request, id, *args, **kwargs):
        course = get_object_or_404(Course, pk=id)
        context = {
            "course": course
        }
        return render(request, 'app/course_detail.html', context)
