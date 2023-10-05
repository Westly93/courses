from django.db import models
from accounts.models import UserAccount
from django_resized import ResizedImageField


""" class Course(models.Model):
    name= models.CharField(max_length= 1000)
    owner_id = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name='courses')
    date_created = models.DateTimeField(auto_now_add=True) """


class Course(models.Model):
    class StatusChoices(models.TextChoices):
        PUBLISH = 'Publish'
        DRAFT = 'Draft'
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    instructor = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="courses")
    title = models.CharField(max_length=1000)
    what_you_will_learn = models.TextField()
    featured_image = ResizedImageField(
        size=[200, 200], quality=100, upload_to="courses"
    )
    featured_video = models.FileField(upload_to="courses")
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def discount_amount(self):
        return (self.discount / 100) * float(self.price)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    student = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="orders")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_paid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order for {self.student.username}'


class Enrollment(models.Model):
    class StatusChoices(models.TextChoices):
        DROPPED = "Dropped"
        COMPLETED = "Completed"
        ENROLLED = "Enrolled"
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.ENROLLED)


class Topic(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=2000)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.title} topic for {self.course.title}'


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=2000)
    content = models.TextField(null=True, blank=True)
    attachment = models.FileField(upload_to=f"courses/", null=True, blank=True)

    def __str__(self):
        return f'{self.title} lesson for the topic {self.topic.title}'


""" class Quiz(models.Model):
    pass 
class Question(models.Model):
    pass
class Answer(models.Model):
    pass """
