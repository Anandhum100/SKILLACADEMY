from django.contrib import admin
from .models import *
# Register your models here.

class Video_TabularInline(admin.TabularInline):
    model = Video


class course_admin(admin.ModelAdmin):
    inlines = [Video_TabularInline]


admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course,course_admin)
admin.site.register(Level)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(UserCourse)
admin.site.register(Payment)
admin.site.register(contactdb)
admin.site.register(reviewdb)



