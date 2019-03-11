# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from jsonfield import JSONField
from django.contrib.auth.models import User 



# Create your models here.


class Producto (models.Model):
    
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique = True)
    descripcion = models.TextField()
    stock = models.IntegerField()
    precio = models.FloatField()
    atributos = JSONField()
    
    class Meta:
        ordering = ('nombre',)
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        
    def __str__(self):
        return self.nombre
    
    def get_admin_absolute_url(self):
        return reverse('adminproductosdetalle',kwargs={'slug':self.slug})
    
    def get_absolute_url(self):
        return reverse('productodetalle',kwargs={'slug':self.slug})
    
    

class Pedido (models.Model):
    
    RECIBIDO = 'Recibido'
    PROCESADO = 'Procesado'
    ENVIADO = 'Enviado'
    ENTREGADO = 'Entregado'
    CANCELADO = 'Cancelado'
    ESTADOS = ((RECIBIDO,'Recibido'),(PROCESADO,'Procesado'),(ENVIADO,'Enviado'),(ENTREGADO,'Entregado'),(CANCELADO,'Cancelado'))
    fecha = models.DateField(auto_now=True)
    detalle = JSONField()
    cliente = models.ForeignKey(User)
    estado = models.CharField(max_length=25,choices=ESTADOS,default=RECIBIDO)
    
    
    class Meta:
        ordering = ('fecha',)
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
    
    def __str__(self):
        return 'Pedido #'+str(self.id)+' del '+str(self.fecha)
    
    def get_admin_absolute_url(self):
        return reverse('adminpedidosdetalle',kwargs={'pk':self.id})
    def get_absolute_url(self):
        return reverse('pedidodetalle',kwargs={'pk':self.id})
    
    
