from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import UserSerializer

class CurrentUser(APIView):
    def get(self, request):
        user_serializer = UserSerializer(instance=request.user)
    
        return Response({
            'user': user_serializer.data,
        })
        
