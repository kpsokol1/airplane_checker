import mysql.connector
import smtplib
from mysql.connector import Error
import time
import credentials

while(True):
    error_state = False
    try:
        connection = mysql.connector.connect(host=credentials.db_host,
                                             database='dump1090_database',
                                             user=credentials.db_user,
                                             password = credentials.db_password)

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor(buffered=True)
            cursor.execute("Select Count(*) from Clean1 WHERE TIMESTAMPDIFF(SECOND, STR_TO_DATE(TIME, '%Y/%m/%d %H:%i:%s'),Now()) < 600 AND Station = 'Louisville,KY';")
            record = cursor.fetchone()
            count = record[0]
            if(count == 0 and error_state == False):
                error_state = True
                try:
                    smtp = smtplib.SMTP('smtp.gmail.com',587)
                    smtp.starttls()
                    smtp.login(credentials.email_user,credentials.email_password)
                    fromaddr = credentials.email_user
                    toaddr = credentials.recipient
                    message_subject = "Radar24 Error"
                    message_text = "Not updating database"
                    message = "From: %s\r\n" % fromaddr + "To: %s\r\n" % toaddr + "Subject: %s\r\n" % message_subject + "\r\n" + message_text
                    smtp.sendmail(credentials.email_user, credentials.recipient,message)
                    # Terminating the session
                    smtp.quit()
                    print("Email sent successfully!")
                except Exception as ex:
                        print(ex)
            else:
                error_state = False #issue resolved


    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    time.sleep(600) #test every 10 minutes