from django.urls import path

from . import api


urlpatterns = [
    path('', api.courses_list, name='api_courses_list'),
    path('create/', api.create_course, name='api_create_course'),
    path('<uuid:pk>/', api.courses_detail, name='api_courses_detail'),
    path('<uuid:pk>/enroll/', api.enroll_course, name='api_enroll_course'),
    path('<uuid:pk>/enrollments/', api.course_enrollment, name='api_course_enrollment'),
    path('<uuid:pk>/toggle_favorite/', api.toggle_favorite, name='api_toggle_favorite'),
]