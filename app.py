from flask import Flask, render_template, request, send_file
from PIL import Image
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

app = Flask(__name__)

# Configurations SMTP pour Gmail
EMAIL_ADDRESS = r'f.benamara2003@gmail.com'
EMAIL_PASSWORD = r"tevq iheb czak fbvw"
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


def send_email(pdf_bytes):
    # Configuration du serveur SMTP
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()

    # Connexion au compte Gmail
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    # Création du message
    message = MIMEMultipart()
    message['From'] = EMAIL_ADDRESS
    message['To'] = 'faridbenamaraip8@icloud.com'  # Envoyer l'e-mail à la même adresse pour cet exemple
    message['Subject'] = 'Conversion d\'image en PDF'

    # Ajout du PDF en pièce jointe
    pdf_attachment = MIMEApplication(pdf_bytes.read(), _subtype="pdf")
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename='image_convertie.pdf')
    message.attach(pdf_attachment)

    # Envoi de l'e-mail
    server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message.as_string())

    # Fermeture de la connexion SMTP
    server.quit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'convert' in request.form:
            # Code pour la conversion en PDF
            try:
                img = Image.open(request.files['file'])
                pdf_bytes = BytesIO()
                img.save(pdf_bytes, format='PDF')
                pdf_bytes.seek(0)
                return send_file(pdf_bytes, as_attachment=True, download_name='image_convertie.pdf',
                                 mimetype='application/pdf')

            except Exception as e:
                return f"Une erreur s'est produite lors de la conversion : {str(e)}"

        elif 'send_email' in request.form:
            # Code pour l'envoi par e-mail
            try:
                img = Image.open(request.files['file'])
                pdf_bytes = BytesIO()
                img.save(pdf_bytes, format='PDF')
                pdf_bytes.seek(0)
                send_email(pdf_bytes)
                return "E-mail envoyé avec succès."

            except Exception as e:
                return f"Une erreur s'est produite lors de l'envoi par e-mail : {str(e)}"

    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

