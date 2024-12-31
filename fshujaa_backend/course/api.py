from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from .forms import CourseForm
from .models import Course, Enrollment
from .serializers import CoursesListSerializer, CoursesDetailSerializer, EnrollmentsListSerializer
from useraccount.models import User

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def courses_list(request):
    #
    # Auth

    try:
        token = request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]
        token = AccessToken(token)
        user_id = token.payload['user_id']
        user = User.objects.get(pk=user_id)
    except Exception as e:
        user = None

    #
    #

    favorites = []
    courses = Course.objects.all()

    #
    # Filter

    is_favorites = request.GET.get('is_favorites', '')
    instructor_id = request.GET.get('instructor_id', '')

    category = request.GET.get('category', '')


    if  instructor_id:
        courses = courses.filter( instructor_id= instructor_id)

    if is_favorites:
        courses = courses.filter(favorited__in=[user])
    
    
    
    if category and category != 'undefined':
        courses = courses.filter(category=category)
    
    #
    # Favorites
        
    if user:
        for course in courses:
            if user in course.favorited.all():
                favorites.append(course.id)

    #
    #

    serializer = CoursesListSerializer(courses, many=True)

    return JsonResponse({
        'data': serializer.data,
        'favorites': favorites
    })


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def courses_detail(request, pk):
    course = Course.objects.get(pk=pk)

    serializer = CoursesDetailSerializer(course, many=False)

    return JsonResponse(serializer.data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def course_enrollment(request, pk):
    course = Course.objects.get(pk=pk)
    enrollment = course.enrollments.all()

    serializer = EnrollmentsListSerializer(enrollment, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST', 'FILES'])
def create_course(request):
    form = CourseForm(request.POST, request.FILES)

    if form.is_valid():
        course = form.save(commit=False)
        course.instructor = request.user
        course.save()

        return JsonResponse({'success': True})
    else:
        print('error', form.errors, form.non_field_errors)
        return JsonResponse({'errors': form.errors.as_json()}, status=400)


@api_view(['POST'])
def enroll_course(request, pk):
    try:
        course = Course.objects.get(pk=pk)

        Enrollment.objects.create(
            course=course,
            created_by=request.user
        )

        return JsonResponse({'success': True})
    except Exception as e:
        print('Error', e)

        return JsonResponse({'success': False})


@api_view(['POST'])
def toggle_favorite(request, pk):
    course = Course.objects.get(pk=pk)

    if request.user in course.favorited.all():
        course.favorited.remove(request.user)

        return JsonResponse({'is_favorite': False})
    else:
        course.favorited.add(request.user)

        return JsonResponse({'is_favorite': True})