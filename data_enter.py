from tkinter import *
from tkinter import ttk, messagebox

from parse_hh_data import download, parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from g4f.client import Client
import g4f

from g4f.Provider import (
    __all__
)

import pymysql
import json

root = Tk()
root.title("resume finder")
root.geometry("950x450")
root.call("source", "Azure/azure.tcl")
root.call("set_theme", "light")

main_menu = Menu()

def edit_email():

    #окно с настройками почты и smtp сервера
    email_window = Toplevel(root)
    email_window.title("Параметры почты")
    #Настройка растягивания элементов под ширину окна
    for c in range(3): email_window.columnconfigure(index=c, weight=1)

    #поле ввода почты
    email_label = Label(email_window, text="Адрес электронной почты отправителя")
    email_label.grid(column=0, row=0, columnspan=3)
    email_entry = Entry(email_window)
    email_entry.grid(column=0, row=1, columnspan=3)
    email_entry.insert(0, "zora1337@bk.ru")

    #поле ввода пароля
    pass_label = Label(email_window, text="Пароль для внешних приложений")
    pass_label.grid(column=0, row=2, columnspan=3)
    pass_entry = Entry(email_window, show="*")
    pass_entry.grid(column=0, row=3, columnspan=3)
    pass_entry.insert(0, "Текущий pass")

    #поле ввода сервера
    server_label = Label(email_window, text="Почтовый сервер отправителя")
    server_label.grid(column=0, row=4, columnspan=3)
    server_entry = Entry(email_window)
    server_entry.grid(column=0, row=5, columnspan=3)
    server_entry.insert(0, "mail.ru")

    #поле ввода порта
    port_label = Label(email_window, text="Порт почтового сервера")
    port_label.grid(column=0, row=6, columnspan=3)
    port_entry = Entry(email_window)
    port_entry.grid(column=0, row=7, columnspan=3)
    port_entry.insert(0, "465")

    with open('mail_content.json', 'r', encoding='utf-8') as file:
        mail_content = json.load(file)

    theme_label = Label(email_window, text="Тема письма:")
    theme_label.grid(column=0, row=8, columnspan=3, pady=10)

    theme_entry = Entry(email_window, width=50)
    theme_entry.grid(column=0, row=9, columnspan=3, pady=10)
    theme_entry.insert(0, mail_content.get("subject", ""))

    text_label = Label(email_window, text="Текст письма:")
    text_label.grid(column=0, row=10, columnspan=3, pady=10)

    text_entry = Text(email_window, height=10, width=50)
    text_entry.grid(column=0, row=11, columnspan=3, pady=10)
    text_entry.insert(INSERT, mail_content.get("body", ""))

    save_button = Button(email_window, text="Сохранить")
    save_button.grid(column=0, row=12, columnspan=3, pady=10)

