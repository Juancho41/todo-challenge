from django.test import TestCase
from django.test import Client
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User

# Create your tests here.
#correr todos los set de tests
# python manage.py test todoApp.tests.ApiTests_crearTarea todoApp.tests.UserTest todoApp.tests.ApiTests_conTarea todoApp.tests.ApiTests_conTarea_dosUsuarios


class UserTest (TestCase):
    #Test al crear un usuario se entrega un token de acceso
    def test_createUser(self):
        client = APIClient()
        response = client.post('http://127.0.0.1:8000/todoApp/crear-user/', {'username': 'testuser', 'password': '123456'}, format='json')
        self.assertFalse(response.data.get('prueba')) #prueba de respuesta inexistente
        self.assertTrue(response.data.get('access'))  #prueba de que la aplicacion devuelve un access token
        assert response.status_code == 200

    #Crea usuario y guarda tokens para utilizarlos
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        response = cls.client.post('http://127.0.0.1:8000/todoApp/crear-user/', {'username': 'testuser2', 'password': '123456'}, format='json')
        cls.accessToken = response.data.get('access')
        cls.refreshToken = response.data.get('refresh')
        cls.authHeader = 'Bearer ' + cls.accessToken

    #prueba de loggin de usuario creado
    def test_loginUser(self):
        response = self.client.post('http://127.0.0.1:8000/todoApp/token/', {'username': 'testuser2', 'password': '123456'}, format='json')
        self.assertFalse(response.data.get('prueba')) #prueba de respuesta inexistente
        self.assertTrue(response.data.get('access'))  #prueba de que la aplicacion devuelve un access token
        assert response.status_code == 200

    #prueba de refresh token para usuario creado que develve nuevo access token
    def test_loginUser_refreshToken(self):
        response = self.client.post('http://127.0.0.1:8000/todoApp/token/refresh/', {'refresh': self.refreshToken}, format='json')
        self.assertFalse(response.data.get('prueba')) #prueba de respuesta inexistente
        self.assertTrue(response.data.get('access'))  #prueba de que la aplicacion devuelve un access token
        assert response.status_code == 200

    #test para ver si NO se puede acceder a la lista vacia de tareas del usuario creado sin token
    def test_accessTareas_sinToken(self):
        response = self.client.get('http://127.0.0.1:8000/todoApp/lista-tareas/')
        assert response.status_code == 401


    #test para ver si se puede acceder a la lista vacia de tareas del usuario creado con su token de acceso
    def test_accessTareas(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accessToken)
        response = client.get('http://127.0.0.1:8000/todoApp/lista-tareas/')
        assert response.status_code == 200

class ApiTests_crearTarea(TestCase):
    #Crea usuario y guarda tokens para utilizarlos
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        response = cls.client.post('http://127.0.0.1:8000/todoApp/crear-user/', {'username': 'testuser3', 'password': '123456'}, format='json')
        cls.accessToken = response.data.get('access')
        cls.refreshToken = response.data.get('refresh')

    #Crear tarea nueva con usuario
    def test_crearTarea(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accessToken)
        response = client.post('http://127.0.0.1:8000/todoApp/crear-tarea/', {"tarea": "tarea prueba"}, format='json')
        self.assertEqual(response.status_code, 200)


