import json
import sys

import anki.cards
import anki.stats
from aqt import mw, gui_hooks
from aqt.qt import *


# Anki Card Counter
# Creates a new menu item under "Tools" that displays the number of cards that you have studied
class CardCounter:
    # class constructor
    def __init__(self):
        # adds menu option
        self.action = QAction("Card Count", mw)
        mw.form.menuTools.addAction(self.action)
        qconnect(self.action.triggered, self.display)

        # loads card_count.json and creates if not found
        try:
            self.file = os.path.join(os.path.dirname(__file__), "user_files", "card_count.json")
            self.count = json.load(open(self.file))
        except (json.JSONDecodeError, FileNotFoundError):
            self.count = {}
            self.reset()

        # adds hook that fires when a card is studied
        gui_hooks.reviewer_did_show_answer.append(self.update)
        gui_hooks.collection_did_load.append(self.update_all)

    # displays card count
    def display(self) -> None:
        # creates message box
        mb = QDialog(mw.app.activeWindow() or mw)
        mb.setFixedSize(307, 145)
        mb.setWindowTitle("Anki - Card Counter")
        mb.setStyleSheet(
            """
            QLabel {
                margin: 5px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton {
                width: 80px;
                font-size: 12px;
            }
            """
        )

        # adds image
        image = QLabel(mb)
        image.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "res", "icon.png")))
        image.move(20, 18)

        # adds text
        text = QLabel(mb)
        text.setText("\nCards Reviewed: " + str(self.count["card_count"]))
        text.move(115, 25)

        # adds reset button
        def reset_func() -> None:
            self.reset()
            text.setText("\nCards Reviewed: " + str(self.count["card_count"]))

        reset_button = QPushButton(mb)
        reset_button.setText("Reset")
        reset_button.move(15, 110)
        reset_button.clicked.connect(reset_func)

        # adds decrease button
        def decrease_func() -> None:
            self.decrease()
            text.setText("\nCards Reviewed: " + str(self.count["card_count"]))

        decrease_button = QPushButton(mb)
        decrease_button.setText("Decrease 10")
        decrease_button.move(110, 110)
        decrease_button.clicked.connect(decrease_func)

        # adds ok button
        ok_button = QPushButton(mb)
        ok_button.setText("OK")
        ok_button.move(205, 110)
        ok_button.clicked.connect(lambda: mb.close())

        mb.exec()

    # increments card count
    def update(self, card: anki.cards.Card) -> None:
        if "cards" not in self.count:
            self.count["cards"] = {}
        if str(card.id) not in self.count["cards"]:
            self.count["cards"][str(card.id)] = 0
        self.count["card_count"] += 1
        self.count["cards"][str(card.id)] += 1
        f = open(self.file, "w")
        json.dump(self.count, f)

    # updates all card counts
    def update_all(self, collection) -> None:
        if "cards" not in self.count:
            self.count["cards"] = {}
        for card_id in mw.col.find_cards(""):
            card = mw.col.getCard(card_id)
            if str(card_id) not in self.count["cards"]:
                self.count["cards"][str(card_id)] = 0
            self.count["card_count"] += max(card.reps - self.count["cards"][str(card_id)], 0)
            self.count["cards"][str(card_id)] = card.reps
        f = open(self.file, "w")
        json.dump(self.count, f)

    # decreases card count by 10
    def decrease(self) -> None:
        self.count["card_count"] = max(self.count["card_count"] - 10, 0)
        f = open(self.file, "w")
        json.dump(self.count, f)

    # resets card count
    def reset(self) -> None:
        if not os.path.exists(os.path.dirname(self.file)):
            os.makedirs(os.path.dirname(self.file))
        f = open(self.file, "w")
        self.count["card_count"] = 0
        json.dump(self.count, f)
