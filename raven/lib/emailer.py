import logging
import config
import smtplib
import traceback

def send_email(subject, body):
    import smtplib

    message = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s\r\n" % (config.EMAIL_HOST_USER, ", ".join(config.EMAIL_RECEIVER), subject, body)
    try:
        smtpserver = smtplib.SMTP(config.EMAIL_HOST)
        smtpserver.set_debuglevel(0)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(config.EMAIL_HOST_USER, config.EMAIL_HOST_PASSWORD)
        smtpserver.sendmail(config.EMAIL_HOST_USER, config.EMAIL_RECEIVER, message)
        smtpserver.quit()  
        smtpserver.close() 
        logging.info("send mail to %s success" % ",".join(config.EMAIL_RECEIVER))      
    except:
        logging.error("send mail failed")
        traceback.print_exc()