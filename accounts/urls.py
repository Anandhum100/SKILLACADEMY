from django.urls import path,include
from . views import registerView,loginView,logout_view,updateProfile,updatedProfile
from django.contrib.auth import views as auth_views


urlpatterns = [
 path('login/',loginView,name='login'),
 path('register/',registerView,name='register'),
 path('logout/',auth_views.LogoutView.as_view(),name='logout'),

 path('accounts/profile',updateProfile,name='profile'),
 path('accounts/profile/update',updatedProfile,name='profileupdated')
]