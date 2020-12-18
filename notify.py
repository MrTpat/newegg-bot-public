from ezSMS.messenger import Messenger
import smtplib, ssl

def notify(msg: str, email: str, pw: str, server: str, number: str) -> None:
    m = Messenger(email, pw, server)
    try:
        m.sendSMS(number, msg)
        colors.printSuccess('Sent notification')
    except Exception as e:
        colors.printFail('Couldnt send message: ' + e)
