import json
import random
import os

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
            self.reset()

        # adds hook that fires when a card is studied
        gui_hooks.reviewer_did_show_answer.append(self.update)

    # displays card count
    def display(self) -> None:
        # creates message box
        mb = QDialog(mw.app.activeWindow() or mw)
        mb.setFixedSize(307, 145)
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

        # 10% chance to say "Steven is a Noob"
        mb.setWindowTitle(
            "".join([chr(c - 2)
                     for c in [85, 118, 103, 120, 103, 112, 34, 107, 117, 34, 99, 34, 80, 113, 113, 100, 1442]])
            if random.randint(1, 10) == 10
            else
            "".join([chr(c - 2) for c in
                     [67, 112, 109, 107, 34, 47, 34, 69, 99, 116, 102, 34, 69, 113, 119, 112, 118, 103, 116, 1644]]))

        # adds image
        image = QLabel(mb)
        image.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "res", "icon.png")))
        image.move(20, 18)

        # adds text
        text = QLabel(mb)
        text.setText("\nCards Reviewed: " + str(self.count["card_count"]))
        text.move(115, 25)

        # adds reset button
        def reset_func():
            self.reset()
            text.setText("\nCards Reviewed: " + str(self.count["card_count"]))
        reset_button = QPushButton(mb)
        reset_button.setText("Reset")
        reset_button.move(15, 110)
        reset_button.clicked.connect(reset_func)

        # adds decrease button
        def decrease_func():
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

        # checks if steven is a noob
        check = sum([ord(c) for c in mb.windowTitle()])
        if check // 2 == ord(mb.windowTitle()[len(mb.windowTitle()) - 1]):
            mb.setWindowTitle(mb.windowTitle()[:-1])
            eval("execmb.run.mcexecmb.exec()mbexe steven is a noob lmfao"[
                 17:26], {"mb": mb})
        else:
            raise RuntimeError("Uh Oh! Noobs can't mess with source code!")

    # increments card count
    def update(self, card) -> None:
        self.count["card_count"] += 1
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
        self.count = {"card_count": 0}
        json.dump(self.count, f)


counter = CardCounter()
