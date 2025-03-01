from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QListWidget,
    QLineEdit, QTextEdit,
    QInputDialog, QFormLayout
)
import json

'''notes = {
    'Інструкція':{
        'текст':'Це додаток для важливих і неважливих записів',
        'теги':['інструкція','вступний']
    }
}

with open('notes_data.json', 'w') as file:
    json.dump(notes, file, sort_keys=True)'''

app = QApplication([])

notes_win = QWidget()
notes_win.setWindowTitle('Розумні замітки')
notes_win.resize(900,600)
#
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
btn_tag_search = QPushButton('Шукати по замітку по тегу')

list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')
#
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

layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)

notes_win.setLayout(layout_notes)
#
def show_note():
    key = list_notes.selectedItems()[0].text()#ключ - назва обранної замітки

    field_text.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])

list_notes.itemClicked.connect(show_note)


#
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Додавання замітки', 'Введіть назву замітки:')
    if ok and note_name != '':
        notes[note_name] = {
            'текст': '',
            'теги': []
        }
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['теги'])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

btn_note_del.clicked.connect(del_note)
btn_note_save.clicked.connect(save_note)
btn_note_create.clicked.connect(add_note)
#
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

btn_tag_add.clicked.connect(add_tag)
btn_tag_del.clicked.connect(del_tag)
#

with open('notes_data.json', 'r') as file:
    notes = json.load(file)

list_notes.addItems(notes)
#
notes_win.show()
app.exec()
