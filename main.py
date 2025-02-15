from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget,
    QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QListWidget,
    QLineEdit, QTextEdit,
    QInputDialog, QFormLayout
)

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
notes_win.show()
app.exec()