import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header


class Sender:
    def __init__(self):
        self.user = "user@yandex.ru"
        self.passwd = "password"
        self.server = "smtp.yandex.ru"
        self.port = 587

    def generate_body_email(self, to_user: str, text: str):

        to = to_user
        subject = "Тестовое задание"
        text = text

        file_path = os.getcwd() + "/result.xlsx"

        if not os.path.exists(file_path):
            print(f"Файл не найден: {file_path}")
            return False

        msg = MIMEMultipart()

        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = self.user
        msg['To'] = to

        msg.attach(MIMEText(text, 'plain', 'utf-8'))

        with open(file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())

            encoders.encode_base64(part)

            filename = os.path.basename(file_path)

            part.add_header(
                'Content-Disposition',
                'attachment',
                filename=Header(filename, 'utf-8').encode()
            )

            msg.attach(part)
        return msg

    def send_email(self, to_user: str, msg):
        try:
            smtp = smtplib.SMTP(self.server, self.port)
            smtp.starttls()
            smtp.ehlo()

            smtp.login(self.user, self.passwd)

            smtp.sendmail(self.user, to_user, msg.as_string())

            return True

        except smtplib.SMTPAuthenticationError:
            print("Ошибка аутентификации почты!")
            return False

        except smtplib.SMTPException as err:
            print(f"Ошибка SMTP: {err}")
            return False

        except Exception as err:
            print(str(err))
            return False

        finally:
            if 'smtp' in locals():
                smtp.quit()
