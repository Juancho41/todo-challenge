# ToDo-List - API backend en Django para crear lista de tareas

Una aplicación web sencilla para backend que permita a los usuarios crear y mantener una lista de tarea.
La API está diseñada para que el usuario tenga que estar autenticado al momento de usarla ya que cada usuario solo puede interactuar con su propia lista de tareas.
Toda la api está escrita en python utilizando DJANGO y Django Rest Framework.

## API

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

- Lista: devuelve la lista completa de las tareas de un usuario 
- Detalles: devuelve los detalles de una tarea especifica, se debe especificar como pk al id de la tarea solicitada
- Crear: endpoint para creación de tareas, se debe especificar el contenido de la tarea 
```
{
    "tarea": "tarea de prueba"
}
```
- Modificar: endpoint para modificar el contenido de la tarea. Se debe especificar el parámetro pk del id de la tarea y el contenido de la misma (como al crearla)
- Completar-tarea: endpoint para cambiar el estado de la tarea (si fue completada o no) solo especificando el parámetro pk como id
- Borrar: endpoint para borrar tarea especificando el id
- Filtrar-contenido: endpoint para filtrar tareas propias del usuario por contenido según un parametro especificado en la url (str:fil)
- Filtrar-fecha: endpoint para filtrar tareas propias del usuario por contenido según una fecha específica. Utiliza un parámetro para especificar el día, mes y año.
- Crear-usuario: endpoint para la creación de usuarios nuevos. Utiliza solo información de username y password. Devuleve token de access y refresh.
```
{
    "username": "Prueba",
    "password": "password123"
}
```
- Obtener-token: endpoint para loguear usuarios. Se debe proveer la misma información que la creación de usuarios pero valida para usuarios existentes. Devuelve tokens de access y refresh.
- Token-refresh: para obtener un nuevo access token dando como input el refresh token.
```
{
    "refresh": "aqui se debe colocar el refresh token que tiene una vida mucho mayor al access token"
}
```

## Modelo de las tareas

en la creación de nuevas tareas solo se debe especificar el título de la tarea, ya que el usuario, y la fecha de creación se obtienen automáticamente. El status de la tarea (si esta completada o no) por default sera falso (no completada)

```
class Tarea(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tarea = models.CharField(max_length=200)
    creada = models.DateTimeField(auto_now_add=True)
    completada = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name = ("Tarea")
        verbose_name_plural = ("Tareas")

    def __str__(self):
        return self.tarea

```

## Autenticación

Para validar la autenticación se eligió utilizar JSON Web Token Authentication con su paquete para django "django-rest-framework-simplejwt" (en referencias).
JSON Web Token es un estándar bastante nuevo que se puede usar para la autenticación basada en tokens. A diferencia del esquema TokenAuthentication incorporado, la autenticación JWT no necesita usar una base de datos para validar un token lo que hace que sea mas veloz. Djangorestframework-simplejwt proporciona algunas funciones para su simple implementación, así como una aplicación de blacklist de tokens para evitar que re utilicen tockes vencidos.

## Referencias

[Dajngo rest frameworkd](https://www.django-rest-framework.org/)

[JSON Web Token Authentication](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

[django-cors-headers](https://pypi.org/project/django-cors-headers/)


