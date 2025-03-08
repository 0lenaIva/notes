from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QListWidget,
    QLineEdit, QTextEdit,
    QInputDialog
)
import json
import sys
import os
import logging

# Визначення шляху до виконуваного файлу
if getattr(sys, 'frozen', False):
    current_path = os.path.dirname(sys.executable)  # Для PyInstaller
else:
    current_path = os.path.dirname(__file__)  # Для звичайного запуску

file_path = os.path.join(current_path, 'notes_data.json')

# Ініціалізація логування
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Перевірка, чи існує файл, і його відкриття
notes = {}
if os.path.exists(file_path):
    try:
        with open(file_path, 'r') as file:
            notes = json.load(file)
    except Exception as e:
        logging.error(f'Error reading {file_path}: {e}')

app = QApplication([])

notes_win = QWidget()
notes_win.setWindowTitle('Розумні замітки')
notes_win.resize(900, 600)

# Створення елементів інтерфейсу
list_notes = QListWidget()
list_notes_label = QLabel('Список заміток')

btn_note_create = QPushButton('Створити замітку')
btn_note_del = QPushButton('Видалити замітку')
btn_note_save = QPushButton('Зберегти замітку')

field_tag = QLineEdit()
field_tag.setPlaceholderText('Введіть тег')

field_text = QTextEdit()

btn_tag_add = QPushButton('Додати до замітки')
btn_tag_del = QPushButton('Відкріпити від замітки')
btn_tag_search = QPushButton('Шукати замітку по тегу')

list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')

# Розмітка
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(btn_note_create)
row_1.addWidget(btn_note_del)

row_2 = QHBoxLayout()
row_2.addWidget(btn_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(btn_tag_add)
row_3.addWidget(btn_tag_del)

row_4 = QHBoxLayout()
row_4.addWidget(btn_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)

notes_win.setLayout(layout_notes)

# Функція для показу замітки
def show_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        field_text.setText(notes[key]['текст'])
        list_tags.clear()
        list_tags.addItems(notes[key]['теги'])

list_notes.itemClicked.connect(show_note)

# Функція для додавання замітки
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Додавання замітки', 'Введіть назву замітки:')
    if ok and note_name != '':
        notes[note_name] = {'текст': '', 'теги': []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['теги'])

# Функція для збереження замітки
def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText()
        with open(file_path, 'w') as file:
            json.dump(notes, file, sort_keys=True)

# Функція для видалення замітки
def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open(file_path, 'w') as file:
            json.dump(notes, file, sort_keys=True)

# Функція для додавання тега
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if tag and tag not in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            with open(file_path, 'w') as file:
                json.dump(notes, file, sort_keys=True)

# Функція для видалення тега
def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        if tag in notes[key]['теги']:
            notes[key]['теги'].remove(tag)
            list_tags.clear()
            list_tags.addItems(notes[key]['теги'])
            with open(file_path, 'w') as file:
                json.dump(notes, file, sort_keys=True)

# Пошук тега
def search_tag():
    tag = field_tag.text()
    if tag:
        notes_filtered = {note: data for note, data in notes.items() if tag in data['теги']}
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    else:
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)

# Підключення кнопок до функцій
btn_note_del.clicked.connect(del_note)
btn_note_save.clicked.connect(save_note)
btn_note_create.clicked.connect(add_note)
btn_tag_add.clicked.connect(add_tag)
btn_tag_del.clicked.connect(del_tag)
btn_tag_search.clicked.connect(search_tag)

# Завантаження заміток в список
list_notes.addItems(notes)

# Показ вікна
notes_win.show()
app.exec()
