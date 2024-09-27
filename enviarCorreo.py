import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo_con_imagen(remitent, destiny, subject, body, image_path):
    mensaje = MIMEMultipart("related")
    mensaje['From'] = remitent
    mensaje['To'] = destiny
    mensaje['Subject'] = subject

    html_body = f"""
    <html>
    <body>
        <p>{body}</p>
        <img src="cid:imagen_incrustada" style="width:100%; max-width:600px;"/>
    </body>
    </html>
    """
    mensaje.attach(MIMEText(html_body, 'html'))

    try:
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            from email.mime.image import MIMEImage
            image = MIMEImage(img_data)
            image.add_header('Content-ID', '<imagen_incrustada>')
            mensaje.attach(image)
    except Exception as e:
        print(f"Error al abrir la imagen: {e}")
        return

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitent, 'qjvq wifl ylgm gtlh')
        servidor.sendmail(remitent, destiny, mensaje.as_string())
        print("Correo enviado exitosamente.")
    except smtplib.SMTPException as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        servidor.quit()

remitent = 'alefito2012@gmail.com'
destiny = input('Email destinatario: ')
subject = 'Correo con imagen incrustada'
body = 'Correo de Ejemplo con imagen.'
image_path = 'images/logo.png' #a
enviar_correo_con_imagen(remitent, destiny, subject, body, image_path)

