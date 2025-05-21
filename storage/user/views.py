from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from user.serializers import UserSerializer,AuthTokenSerializer
from django.shortcuts import render


def login_page(request):
    return render(request, 'user/login.html')

def register_page(request):
    return render(request, 'user/register.html')

class CreateUSerView(generics.CreateAPIView):
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user