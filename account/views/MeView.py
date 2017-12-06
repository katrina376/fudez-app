from rest_framework import generics, permissions, views, status
from rest_framework.response import Response

from account.models import User
from account.serializers import UserSerializer, SimpleUserSerializer, FullUserSerializer, PasswordSerializer


class MeView(views.APIView):
    def get(self, request, format=None):
        serializer = FullUserSerializer(self.request.user)
        return Response(status=status.HTTP_200_OK,
                        data=serializer.data)

    def patch(self, request, format=None):
        user = self.request.user
        data = self.request.data

        if 'new_password' in data:
            password_serializer = PasswordSerializer(data=data)
            if password_serializer.is_valid():
                if not user.check_password(password_serializer.data.get('old_password')):
                    return Response(data={'old_password': ['Wrong password.']},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.set_password(
                        password_serializer.data.get('new_password'))
                    user.save()
                    return Response(data={'Update password sucessfully.'},
                                    status=status.HTTP_200_OK)
            else:
                return Response(data={'Fail updating password.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserSerializer(user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK,
                                data=SimpleUserSerializer(user).data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data=serializer.errors)
