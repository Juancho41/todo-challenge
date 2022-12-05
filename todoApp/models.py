from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
