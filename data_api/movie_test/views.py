# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer
from django.contrib.auth.models import User


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        # Extract specific fields from the request data
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # Create a dictionary with the extracted fields
        data_to_send = {
            'username': username,
            'password': password,
            'email': email,
        }

        # Create an instance of the serializer with the extracted data
        serializer = self.get_serializer(data=data_to_send)
        serializer.is_valid(raise_exception=True)

        # Call the create method of the serializer to create the user
        self.perform_create(serializer)

        # Optionally customize the response data or status code
        response_data = {'message': 'User created successfully'}

        # Return the response
        return Response(response_data, status.HTTP_201_CREATED)