class ApiTests_conTarea(TestCase):
    #Crea usuario y guarda tokens para utilizarlos
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        response = cls.client.post('http://127.0.0.1:8000/todoApp/crear-user/', {'username': 'testuser3', 'password': '123456'}, format='json')
        cls.accessToken = response.data.get('access')
        cls.refreshToken = response.data.get('refresh')
        cls.client.credentials(HTTP_AUTHORIZATION='Bearer ' + cls.accessToken)
        createResponse = cls.client.post('http://127.0.0.1:8000/todoApp/crear-tarea/', {"tarea": "tarea prueba"}, format='json')
        createResponse_fil = cls.client.post('http://127.0.0.1:8000/todoApp/crear-tarea/', {"tarea": "tarea prueba para filtrado"}, format='json')

    #Ver si el usuario tiene la tarea creada
    def test_verListaTareas(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accessToken)
        response = client.get('http://127.0.0.1:8000/todoApp/lista-tareas/')
        #print(response.json()[0]['tarea'])
        self.assertEqual(response.json()[0]['tarea'], 'tarea prueba')
        assert response.status_code == 200

    #Probar cambio de estado de tarea: tarea completada
    def test_completarTarea(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accessToken)
        response = client.post('http://127.0.0.1:8000/todoApp/completar-tarea/1/')

        #print(response.data['completada'])
        self.assertEqual(response.data['completada'], True)
        assert response.status_code == 200

        response2 = client.post('http://127.0.0.1:8000/todoApp/completar-tarea/1/')
        self.assertEqual(response2.data['completada'], False)
        assert response2.status_code == 200

    #Probar cambio de nombre de tarea
    def test_modificarTarea(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accessToken)
        response_detalles = client.get('http://127.0.0.1:8000/todoApp/detalles-tarea/1/')

        #print(response_detalles.data['tarea'])
        self.assertEqual(response_detalles.data['tarea'], 'tarea prueba')
        assert response_detalles.status_code == 200

        response_modificar = client.post('http://127.0.0.1:8000/todoApp/modificar-tarea/1/', {'tarea': 'tarea modificada'})
        #print(response_modificar.data['tarea'])
        self.assertEqual(response_modificar.data['tarea'], 'tarea modificada')
        assert response_modificar.status_code == 200

    #test borrado de tarea
    def test_borrarTarea(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accessToken)
        response_lista = client.get('http://127.0.0.1:8000/todoApp/lista-tareas/')

        self.assertEqual(len(response_lista.data), 2) #ver tamaño inicial de la lista
        self.assertEqual(response_lista.status_code, 200)

        response_borrar = client.delete('http://127.0.0.1:8000/todoApp/borrar-tarea/1/')
        self.assertEqual(response_borrar.status_code, 200)

        response_lista_nueva = client.get('http://127.0.0.1:8000/todoApp/lista-tareas/')
        self.assertEqual(len(response_lista_nueva.data), 1) #verificar que la se haya borrado de la lista
        assert response_lista_nueva.status_code == 200

    #test filtrar tarea por contenido
    def test_filtrarTarea_porNombre(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accessToken)
        response_lista = client.get('http://127.0.0.1:8000/todoApp/filtrar-contenido/filt/')

        self.assertEqual(len(response_lista.data), 1) #ver tamaño de lista para un filtrado q deberia traer una tarea
        self.assertEqual(response_lista.status_code, 200)

        response_lista2 = client.get('http://127.0.0.1:8000/todoApp/filtrar-contenido/prasdfueb/')

        self.assertEqual(len(response_lista2.data), 0) #ver tamaño de lista para un filtrado q deberia traer cero tareas
        self.assertEqual(response_lista2.status_code, 200)

    #test filtrar tarea por fecha
    def test_filtrarTarea_porFecha(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accessToken)
        response_lista = client.get('http://127.0.0.1:8000/todoApp/filtrar-fecha/9/12/2022')

        self.assertEqual(len(response_lista.data), 2) #ver tamaño de lista para un filtrado q deberia traer 2 tarea
        self.assertEqual(response_lista.status_code, 200)

        response_lista2 = client.get('http://127.0.0.1:8000/todoApp/filtrar-fecha/5/12/2022')

        self.assertEqual(len(response_lista2.data), 0) #ver tamaño de lista para un filtrado q deberia traer cero tareas
        self.assertEqual(response_lista2.status_code, 200)


class ApiTests_conTarea_dosUsuarios(TestCase):
    #Crea usuarios y guarda tokens para utilizarlos
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        response = cls.client.post('http://127.0.0.1:8000/todoApp/crear-user/', {'username': 'testuser3', 'password': '123456'}, format='json')
        cls.accessToken2 = response.data.get('access')
        cls.refreshToken2 = response.data.get('refresh')
        cls.client.credentials(HTTP_AUTHORIZATION='Bearer ' + cls.accessToken2)
        createResponse = cls.client.post('http://127.0.0.1:8000/todoApp/crear-tarea/', {"tarea": "tarea prueba"}, format='json')
        createResponse_fil = cls.client.post('http://127.0.0.1:8000/todoApp/crear-tarea/', {"tarea": "tarea prueba para filtrado"}, format='json')
        cls.client.credentials()
        response_otroUser = cls.client.post('http://127.0.0.1:8000/todoApp/crear-user/', {'username': 'testuserOtro', 'password': '123456'}, format='json')
        cls.accessToken = response_otroUser.data.get('access')
        cls.client.credentials(HTTP_AUTHORIZATION='Bearer ' + cls.accessToken)
        createResponseOtro = cls.client.post('http://127.0.0.1:8000/todoApp/crear-tarea/', {"tarea": "tarea usuario testuserOtro"}, format='json')

    #Ver si el usuario testuserOtro obtine solamente su tarea creada
    def test_verListaTareas(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accessToken) #Token de testuserOtro
        response = client.get('http://127.0.0.1:8000/todoApp/lista-tareas/')
        #print(response.data)
        self.assertEqual(len(response.data), 1) #ver si solo tiene su tarea creada
        assert response.status_code == 200

    #Probar cambio de estado de tarea para tarea de otro usuario
    def test_completarTarea(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accessToken)
        response = client.post('http://127.0.0.1:8000/todoApp/completar-tarea/1/')

        #print(response.data['completada'])
        assert response.status_code == 401


    #Probar cambio de nombre de tarea para tarea de otro usuario
    def test_modificarTarea(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accessToken)
        response_detalles = client.post('http://127.0.0.1:8000/todoApp/modificar-tarea/1/')

        self.assertEqual(response_detalles.status_code, 401)


    #test borrado de tarea de otro usuario
    def test_borrarTarea(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.accessToken)

        response_borrar = client.delete('http://127.0.0.1:8000/todoApp/borrar-tarea/1/')
        self.assertEqual(response_borrar.status_code, 401)
