from django.db import models

# Create your models here.

class Tarea(models.Model):

    tarea = models.CharField(max_length=200)
    creada = models.DateTimeField(auto_now_add=True)
    completada = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name = ("Tarea")
        verbose_name_plural = ("Tareas")

    def __str__(self):
        return self.tarea
