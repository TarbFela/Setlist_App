from PySide6.QtWidgets import (QApplication,
                               QMainWindow,
                               QListWidget,
                               QVBoxLayout,
                               QHBoxLayout,
                               QWidget,
                               QScrollArea,
                               QPlainTextEdit,
                               QLabel,
                               QPushButton)
from PySide6.QtGui import QFont, QFontDatabase

from time import time, sleep

from SetlistModule import *

header_font = QFont("Helvetica Neue", 16)  # Example: Arial, size 16
header_font.setBold(True)


class SongLibraryGUI(QMainWindow):
    def __init__(self, Library):
        super().__init__()
        self.setWindowTitle("Song Library")
        self.setGeometry(100, 100, 400, 300)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout for main widget
        layout = QHBoxLayout(main_widget)

        # SCROLL AREA STUFF
        scroll_layout = QVBoxLayout()

        self.scroll_area_search_box = QPlainTextEdit()
        self.scroll_area_search_box.setMaximumHeight(25)
        self.scroll_area_search_box.textChanged.connect(self.search_box_update)
        scroll_layout.addWidget(self.scroll_area_search_box)
        scroll_area = QScrollArea()
        scroll_layout.addWidget(scroll_area)

        layout.addLayout(scroll_layout)


        # Song list widget
        self.song_list_widget = QListWidget()

        # Populate song list with songs
        for song in songs:
            self.song_list_widget.addItem(song)

        # Connect the item click signal to the custom function
        self.song_list_widget.itemClicked.connect(self.on_song_clicked)

        # Make the song list scrollable
        scroll_area.setWidget(self.song_list_widget)
        scroll_area.setWidgetResizable(True)


        # SECTION FOR MAIN PAGE
        info_layout = QVBoxLayout()
        header = QLabel("HEADER BABEYYY")

        header.setFont(header_font)
        open_song_button = QPushButton()
        info_layout.addWidget(header)
        info_layout.addWidget(open_song_button)


        layout.addLayout(info_layout)
        #info_layout.addWidget(open_song_button)

    def on_song_clicked(self, item):
        print(item.text())

    time_of_last_update = 0
    def search_box_update(self):
        content = self.scroll_area_search_box.toPlainText()
        if 0 == len(content): return
        if content.endswith('\n'):
            #let's perform a search


            self.scroll_area_search_box.setPlainText("")
            self.scroll_area_search_box.moveCursor(self.scroll_area_search_box.textCursor().End)


def run_gui(songs):
    app = QApplication([])
    gui = SongLibraryGUI(songs)
    gui.show()
    app.exec()

if __name__ == "__main__":

    song_library = load_from_file()

    # Example list of songs
    song_list = [song.name for song in song_library.songs]
    run_gui(song_list)