def edit_base():

    #окно с настройками почты и smtp сервера
    base_window = Toplevel(root)
    base_window.title("Параметры подключения к базе данных")
    #Настройка растягивания элементов под ширину окна
    for c in range(3): base_window.columnconfigure(index=c, weight=1)

    # Чтение значений из внешнего JSON файла
    with open('config.json', 'r') as json_file:
        data = json.load(json_file)
        host = data['host']
        port = data['port']
        user = data['user']
        password = data['password']
        database = data['database']

    def save_settings():
        data = {
            'host': host_entry.get(),
            'port': int(port_entry.get()),
            'user': user_entry.get(),
            'database': database_entry.get(),
            'password': pass_entry.get()
        }

        with open('config.json', 'w') as json_file:
            json.dump(data, json_file)


    #поле ввода хоста
    host_label = Label(base_window, text="host")
    host_label.grid(column=0, row=0, columnspan=3)
    host_entry = Entry(base_window)
    host_entry.grid(column=0, row=1, columnspan=3, padx=10)
    host_entry.insert(0, host)

    #поле ввода порта
    port_label = Label(base_window, text="port")
    port_label.grid(column=0, row=2, columnspan=3)
    port_entry = Entry(base_window)
    port_entry.grid(column=0, row=3, columnspan=3, padx=10)
    port_entry.insert(0, port)

    #поле ввода юзера
    user_label = Label(base_window, text="user")
    user_label.grid(column=0, row=4, columnspan=3)
    user_entry = Entry(base_window)
    user_entry.grid(column=0, row=5, columnspan=3, padx=10)
    user_entry.insert(0, user)

    #поле ввода бд
    database_label = Label(base_window, text="database")
    database_label.grid(column=0, row=6, columnspan=3)
    database_entry = Entry(base_window)
    database_entry.grid(column=0, row=7, columnspan=3, padx=10)
    database_entry.insert(0, database)

    #поле ввода пароля
    pass_label = Label(base_window, text="password")
    pass_label.grid(column=0, row=8, columnspan=3)
    pass_entry = Entry(base_window, show="*")
    pass_entry.grid(column=0, row=9, columnspan=3, padx=10)
    pass_entry.insert(0, "6H53PVXQWp")

    # привязываем save_settings() к кнопке "Сохранить"
    save_button = Button(base_window, text="Сохранить", command=save_settings)
    save_button.grid(column=0, row=10, columnspan=3, pady=10)
    def test_connection():
        try:
            connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
            messagebox.showinfo("Статус", "Успешное соединение с базой данных")
            base_window.destroy()
        except pymysql.Error as e:
            messagebox.showerror("Статус", f"Ошибка: {str(e)}")
            base_window.destroy()

    test_connection_button = Button(base_window, text="Тест соединения", command=test_connection)
    test_connection_button.grid(column=0, row=11, columnspan=3, pady=10)



def edit_style():

    #окно с настройками стиля
    edit_style_window = Toplevel(root)
    edit_style_window.title("Общие настройки")
    #Настройка растягивания элементов под ширину окна
    for c in range(3): edit_style_window.columnconfigure(index=c, weight=1)

    #функция смены темы по событию
    def change_theme(event):
        selected_theme = themeBox.get()
        if selected_theme == "Light":
            root.call("set_theme", "light")
        elif selected_theme == "Dark":
            root.call("set_theme", "dark")

    style_label = Label(edit_style_window, text="Тема приложения:") #название переключалки
    style_label.grid(column=0, row=0,columnspan=3)

    themeBox = ttk.Combobox(edit_style_window, values=["Light", "Dark"], state="readonly") #коробка значений
    themeBox.grid(column=0, row=1, columnspan=3, padx=10, pady=10)

    token_label = Label(edit_style_window, text="Токен HeadHunterAPI:") #название переключалки
    token_label.grid(column=0, row=2,columnspan=3)

    token_entry = ttk.Entry(edit_style_window)
    token_entry.grid(column=0, row=3, columnspan=3, padx=10, pady=10)

    themeBox.bind("<<ComboboxSelected>>", change_theme)  # привязка функцию к событию выбора из combobox


settings_menu = Menu(tearoff=0)
main_menu.add_cascade(label="Настройки", menu=settings_menu)
settings_menu.add_command(label="База данных", command=edit_base)
settings_menu.add_command(label="Почта", command=edit_email)
settings_menu.add_command(label="Общее", command=edit_style)


#Таблица
table = ttk.Treeview(columns=('id_resume', 'gender', 'contacts', 'skills', 'last_work'), show='headings')
table.grid(column=0, row=4, columnspan=3, sticky='ew', padx=50)

table.heading('id_resume', text='ID Резюме')
table.column('id_resume', minwidth=0, width=100, anchor='center')
table.heading('gender', text='Пол')
table.column('gender', minwidth=0, width=70, anchor='center')
table.heading('contacts', text='Контакты')
table.column('contacts', anchor='center')
table.heading('skills', text='Навыки')
table.heading('last_work', text='Места работы')

