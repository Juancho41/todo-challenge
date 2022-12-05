from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import TareaSerializer
from .models import Tarea
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.


@api_view(['GET'])
def apiOverview(request):
    api_urls={
        'Lista': '/lista-tareas/',
        'Detalles': '/detalles-tarea/<str:pk>/',
        'Crear': '/crear-tarea/',
        'Modificar': '/modificar-tarea/<str:pk>/',
        'Borrar': '/borrar-tarea/<str:pk>/',

        'Obtener-token': '/token/',
        'Token-refresh': '/token/refresh/',
        }
    return Response (api_urls)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listaTareas(request):
    tareas = Tarea.objects.filter(usuario=request.user)
    serializer = TareaSerializer(tareas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def detallesTarea(request, pk):
    tareas = Tarea.objects.get(id=pk)
    serializer = TareaSerializer(tareas, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def crearTarea(request):
    serializer = TareaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def modificarTarea(request, pk):
    tarea = Tarea.objects.get(id=pk)
    serializer = TareaSerializer(instance=tarea, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def borrarTarea(request, pk):
    tarea = Tarea.objects.get(id=pk)
    tarea.delete()
    return Response('Tarea eliminada!')


#token views modificadas

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer