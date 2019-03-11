# -*- coding: utf-8 -*-

from berninishoes.settings import EMAIL_PEDIDOS, EMAIL_HOST_USER
from django.core.mail import EmailMessage

def enviaMail(adjunto,pedido,usuario):
    fecha = pedido.fecha
    nomuser = usuario.first_name
    mailuser = usuario.email
    cuerpo = 'Estimado {0},\n su pedido del {1} ha sido recibido. Estamos tramitandolo. En breves recibira actualizaciones sobre el estado de su pedido'.format(nomuser,fecha)
    email = EmailMessage('Su pedido en Bernini Shoes',cuerpo,EMAIL_HOST_USER,[mailuser])
    fichero = open(adjunto,'rb')
    email.attach(adjunto,fichero.read(),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    try:
        email.send()
    except Exception as e:
        print str(e)
        
    adminmail = EmailMessage('Nuevo Pedido','Se ha realizado un nuevo pedido en la tienda',EMAIL_HOST_USER,[EMAIL_PEDIDOS])
    adminmail.attach(adjunto,fichero.read(),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    try:
        adminmail.send()
    except Exception as e:
        print str(e)
    