# Создание скроллбара таблице
tableScrollbar = ttk.Scrollbar(orient="vertical", command=table.yview)
table.configure(yscrollcommand=tableScrollbar.set)
tableScrollbar.grid(row=4, column=3, sticky='ns')

#тестовые ячейки
table.insert("", "end", values=("test", "Мужчина", "marl.marl@bk.ru","some skills", "last work"))
table.insert("", "end", values=("test2", "Мужчина", "anomalia66@gmail.com","some skills2", "last work2"))

#ТЕСТ ОТОБРАЖАЛКИ
def open_additional_window(event):
    selected_item = table.item(table.selection())  # Получаем выбранный элемент
    id_resume = selected_item['values'][0]
    gender = selected_item['values'][1]
    contacts = selected_item['values'][2]
    skills = selected_item['values'][3]
    last_work = selected_item['values'][4]

    # Создаем новое окно для отображения информации
    additional_window = Toplevel()
    additional_window.title("Полная информация")

    # Создаем метки для отображения данных
    short_data_bar = ttk.Frame(additional_window)
    short_data_bar.grid(column=0, row=0, columnspan=3)
    Label(short_data_bar, text=f"ID Резюме: {id_resume}", cursor="hand2").grid(column=0, row=0, padx=10, pady=10)

    Label(short_data_bar, text=f"Пол: {gender}").grid(column=1, row=0, padx=10, pady=10)

    Label(short_data_bar, text=f"Контакты: {contacts}").grid(column=2, row=0, padx=10, pady=10)

    skills_text = Text(additional_window)
    skills_text.insert('1.0', f"Навыки: {skills}")
    skills_text.grid(column=0, row=2, padx=10, pady=10)
    skills_text.config(wrap=WORD)

    last_work_text = Text(additional_window)
    last_work_text.insert('1.0', f"Места работы: {last_work}")
    last_work_text.grid(column=1, row=2, padx=10, pady=10)

# Привязываем обработчик события к таблице
table.bind('<Double-1>', open_additional_window)

'''
Тут у нас распределение элементов по колонкам и ярлык
ttk более бутиковый
'''

for c in range(4): root.columnconfigure(index=c, weight=1)
paramLabel = Label(root, text="Параметры поиска", font=("", 14))
paramLabel.grid(column=0, row=0, columnspan=3)

#поля с выбором параметров поиска
searchRegions = {"Екатеринбург": 3, "Москва": 1, "Калининград": 41}
regionBox = ttk.Combobox(values=list(searchRegions.keys()), state="readonly")
regionBox.grid(column=0, row=1)

searchSpec = {"Механик": 5, "Менеджер": 3}
specBox = ttk.Combobox(values=list(searchSpec.keys()), state="readonly")
specBox.grid(column=1, row=1)

searchPeriod = {"День": 1, "Неделя": 7, "Месяц": 30, "За всё время": 0}
periodBox = ttk.Combobox(values=list(searchPeriod.keys()), state="readonly")
periodBox.grid(column=2, row=1)

#Надписи под полями
label_region = ttk.Label(text="Регион")
label_region.grid(column=0, row=2)

label_spec = ttk.Label(text="Специализация")
label_spec.grid(column=1, row=2)

label_period = ttk.Label(text="Период поиска")
label_period.grid(column=2, row=2)


#поиск
def parseBtn_Click(event=None):
    #список найденных айди
    idList = download.resume_ids(searchRegions[regionBox.get()], searchSpec[specBox.get()], searchPeriod[periodBox.get()], 0)
    print(idList)
    print(str(searchRegions[regionBox.get()]) + " id региона " +
          str(searchSpec[specBox.get()]) + " id специальности " +
          str(searchPeriod[periodBox.get()]) + " Период поиска")#Вывод параметров в консоль которые принимает метод выше
    #тестовое заполнение таблицы айдишками(нужно добавлять только те айдишки которых ещё нет)

    #Заполнение таблицы полученными данными
    for i in idList:
        resume = download.resume(i)
        resume = parse.resume(resume)
        table.insert("", "end", values=(i, resume.get('gender'), resume.get('contacts'),
                                        resume.get('skills'), str(resume.get('experience')).replace("{", "").replace("}", "").replace("[", "").replace("]", "")))

