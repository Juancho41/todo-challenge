from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('lista-tareas/', views.listaTareas, name='lista-tareas'),
    path('detalles-tarea/<str:pk>/', views.detallesTarea, name='detalles-tarea'),
    path('crear-tarea/', views.crearTarea, name='crear-tarea'),
    path('modificar-tarea/<str:pk>/', views.modificarTarea, name='modificar-tarea'),
    path('borrar-tarea/<str:pk>/', views.borrarTarea, name='borrar-tarea'),
    path('filtrar-contenido/<str:fil>/', views.filtrarContenido, name='filtrar-contenido'),
    path('filtrar-fecha/<int:dia>/<int:mes>/<int:año>', views.filtrarFecha, name='filtrar-fecha'),

    path('token/', views.MyTokenObtainPairView.as_view(), name='obtener-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]