from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    # Restricting nonlogged in users from accessing the list and retrieve endpoints
    # def get_permissions(self):
        # if self.action in ['register', 'login']:
            # permission_classes = [AllowAny]
        # else:
            # permission_classes = [IsAuthenticated]
        # This line:
        # return [permission() for permission in permission_classes]

        # Is equivalent to this traditional for loop:
        # result = []
        # for permission in permission_classes:
            # result.append(permission())
        # return result

    # Restricting nonlogged in users from accessing the list of users
    # def list(self, request, *args, **kwargs):
        # return Response(status=status.HTTP_403_FORBIDDEN)

    # Restricting nonlogged in users from retrieving the user details endpoint
    # def retrieve(self, request, *args, **kwargs):
        # Add custom permission logic
        # if request.user.is_authenticated and request.user.id == int(kwargs['pk']):
            # return super().retrieve(request, *args, **kwargs)
        # return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            serializer = self.get_serializer(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'},
                      status=status.HTTP_401_UNAUTHORIZED)