from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


@api_view(['GET'])
def apiOverview(request):
    api_urls={
        'Lista': '/lista-tareas/',
        'Detalles': '/detalles-tarea/<str:pk>/',
        'Crear': '/crear-tarea/',
        'Modificar': '/modificar-tarea/<str:pk>/',
        'Borrar': '/borrar-tarea/<str:pk>/',
        }
    return Response (api_urls)