#функция метки
table.tag_configure("marked", background="pink")
def mark_selected_row(event):
    selected_item = table.selection()
    if selected_item:
        tags = table.item(selected_item, option="tags")
        if "marked" in tags:
            table.item(selected_item, tags="")
        else:
            table.item(selected_item, tags="marked")

#функция удаления строк
def delete_selected_row(event=None):
    selected_rows = table.selection()
    if not selected_rows and event==None:
        messagebox.showwarning("Внимание", "Выделите строки для удаления")
        return
    for row_id in selected_rows:
        table.delete(row_id)


#функция добавления резюме вручную
def add_by_hand():
    addbyhand_window = Toplevel(root)
    addbyhand_window.title("Добавить резюме по ID")
    addbyhand_window.geometry("+500+350")
    addbyhand_window.attributes('-topmost', 'true')

    id_label = ttk.Label(addbyhand_window, text="ID Резюме")
    id_label.pack()

    id_entry = ttk.Entry(addbyhand_window)
    id_entry.pack()

    def paste_from_clipboard():
        text = root.clipboard_get()
        id_entry.insert(END, text)

    def get_resume():
        if len(id_entry.get())==38:
            resume = download.resume(id_entry.get())
            resume = parse.resume(resume)
            table.insert("", "end", values=(id_entry.get(),
                                            resume.get('gender'),
                                            resume.get('contacts'),
                                            resume.get('skills'),
                                            str(resume.get('experience'))))
        else: messagebox.showinfo( "Внимание", "Введите корректный ID")

    paste_button = ttk.Button(addbyhand_window, text="Вставить из буфера обмена", command=paste_from_clipboard)
    paste_button.pack(padx=5, pady=5)

    submit_button = ttk.Button(addbyhand_window, text="Добавить в таблицу", command=get_resume)
    submit_button.pack(padx=5, pady=5)

#нейросеть
def ask_gpt(question):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.Liaobots,
        messages=[{"role": "user", "content": question}],
        #proxy="http://64.112.184.89:3128",
    )

    return response.choices[0].message.content


def resume_analys(event=None):
    resume_analys_window = Toplevel(root)
    resume_analys_window.title("Анализ резюме")
    resume_analys_window.geometry("+500+350")
    resume_analys_window.attributes('-topmost', 'true')

    selected_item = table.item(table.selection())

    answer = ask_gpt("Ответь на русском, проанализируй это резюме, коротко расскажи о кандидате и прошлых его местах работы, пожалуйста: " +
                     str(selected_item.get('values')[1:5]))#из словаря извлекается список и срезаются элементы

    skills_text = Text(resume_analys_window)
    skills_text.insert('1.0', answer)
    skills_text.pack()
    skills_text.config(wrap=WORD)


def send_email(event=None):
    if not table.selection():
        messagebox.showwarning(title=" ", message="Выберите контакт перед отправкой письма")
        return

    item = table.selection()[0] #Выбор ячейки контактов
    contacts = table.item(item, 'values')[2]
    if contacts == "":
        messagebox.showwarning(title=" ", message="Контакты не найдены")
        return
    messagebox.showinfo(title=" ", message="Письмо отправлено")

    smtp_server = 'smtp.mail.ru'  # смтп сервер почты отправителя
    port = 465  # Порт для SSL
    sender_email = 'zora1337@bk.ru'  # отправитель
    receiver_email = contacts  # получатель
    password = 'hwpbTeCFxXznCLTUaTDz'  # пароль для внешних приложений

    # Создание объекта SMTP
    server = smtplib.SMTP_SSL(smtp_server, port)

    # Логин на почтовом сервере
    server.login(sender_email, password)

    with open('mail_content.json', 'r', encoding='utf-8') as file:
        mail_content = json.load(file)

    # Создание сообщения
    subject = mail_content['subject']
    body = mail_content['body']

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = Header(subject, 'utf-8')

    message.attach(MIMEText(body, 'plain'))

    # Отправка письма
    server.sendmail(sender_email, receiver_email, message.as_string())

    # Закрытие соединения
    server.quit()

