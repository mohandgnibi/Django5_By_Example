from rest_framework import generics
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.api.serializers import CourseSerializer, SubjectSerializer
from courses.models import Course, Subject
from courses.api.pagination import StandardPagination


# class SubjectListView(generics.ListAPIView):
#     queryset = Subject.objects.annotate(total_courses=Count('courses'))
#     serializer_class = SubjectSerializer
#     pagination_class = StandardPagination


# class SubjectDetailView(generics.RetrieveAPIView):
#     queryset = Subject.objects.annotate(total_courses=Count('courses'))
#     serializer_class = SubjectSerializer


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination


class CourseEnrollView(APIView):
    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({'enrolled': True})
    