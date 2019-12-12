from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, throttle_classes

from .models import Application
from .serializers import ApplicationSerializer

#-----------------------------------------
# Restful API : GET list route
#-----------------------------------------

@api_view(['GET'])
@csrf_exempt
def api_list(request):
    """ List all applications """
    apps = Application.objects.all()
    serializer = ApplicationSerializer(apps, many=True)
    return JsonResponse(serializer.data)


#-----------------------------------------
# Restful API : POST add route
#-----------------------------------------

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import ApplicationSerializerUpload


class APIApplicationAdd(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_serializer = ApplicationSerializerUpload(data=request.data)

        if file_serializer.is_valid():
            app = file_serializer.save()
            serializer = ApplicationSerializer(app)  # other serializer to get same data as in the list
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)