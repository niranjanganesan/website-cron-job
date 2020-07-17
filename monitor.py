import os
import smtplib
import requests
import logging
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

EMAIL_ADDRESS = 'madninja.business@gmail.com'
EMAIL_PASSWORD = os.environ.get('password')

@sched.scheduled_job('interval', minutes=25)

def timed_job():
    try:
        r = requests.get('http://www.niranjanganesan.com', timeout=10)
        status_code = r.status_code
        current_time = datetime.datetime.now()

        if status_code != 200:
            logging.info(f'Website is DOWN at {current_time}')
            print(f'Website is DOWN, time: {current_time}')
            print(status_code)
            # send email notification
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()

                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

                subject = 'YOUR SITE IS DOWN!'
                body = f'Response Code: {status_code}, time:{current_time}'
                msg = f'Subject: {subject}\n\n{body}'

                logging.info('Sending Email...')
                smtp.sendmail(EMAIL_ADDRESS, 'niranjan27494@gmail.com', msg)
        else:
            logging.info(f'Website is UP, time:{current_time}')
            print(f'Website is UP, time: {current_time}')
            print(status_code)

    except Exception as e:
        current_time = datetime.datetime.now()
        logging.info(f'Website is DOWN at {current_time}')
        # send email notification
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            subject = 'YOUR SITE IS DOWN!'
            body = f'Not able to check the response of website. Exception occurred. Please check manually'
            msg = f'Subject: {subject}\n\n{body}'

            logging.info('Sending Email...')
            smtp.sendmail(EMAIL_ADDRESS, 'niranjan27494@gmail.com', msg)

sched.start()

