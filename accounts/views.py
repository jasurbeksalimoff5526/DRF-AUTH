from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from .serializer import SignupSerializer


class SignupView(GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "user": serializer.data,
            "token": token.key
        })