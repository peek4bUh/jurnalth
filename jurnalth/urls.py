"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import path

from apps.exercises.views import exercises_index
from apps.workouts.views import (
    workout_create,
    workout_delete,
    workout_edit,
    workouts_index,
    last_exercise_data,
)
from jurnalth.auth_views import (
    forgot_password_view,
    login_view,
    logout_view,
    signup_view,
)


@login_required(login_url='login')
def index(request):
    return render(request, 'index.html', {
        'header_actions': [
            {'route': 'logout', 'label': 'Logout'},
        ],
    })


urlpatterns = [
    path('', index, name='index'),

    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('forgot-password/', forgot_password_view, name='forgotPassword'),
    path('logout/', logout_view, name='logout'),

    path("admin/", admin.site.urls),
    path("exercises/", exercises_index, name="exercises_index"),
    path("workouts/", workouts_index, name="workouts_index"),
    path("workouts/new/", workout_create, name="workout_create"),
    path("workouts/<int:workout_id>/edit/", workout_edit, name="workout_edit"),
    path("workouts/<int:workout_id>/delete/",
         workout_delete, name="workout_delete"),
    path("workouts/exercises/<int:exercise_id>/last-data/",
         last_exercise_data, name="last_exercise_data"),
]
