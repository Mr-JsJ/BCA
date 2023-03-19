import yagmail
import os
def mail(mail,img):
    receiver = "reciver email id"  # receiver email address
    body = str(mail)
    filename="mailed"+os.sep+str(img)

# mail information
    yag = yagmail.SMTP("senter email id", "password")

# sent the mail
    yag.send(
        to=receiver,
        subject="****ALERT****",  # email subject
        contents=body,
        attachments=filename,
    )
