# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from shop.models import Producto, Pedido
from django.template import defaultfilters
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User 
from shop.forms import UserForm, PedidoAdminForm, SignUpForm
import json
from django.core.urlresolvers import reverse
from shop.excel import creaExcelPedido
from shop.mail import enviaMail


# Create your views here.

def index(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect('/shop/')
    return render(request,'index.html')


def dologin(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        passwd = request.POST['password']
        usuario = authenticate(username=username,password=passwd)
        if usuario:
            if usuario.is_active:
                login(request,usuario)
                if usuario.is_staff:
                    return HttpResponseRedirect('/shop/admin/')
                return HttpResponseRedirect('/shop/')
            else:
                return render(request,'index.html',{'mensaje':'ERROR: Usuario bloqueado'})
        else:
            return render(request,'index.html',{'mensaje':'ERROR: Usuario no existe'})

def dologout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')        
    
def dosignup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            passwd=form.cleaned_data.get('password1')
            user = authenticate(username=username,password=passwd)
            login(request,user)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request,'registro.html',{'form':form})

#@login_required
def tienda(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    
    productos = Producto.objects.all()
    return render(request,'tienda.html',{'productos':productos})

def detalleProducto(request,slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    
    prod = get_object_or_404(Producto,slug=slug)
    return render(request,'detalleproducto.html',{'producto':prod})

def pedidosUsuario(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    
    user=request.user
    pedidos = Pedido.objects.filter(cliente=user)
    return render(request,'pedidosuser.html',{'pedidos':pedidos})

def detallePedido(request,pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    
    pedidos = get_object_or_404(Pedido,id=pk)
    return render(request,'detallepedido.html',{'pedido':pedidos})

def perfilUsuario(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method=="POST":
        form = UserForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return render(request,'perfiluser.html',{'form':form})
    else:
        form = UserForm(instance=request.user)
        return render(request,'perfiluser.html',{'form':form})

def carrito(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    
    
    if request.method == "POST":
        if not request.COOKIES.get('carrito'):
            #primer producto anyadido
            data = {}
            data['nombre']=request.POST['nombre']
            data['id']=request.POST['id']
            data['cantidad']=request.POST['cantidad']
            data['rs']=request.POST['rs']
            data['precio']=request.POST['precio']
            if request.POST['detalle'] != '':
                d=json.loads(request.POST['detalle'])
            data['detalle']=d
            ldata=[]
            ldata.append(data)
            valcookie=json.dumps(ldata)
            response = HttpResponse("Producto anñadido al carrito")
            response.set_cookie('carrito',valcookie)
            return response
            
        else:
            #Ya hay productos en el carrito
            data = {}
            data['nombre']=request.POST['nombre']
            data['id']=request.POST['id']
            data['cantidad']=request.POST['cantidad']
            data['rs']=request.POST['rs']
            data['precio']=request.POST['precio']
            if request.POST['detalle'] != '':
                d=json.loads(request.POST['detalle'])
            data['detalle']=d
            oldprods = request.COOKIES.get('carrito')
            ldata = []
            ldata.append(data)
            if oldprods != "":
                oldprods=json.loads(oldprods)
                for prod in oldprods:
                    ldata.append(prod)
                valcookie=json.dumps(ldata)
                response = HttpResponse("Producto añadido al carrito")
                response.set_cookie('carrito',valcookie)
                return response
    else:
        return render(request,'cesta.html')
    
def updateCarrito(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    
    if request.method == "POST":
        prod = request.POST['producto']
        cesta = request.COOKIES.get('carrito')
        ldata = []
        if cesta !='':
            cesta = json.loads(cesta)
            for p in cesta:
                if p['rs']!=prod:
                    ldata.append(p)
            
            if len(cesta) >0:
                valcookie = json.dumps(ldata)
            else:
                valcookie = ''
            response = HttpResponse("Carrito actualizado")
            response.set_cookie('carrito',valcookie)
            return response

def checkoutCarrito(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    import datetime
    if request.method=="POST":
        user = request.user
        pedido = Pedido()
        pedido.cliente=user
        pedido.detalle=request.POST["detalle"]
        pedido.estado="Recibido"
        pedido.fecha=datetime.datetime.now()
        
        
        
        try:
            pedido.save()
            ficheroexcel=creaExcelPedido(pedido)
            enviaMail(ficheroexcel,pedido,request.user)
            response = HttpResponse("Pedido realizado correctamente")
            response.delete_cookie('carrito')
            return response
        except Exception as e:
            print str(e)
            return HttpResponse("ERROR")
    
def adminSite(request):
    if not request.user.is_authenticated and request.user.is_staff:
        return HttpResponseRedirect('/')
    
    productos = Producto.objects.all()
    pedidos = Pedido.objects.all()
    clientes = User.objects.filter(is_staff=False)
    
    return render(request,'admin.html',{'productos':productos,'pedidos':pedidos,'clientes':clientes})


def adminSiteProductoDetalle(request,slug):
    if not request.user.is_authenticated and request.user.is_staff:
        return HttpResponseRedirect('/')
    
    if request.method == "GET":
        producto = get_object_or_404(Producto,slug=slug)
        return render(request,'admindetalleproducto.html',{'producto':producto})
    
    if request.method == "POST":
        producto = Producto.objects.get(slug=slug)
        if producto:
            data = request.POST
            producto.nombre = data['nombre']
            producto.descripcion = data['descripcion']
            producto.stock = data['stock']
            producto.precio = data['precio']
            producto.atributos = data['atributos']
            producto.save()
            return HttpResponse("PRODUCTO MODIFICADO OK")
        else:
            return HttpResponse("ERROR PRODUCTO NOT FOUND")
            
    if request.method == "DELETE":
        producto = Producto.objects.get(slug=slug)
        if producto:
            producto.delete()
            return HttpResponse("PRODUCTO BORRADO")
        else:
            return HttpResponse("ERROR BORRANDO PRODUCTO")
        
def adminSiteProductoNuevo(request):
    if not request.user.is_authenticated and request.user.is_staff:
        return HttpResponseRedirect('/')
    
    if request.method == "POST":
        newprod = Producto()        
        data = request.POST
        newprod.nombre = data["nombre"]
        newprod.descripcion = data["descripcion"]
        newprod.stock = data["stock"]
        newprod.precio = data["precio"]
        newprod.atributos = data["atributos"]
        newprod.slug = defaultfilters.slugify(data["nombre"])
        try:
            newprod.save()
            return HttpResponse("PRODUCTO ANYADIDO")
        except Exception as e:
            print str(e)
            return HttpResponse("ERROR")
        
    
    return render(request,'adminnuevoproducto.html')


def adminSitePedidosDetalle(request,pk):
    if not request.user.is_authenticated and request.user.is_staff:
        return HttpResponseRedirect('/')
    if request.method == "GET":
        pedido = get_object_or_404(Pedido,id=pk)
        form = PedidoAdminForm()
        return render(request,'admindetallepedido.html',{'pedido':pedido,'form':form})
    if request.method == 'POST':
        form = PedidoAdminForm(request.POST)
        if form.is_valid():
            oldpedido = get_object_or_404(Pedido,id=pk)
            estado = form.cleaned_data.get('estado')
            oldpedido.estado = estado
            oldpedido.save() 
            return HttpResponseRedirect(reverse('adminhome'))
    if request.method == 'DELETE':
        pedido = get_object_or_404(Pedido,id=pk)
        if pedido:
            pedido.delete()
            return HttpResponse("Pedido Borrado")
        else:
            return HttpResponse("Error Pedido no borrado")

def adminSiteClientes(request):
    if not request.user.is_authenticated and request.user.is_staff:
        return HttpResponseRedirect('/')
    
    if request.method == "DELETE":
        data = request.body
        user = User.objects.filter(id=data)
        user.delete()
        return HttpResponse("Usuario Borrado")
    return render(request,'admin.html')