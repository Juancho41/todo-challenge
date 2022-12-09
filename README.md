# ToDo-List - API backend en Django para crear lista de tareas

Una aplicación web sencilla para backend que permita a los usuarios crear y mantener una lista 
de tarea

## Aplicación

la API contiene los siguientes endpoints
```
api_urls=
        {
        'Lista': '/lista-tareas/',
        'Detalles': '/detalles-tarea/<str:pk>/',
        'Crear': '/crear-tarea/',
        'Modificar': '/modificar-tarea/<str:pk>/',
        'Completar-tarea': 'completar-tarea/<str:pk>/',
        'Borrar': '/borrar-tarea/<str:pk>/',
        'filtrar-contenido': '/filtrar-contenido/<str:fil>/',
        'filtrar-fecha': 'filtrar-fecha/<int:dia>/<int:mes>/<int:año>',
        'crear-usuario': 'crear-user/',
        'Obtener-token': '/token/',
        'Token-refresh': '/token/refresh/',
        }
```

