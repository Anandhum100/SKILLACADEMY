from django.urls import path,include
from myapp import views,user_login


urlpatterns = [
 path('BASE',views.BASE,name='base'),
 path('404',views.PAGE_NOT_FOUND,name='404'),
 path('',views.HOME,name='home'),

 path('courses',views.SINGLE_COURSE,name='single_course'),
 path('course/<int:id>',views.COURSE_DETAILS,name='course_details'),
 path('course/filter-data/',views.filter_data,name="filter-data"),
 path('mycourse/',views.My_Course,name='my_course'),

 path('search',views.SEARCH_COURSE,name='search_course'),
 path('contact',views.CONTACT_US,name='contact_us'),
 path('contactdata/',views.contactdata,name="contactdata"),
 path('reviewdata/',views.reviewdata,name="reviewdata"),
 path('about',views.ABOUT_US,name='about_us'),

 path('login',views.LOGIN,name='login'),
 path('doLOgin',user_login.DO_LOGIN,name= 'doLogin'),

 path('checkout/<int:id>',views.CHECKOUT,name='checkout'),
 path('verify_payment',views.VERIFY_PAYMENT, name= 'verify_payment'),

]