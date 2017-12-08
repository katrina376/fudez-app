from rest_framework import views, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from account.models import User
from account.serializers import SimpleUserSerializer, FullUserSerializer, PasswordSerializer, UserUpdateSerializer


class MeView(views.APIView):
    def get(self, request, format=None):
        serializer = FullUserSerializer(request.user)
        return Response(status=status.HTTP_200_OK,
                        data=serializer.data)

    def patch(self, request, format=None):
        user = request.user
        data = request.data

        serializer = UserUpdateSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK,
                            data=SimpleUserSerializer(user).data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)


class MeResetPasswordView(views.APIView):
    def patch(self, request, format=None):
        user = request.user
        password_serializer = PasswordSerializer(data=request.data)
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
