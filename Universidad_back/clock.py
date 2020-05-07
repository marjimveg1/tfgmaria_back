from datetime import datetime, timedelta, date
from django.core.mail import EmailMultiAlternatives
import psycopg2
import smtplib
from email.mime.text import MIMEText

def testing1():
    print ("testing1 - every 2 min...")


def consultabbdd():
    try:
        connection = psycopg2.connect(user="seqapevgjsmefx",
                                      password="0098e32dd78dbd3aaab191910e1aa655b0e6252f5fd1e2a9ad24aadcb5eead85",
                                      host="ec2-52-71-85-210.compute-1.amazonaws.com",
                                      port=5432,
                                      database="d2f5jggrnej8a8")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from User"

        cursor.execute(postgreSQL_select_Query)
        print("seleccionado los usuarios" )
        mobile_records = cursor.fetchall()

        print("Print each row and it's columns values")
        for row in mobile_records:
            print("Id = ", row)

        hoy = datetime.now()
        menos28Sem = hoy - timedelta(weeks=28)
        todosUsuariosAvisar = []


        print("pre email")
        asunto = "Aviso patadas"
        mensaje = MIMEText("Le recordamos que hace más de dos horas que no registra patadas en nuestro sistema")
        receptor = "majive02696@gmail.com"
        emisor = "cuarentasemanastfg@gmail.com"

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

        print("email enviado")


    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
         # closing database connection.
       if (connection):
           cursor.close()
           connection.close()
           print("PostgreSQL connection is closed")




if __name__ == '__main__':
    from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()
    sched.add_job(consultabbdd, 'cron', id='run_every_1_min_email', minute='*/2')
    sched.add_job(testing1, 'cron', id='run_every_1_min', minute='*/2')
sched.start()





