from parse_hh_data import download, parse
import g4f
#vacancy = download.vacancy("36070814")

resume = download.resume("94b3f66a00090f70f10039ed1f785861757934")
resume = parse.resume(resume)

"""
from g4f.client import Client

client = Client()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": ""}],
)
print(response.choices[0].message.content)
"""

print(resume)
#print(resume.get('gender'))
#print(resume.get('education'))
unpack = resume.get('experience')
unpack = str(unpack).replace("{", "").replace("}", "")
print(unpack)
print(resume.get('experience'))
print(type(resume.get('experience')))
#print(download.resume_ids(3, 5, 0, 0))
#print(download.resume_search_page(3, 5, 7, 0))
#print(download.vacancy_ids(3, 5, 7, 0))
#print(download.vacancy_search_page(3, 5, 7, 0))
#print(download.specializations())
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# Настройки почтового сервера Mail.ru
smtp_server = 'smtp.mail.ru' #смтп сервер почты отправителя
port = 465  # Порт для SSL
sender_email = 'zora1337@bk.ru' #отправитель
receiver_email = 'anomalia66@gmail.com' #получатель
password = 'hwpbTeCFxXznCLTUaTDz' #пароль для внешних приложений

# Создание объекта SMTP
server = smtplib.SMTP_SSL(smtp_server, port)

# Логин на почтовом сервере
server.login(sender_email, password)

# Создание сообщения
subject = 'Тема письма'
body = 'Основной текст'

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = Header(subject, 'utf-8')

message.attach(MIMEText(body, 'plain'))

# Отправка письма
server.sendmail(sender_email, receiver_email, message.as_string())

# Закрытие соединения
server.quit()
"""