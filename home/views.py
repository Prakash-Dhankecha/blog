from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.

class PublicBlog(APIView):
    def get(self, request):
        try:
            blogs = Blog.objects.all()

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))

            page_number = request.GET.get('page', 1)
            paginator = Paginator(blogs, 1)
            try:
                blogs_page = paginator.page(page_number)
            except PageNotAnInteger:
                return Response({
                    'data': {},
                    'message': 'Invalid page number. Must be an integer.'
                }, status=status.HTTP_400_BAD_REQUEST)
            except EmptyPage:
                return Response({
                    'data': {},
                    'message': 'No blogs available for the requested page.'
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = BlogSerializer(blogs_page, many=True)

            return Response({
                'data': serializer.data,
                'message': 'Blogs successfully retrieved'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)




class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user=request.user)

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))

            serializer = BlogSerializer(blogs, many=True)

            return Response({
                'data': serializer.data,
                'message': 'Blogs successfully retrieved'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Invalid, Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': 'Blog successfully created'
            }, status=status.HTTP_201_CREATED)


        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():
                return Response({
                    'data': {},
                    'message': 'Blog does not exist'
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    'data': {},
                    'message': 'You are not authorized to update this'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = BlogSerializer(blog[0], data=data, partial=True)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Invalid, Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': 'Blog successfully updated'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():
                return Response({
                    'data': {},
                    'message': 'Blog does not exist'
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    'data': {},
                    'message': 'You are not authorized to update this'
                }, status=status.HTTP_400_BAD_REQUEST)


            blog[0].delete()

            return Response({
                'data': {},
                'message': 'Blog successfully deleted'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            pass