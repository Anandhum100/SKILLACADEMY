"""
Module: models.py

This module defines the database models for your Django application.
It includes models for categories, authors, courses, lessons, videos, users,
payments, and other related entities.

"""
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save


# Create your models here.
class Categories(models.Model):
    """
    Represents a category with an icon and a name.

    Fields:
    - `icon`: A character field for an icon (nullable).
    - `name`: A character field for the category name.

    Methods:
    - `__str__`: Returns the name of the category.
    - `get_all_category()`: Returns all categories ordered by ID.

    """
    icon = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def get_all_category(self):
        """
        Returns all categories ordered by ID.

        Returns:
            QuerySet: A queryset of Categories objects.
        """
        return Categories.objects.all().order_by('id')
    

class Author(models.Model):
    """
    Represents an author with a profile image, name, and a short bio.

    Fields:
    - `author_profile`: An image field for the author's profile image.
    - `name`: A character field for the author's name (nullable).
    - `about_author`: A text field for a short bio.

    Methods:
    - `__str__`: Returns the name of the author.

    """
    author_profile = models.ImageField(upload_to="Media/author")
    name = models.CharField(max_length=100, null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name
    

class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Represents a course with various details.

    Fields:
    - `STATUS`: Choices for the course status ('PUBLISH' or 'DRAFT').
    - `featured_image`: An image field for the course's featured image (nullable).
    - `featured_video`: A character field for a featured video (nullable).
    - `title`: A character field for the course title.
    - `created_at`: A date field for the course creation date.
    - `author`: A foreign key to the Author model (nullable).
    - `category`: A foreign key to the Categories model.
    - `level`: A foreign key to the Level model (nullable).
    - `description`: A text field for the course description.
    - `price`: An integer field for the course price (nullable, default: 0).
    - `discount`: An integer field for any discount (nullable).
    - `slug`: A slug field for a human-readable URL (nullable).
    - `status`: A choice field for the course status.

    Methods:
    - `__str__`: Returns the title of the course.
    - `get_absolute_url()`: Returns the absolute URL of the course details page.

    """
    STATUS = (
        ('PUBLISH','PUBLISH'), 
        ('DRAFT', 'DRAFT'),
    )

    featured_image = models.ImageField(upload_to="Media/featured_img",null=True) 
    featured_video = models.CharField(max_length=300,null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    level = models.ForeignKey(Level,on_delete=models.CASCADE,null=True)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS,max_length=100,null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_details", kwargs={'slug': self.slug})
    

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)


class Lesson(models.Model):
    """
    Represents a lesson associated with a course.

    Fields:
    - `course`: A foreign key to the Course model, indicating the parent course.
    - `name`: A character field for the lesson name.

    Methods:
    - `__str__`: Returns a formatted string with the lesson name and the associated course title.

    """
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " - " + self.course.title
    

class Video(models.Model):
    """
    Represents a video lesson associated with a course.

    Fields:
    - `serial_number`: An integer field for the video's serial number (nullable).
    - `thumbnail`: An image field for the video's thumbnail (nullable).
    - `course`: A foreign key to the Course model, indicating the parent course.
    - `lesson`: A foreign key to the Lesson model, indicating the parent lesson.
    - `title`: A character field for the video title.
    - `youtube_id`: A character field for the YouTube video ID.
    - `time_duration`: A floating-point field for the video's duration (nullable).
    - `preview`: A boolean field indicating whether the video is a preview (default: False).

    Methods:
    - `__str__`: Returns the video's title.

    """
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="Media/Yt_Thumbnail",null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=200)
    time_duration = models.FloatField(null=True)
    preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class UserCourse(models.Model):
    """
    Represents a user's enrollment in a course.

    Fields:
    - `user`: A foreign key to the User model, indicating the enrolled user.
    - `course`: A foreign key to the Course model, indicating the enrolled course.
    - `paid`: A boolean field indicating whether the user has paid for the course (default: False).
    - `date`: A date and time field representing the enrollment date (auto-generated).

    Methods:
    - `__str__`: Returns a formatted string with the user's first name and the enrolled course title.

    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + "-" + self.course.title


class Payment(models.Model):
    """
    Represents a payment transaction for a user's enrollment in a course.

    Fields:
    - `order_id`: A character field for the payment order ID (nullable).
    - `payment_id`: A character field for the payment ID (nullable).
    - `user_course`: A foreign key to the UserCourse model, indicating the enrolled user's course (nullable).
    - `user`: A foreign key to the User model, indicating the user associated with the payment (nullable).
    - `course`: A foreign key to the Course model, indicating the enrolled course (nullable).
    - `date`: A date and time field representing the payment transaction date (auto-generated).
    - `status`: A boolean field indicating the payment status (default: False).

    Methods:
    - `__str__`: Returns a formatted string with the user's first name and the enrolled course title.

    """
    order_id = models.CharField(max_length=100,null=True,blank=True)
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    user_course = models.ForeignKey(UserCourse,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + "-" + self.course.title


class contactdb (models.Model):
    """
    Represents a database entry for user contact information.

    Fields:
    - `NAME`: A character field for the user's name (nullable).
    - `EMAIL`: A character field for the user's email address (nullable).
    - `MESSAGE`: A character field for the user's message (nullable).

    Methods:
    - `__str__`: Returns the user's name.

    """
    NAME = models.CharField(max_length=50, null=True, blank=True)
    EMAIL = models.CharField(max_length=50, null=True, blank=True)
    MESSAGE = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.NAME
    

class reviewdb(models.Model):
    """
    Represents a user review for a course.

    Fields:
    - `selectcourse`: A character field for the course name (nullable).
    - `selectuser`: A character field for the user's name (nullable).
    - `Userphoto`: An image field for the user's photo (nullable).
    - `Review`: A text field for the user's review.

    Methods:
    - `__str__`: Returns the user's name.

    """
    selectcourse = models.CharField(max_length=50, null=True, blank=True)
    selectuser = models.CharField(max_length=50, null=True, blank=True)
    Userphoto = models.ImageField(upload_to="Media/user_img",null=True)
    Review = models.TextField()

    def __str__(self):
        return self.selectuser

    
        
