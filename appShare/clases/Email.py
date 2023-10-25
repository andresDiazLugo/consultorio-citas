from django.core.mail import EmailMultiAlternatives
class Email:
    def __init__(self,email, name, token):
        self.email = email
        self.nombre = name
        self.token = token
    def __repr__(self):
        return f'MiClase(email={self.email}, nombre={self.nombre}, token={self.token})'
    def  sendConfirm(self):
        subject = 'Confirma tu cuenta'
        text_content = 'Cuerpo del correo electrónico en texto plano'
        html_content = f'<p>Hola {self.nombre} confirma tu cuenta haciendo click . <a href="http://127.0.0.1:8000/confirmarcuenta?token={self.token}">Aquí</a>, <strong> si tu no solicitate la cuenta ignora este mensaje</strong></p>'
        from_email = 'clinica'
        to_emails = [self.email]

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    def sendResetPassword(self):
        subject = 'Olvidaste Tu contraseña'
        text_content = 'Cuerpo del correo electrónico en texto plano'
        html_content = f'<p>Hola {self.nombre} deberas hacer clik . <a href="http://127.0.0.1:8000/restablecer?token={self.token}">Aquí</a> para poder crear una nueva contraseña y asi poder acceder a tu cuenta. <strong> SI TU NO SOLICITASTE RESETEAR TU CONTRASEÑA IGNORA ESTE MENSAJE</strong></p>'
        from_email = 'clinica'
        to_emails = [self.email]

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        msg.attach_alternative(html_content, "text/html")
        msg.send()