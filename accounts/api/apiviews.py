from django.shortcuts import render
from rest_framework import status, permissions
from accounts.models import NewUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import  NewUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import NewUserSerializer
# Create your views here.

# APIVIEW TO REGISTER USER
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            serializer = NewUserSerializer(data = request.data)
            if serializer.is_valid():
                newuser = serializer.save()
                if newuser:
                    return Response(serializer.data, status= status.HTTP_201_CREATED)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {'error':'Something went wrong when registering an account'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# APIVIEW TO REGISTER AGENT
class RegisterAgentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = NewUserSerializer(data = request.data)
            if serializer.is_valid():
                newuser = serializer.save()
                if newuser:
                    return Response(serializer.data, status= status.HTTP_201_CREATED)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {'error':'Something went wrong when registering an account'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# APIVIEW FOR LOGOUT
class LogoutView(APIView):
    def post(self, request):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blackmailing()
            return Response('Success', status= status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status= status.HTTP_400_BAD_REQUEST)

# APIVIEW FOR LOGIN
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created= Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username' : user.user_name
        })  

# API VIEW TO DISPLAY USER DETAILS
@api_view(['GET'])
def user_details(request, id):
    try:
        user = NewUser.objects.get(pk=id)
    except NewUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = NewUserSerializer(user)
    return Response(serializer.data)


# API VIEW TO EDIT PROFILE
@api_view(['PUT'])
def user_update(request, id):
    try:
        user = NewUser.objects.get(pk=id)
    except NewUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = NewUserSerializer(user, data= request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)



# API VIEW TO DELETE ACCOUNT
@api_view(['DELETE'])
def user_delete(request, id):
    try:
        user = NewUser.objects.get(pk=id)
        users = NewUser.objects.all()
        serializer = NewUserSerializer(users, many= True)
    except NewUser.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response(serializer.data, status= status.HTTP_204_NO_CONTENT)



# API VIEW TO DISPLAY ALL AGENTS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def agent_list(request):
    agents = NewUser.objects.all()
    # print(agents)
    serializer = NewUserSerializer(agents, many= True)
    return Response(serializer.data)