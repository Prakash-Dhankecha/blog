from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.serializers import RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Invalid, Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': {},
                'message': 'Account created successfully'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        try:

            data = request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Invalid, Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            response = serializer.get_jwt_token(serializer.data)

            return Response(data=response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)