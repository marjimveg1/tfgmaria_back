from datetime import datetime, timedelta, date
from django.core.mail import EmailMultiAlternatives
import psycopg2
import smtplib
from email.mime.text import MIMEText

def testing1():
    print ("testing1 - every 2 min...")


def consultabbdd():
    try:

        usuariosDestinos = []
        hoy = datetime.now()
        finEmb = hoy - timedelta(weeks=42)

        conexion = psycopg2.connect(user="seqapevgjsmefx",
                                      password="0098e32dd78dbd3aaab191910e1aa655b0e6252f5fd1e2a9ad24aadcb5eead85",
                                      host="ec2-52-71-85-210.compute-1.amazonaws.com",
                                      port=5432,
                                      database="d2f5jggrnej8a8")
        cursor = conexion.cursor()
        query_todosUsuarios = ' select * from "Gestion_user" where "fechaUltMens" >= %s AND CURRENT_DATE >= "fechaUltMens" AND "quiereNot"=True'

        cursor.execute(query_todosUsuarios, (str(finEmb),))
        resultado_query_todoUsuarios = cursor.fetchall()

        for usuario in resultado_query_todoUsuarios:
            id_usuario = usuario[0]

            cursor.execute('select id from "Gestion_diario" where user_id=%s;', (str(id_usuario),))
            resultado_query_diario = cursor.fetchall()

            diario_id = resultado_query_diario[0][0]
            cursor.execute('select count(*) from "Gestion_patada" where diario_id=%s;', (str(diario_id),))
            resultado_query_patada = cursor.fetchall()

            if (resultado_query_patada[0][0] != 0):
                usuariosDestinos.append(usuario[6])

        hoy = datetime.now()
        menos28Sem = hoy - timedelta(weeks=28)

        usuariosDestinos.append("majive02696@gmail.com")
        usuariosDestinos.append("majive026962@gmail.com")
        usuariosDestinos.append("majive026963@gmail.com")

        asunto = "Aviso patadas"
        mensaje = MIMEText("Le recordamos que hace más de dos horas que no registra patadas en nuestro sistema.")
        emisor = "cuarentasemanastfg@gmail.com"

        for email in usuariosDestinos:
            receptor = email
            mensaje['From'] = emisor
            mensaje['To'] = receptor
            mensaje['Subject'] = asunto
            serverSMTP = smtplib.SMTP('smtp.gmail.com', 587)
            serverSMTP.ehlo()
            serverSMTP.starttls()
            serverSMTP.ehlo()
            serverSMTP.login(mensaje['From'], "Contratfg_")
            serverSMTP.sendmail(emisor, receptor, mensaje.as_string())

            serverSMTP.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
         # closing database connection.
       if (conexion):
           cursor.close()
           conexion.close()
           print("PostgreSQL connection is closed")




if __name__ == '__main__':
    from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()
  #  sched.add_job(consultabbdd, 'cron', id='run_every_1_min_email', hour='*/2')
 #   sched.add_job(testing1, 'cron', id='run_every_1_min', minute='*/2')
sched.start()





