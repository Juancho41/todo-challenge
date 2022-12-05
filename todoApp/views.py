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


""" se deja para poder tener acceso a todas la tareas sin tener
#          encuenta de q usuario son por las dudas """

# @api_view(['GET'])
# def listaTareas(request):
#     tareas = Tarea.objects.all()
#     serializer = TareaSerializer(tareas, many=True)
#     print(serializer)
#     return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listaTareas(request):
    tareas = Tarea.objects.filter(usuario=request.user)
    serializer = TareaSerializer(tareas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detallesTarea(request, pk):
    tarea = Tarea.objects.get(id=pk)
    if (tarea.usuario == request.user):
        serializer = TareaSerializer(tarea, many=False)
        return Response(serializer.data)
    else:
        return Response('Tarea no pertenece al usuario logueado')



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crearTarea(request):
    datos = request.data
    datos['usuario'] = request.user.id
    serializer = TareaSerializer(data=datos)
    print(request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        print(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def modificarTarea(request, pk):
    tarea = Tarea.objects.get(id=pk)
    if (tarea.usuario == request.user):
        serializer = TareaSerializer(instance=tarea, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    else:
        return Response('Tarea no pertenece al usuario logueado')

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def borrarTarea(request, pk):
    tarea = Tarea.objects.get(id=pk)
    if (tarea.usuario == request.user):
        tarea.delete()
        return Response('Tarea eliminada!')
    else:
        return Response('Tarea no pertenece al usuario logueado')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filtrarContenido (request, fil):
    tareas = Tarea.objects.filter(tarea__icontains=fil, usuario=request.user)
    serializer = TareaSerializer(tareas, many=True)
    return Response(serializer.data)

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