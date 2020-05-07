# -*- coding: utf-8 -*-


from datetime import date, timedelta, datetime
from .models import *
from django.core.mail import EmailMultiAlternatives
from Universidad_back.settings import base
import schedule
import time



def enviarCorreoPatadas():
    hoy = datetime.now()
    menos28Sem =  hoy - timedelta(weeks=28)
    todosUsuariosAvisar = []

    #Coger todos los usuario que estén de más de 28 semanas
    todosUsuarioQuery = User.objects.filter(fechaUltMens__gte = menos28Sem)

    for user in todosUsuarioQuery:
        diferencia = date.today() - user.fechaUltMens
        if  diferencia <= timedelta(days=294):
            todosUsuariosAvisar.append(user)

    asunto_mail = "Aviso patadas"
    mensaje_mail = "Le recordamos que hace más de dos horas que no registra patadas en nuestro sistema"

    for user in todosUsuariosAvisar:
       # para_mail = user.email
        para_mail = "majive02696@gmail.com"
        mail = EmailMultiAlternatives(asunto_mail, mensaje_mail, base.EMAIL_HOST_USER, [para_mail])
        mail.send()

    # schedule.every(2).hours.do(enviarCorreoPatadas)
schedule.every(5).seconds.do(enviarCorreoPatadas)
while True:
    schedule.run_pending()
    time.sleep(1)