def view_test_results():
    table_window = Toplevel()
    table_window.title("Результаты тестирования кандидатов")

    # Создаем таблицу
    results_table = ttk.Treeview(table_window, columns=('ID', 'Email', 'Верные ответы', 'Желание работать'))
    results_table.heading('#0', text='ID')
    results_table.heading('#1', text='Email')
    results_table.heading('#2', text='Верные ответы')
    results_table.heading('#3', text='Желание работать')

    # Добавляем данные в таблицу (здесь можно использовать реальные данные)
    results_table.insert('', 'end', text='test1', values=('marl.marl@bk.ru', '1', 'Да'))
    results_table.insert('', 'end', text='test2', values=('anomalia66@gmail.com', '2', 'Нет'))

    results_table.pack()

# панель инструментов
toolbar = ttk.Frame(root)
toolbar.grid(column=0, row=3, columnspan=3)

#иконки
search_icon = PhotoImage(file="icons/search.png")
star_icon = PhotoImage(file="icons/star.png")
trash_icon = PhotoImage(file="icons/trash.png")
add_icon = PhotoImage(file="icons/add.png")
stat_icon = PhotoImage(file="icons/stats.png")
email_icon = PhotoImage(file="icons/email.png")
tests_icon = PhotoImage(file="icons/test.png")

# кнопки
parseBtn = ttk.Button(toolbar, text="Поиск", command=parseBtn_Click, image=search_icon, compound=LEFT)
parseBtn.pack(side=LEFT, padx=1)

likeBtn = ttk.Button(toolbar, text="Пометить", command=mark_selected_row, image=star_icon, compound=LEFT)
likeBtn.pack(side=LEFT, padx=1)

addbyhandBtn = ttk.Button(toolbar, text="Добавить", command=add_by_hand, image=add_icon, compound=LEFT)
addbyhandBtn.pack(side=LEFT, padx=1)

deleteBtn = ttk.Button(toolbar, text="Удалить", command=delete_selected_row, image=trash_icon, compound=LEFT)
deleteBtn.pack(side=LEFT, pady=10, padx=1)

analysBtn = ttk.Button(toolbar, text="Анализ", command=resume_analys, image=stat_icon, compound=LEFT)
analysBtn.pack(side=LEFT, pady=10, padx=1)

emailBtn = ttk.Button(toolbar, text="Письмо", command=send_email, image=email_icon, compound=LEFT)
emailBtn.pack(side=LEFT, pady=10, padx=1)

testsBtn = ttk.Button(toolbar, text="Тесты", command=view_test_results, image=tests_icon, compound=LEFT)
testsBtn.pack(side=LEFT, pady=10, padx=1)

root.bind("<Shift-S>", send_email)
root.bind("<Delete>", delete_selected_row)
root.bind("<m>", mark_selected_row)
root.bind("<Shift-W>", parseBtn_Click)
root.bind("<Shift-A>", resume_analys)


"""
gridBtn = Button(root, text="0")
gridBtn.grid(column=0, row=5)
gridBtn = Button(root, text="1")
gridBtn.grid(column=1, row=5)
gridBtn = Button(root, text="2")
gridBtn.grid(column=2, row=5)
"""
root.config(menu=main_menu)
root.mainloop()
