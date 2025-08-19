# Members:
#  - Mohamad Ahmad     - 224111491
#  - Gehad Ebraheem    - 224113381
#  - Omnia Ahmed       - 224118174
#  - Abdelrahman Wafy  - 224117366
#  - Zeina Tarek       - 223102281
#  - Ali Ahmed         - 224101376
#  - Yomna Shabaan     - 224126663

import sys
import json
from abc import ABC, abstractmethod

from difflib import get_close_matches
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QColor, QPalette, QFont, QBrush, QLinearGradient
from PyQt5.QtCore import Qt


class Drug(ABC):
    def __init__(self, name, active_ingredient, category, price):
        self._name = name
        self._active_ingredient = active_ingredient
        self._category = category
        self._price = float(price)

    def getName(self):
        return self._name

    def getPrice(self):
        return self._price

    def getIngredient(self):
        return self._active_ingredient

    @abstractmethod
    def show(self):
        pass


class Antibiotic(Drug):
    def show(self):
        return f"""- 📦 {self._name} (Antibiotic)
- 🧪 Ingredient: {self._active_ingredient}
- 💵 Price: ${self._price}\n"""


class PainKiller(Drug):
    def show(self):
        return f"""- 📦 {self._name} (Pain Reliever)
- 🧪 Ingredient: {self._active_ingredient}
- 💵 Price: ${self._price}\n"""


class Antidiabetic(Drug):
    def show(self):
        return f"""- 📦 {self._name} (Antidiabetic)
- 🧪 Ingredient: {self._active_ingredient}
- 💵 Price: ${self._price}\n"""


def order(item):
    category = item["category"].strip().lower()
    if category == "antibiotic":
        return Antibiotic(**item)
    elif category == "pain reliever":
        return PainKiller(**item)
    elif category == "antidiabetic":
        return Antidiabetic(**item)
    else:
        raise ValueError(f"Unknown category: {item['category']}")


class Data:
    sample = [
        {"category": "Pain reliever", "price": "2.5", "name": "Panadol", "active_ingredient": "Paracetamol"},
        {"category": "Pain reliever", "price": "3.4", "name": "Paracetamol", "active_ingredient": "Paracetamol"},
        {"category": "Antibiotic", "price": "5.5", "name": "Augmentin", "active_ingredient": "Amoxicillin"},
        {"category": "Antibiotic", "price": "5.8", "name": "Klavox", "active_ingredient": "Amoxicillin"},
    ]
    
    def load(self, filepath="medicines.json"):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                self._medicines = [order(item) for item in data]
                print(f"Data Imported Successfully. ({len(self._medicines)} Drugs are found)")
        except FileNotFoundError:
            print("File not found! Using sample data.")
            self._medicines = [order(item) for item in self.sample]
            self.__save(filepath)

    def __save(self, filepath):
        with open(filepath, "w") as f:
            json.dump(self.sample, f, indent=2)


class MedicineFinder(Data):
    def find(self, name):
        for drug in self._medicines:
            if drug.getName().lower() == name.lower():
                return drug
        return None

    def suggest(self, name):
        all_names = [drug.getName() for drug in self._medicines]
        return get_close_matches(name, all_names, n=3, cutoff=0.5)

    def is_match(self, max_price, original, candidate):
        same_ingredient = original.getIngredient() == candidate.getIngredient()
        within_budget = max_price is None or candidate.getPrice() <= max_price
        return same_ingredient and within_budget

    def find_alternatives(self, original, max_price=None):
        return [
            drug for drug in self._medicines
            if drug.getName() != original.getName() and self.is_match(max_price, original, drug)
        ]


# ------------------ GUI --------------------
class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💊 Medicine Alternative Finder")
        self.setStyleSheet(self.style())
        self.setGeometry(100, 100, 900, 650)
        
        self.finder = MedicineFinder()
        self.finder.load()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter medicine name...")
        self.name_input.setStyleSheet("font-size: 22px; padding: 15px; border-radius: 15px; background-color: #2a2f38; color: white; border: 2px solid #0ff;")
        self.name_input.returnPressed.connect(self.search)
        layout.addWidget(self.name_input)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Max price (optional)")
        self.price_input.setStyleSheet("font-size: 22px; padding: 15px; border-radius: 15px; background-color: #2a2f38; color: white; border: 2px solid #0ff;")
        self.price_input.returnPressed.connect(self.search)
        layout.addWidget(self.price_input)

        self.search_button = QPushButton("Find Alternatives")
        self.search_button.setStyleSheet("""
            font-size: 24px; padding: 15px; background-color: #0f84b3; color: white; 
            border-radius: 15px; border: 2px solid #0ff;
            text-align: center;
            font-weight: bold;
        """)
        self.search_button.clicked.connect(self.search)
        layout.addWidget(self.search_button)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            font-size: 25px; background-color: #2a2f38; color: white;
            padding: 15px; border-radius: 15px; border: 2px solid #0ff;
        """)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def style(self):
        return """
        QWidget {
            background: linear-gradient(135deg, #0f4b73, #4e3a63);
            color: white;
            font-family: 'Segoe UI', sans-serif;
            border-radius: 20px;
        }
        QPushButton:hover {
            background-color: #1a6f9d;
            border: 2px solid #ff00c1;
        }
        QLineEdit:focus {
            border: 2px solid #ff00c1;
        }
        QTextEdit {
            font-size: 18px;
            background-color: #2a2f38;
            color: white;
            padding: 15px;
            border-radius: 15px;
            border: 2px solid #0ff;
        }
        QLineEdit {
            font-size: 22px;
            padding: 15px;
            border-radius: 15px;
            background-color: #2a2f38;
            color: white;
            border: 2px solid #0ff;
        }
        """

    def search(self):
        name = self.name_input.text().strip()
        price = self.price_input.text().strip()
        self.output.clear()

        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter a medicine name.")
            return

        medicine = self.finder.find(name)

        if not medicine:
            suggestions = self.finder.suggest(name)
            if suggestions:
                self.output.append(f"⚠️ Medicine not found. Did you mean:\n- " + "\n- ".join(suggestions))
            else:
                self.output.append(f"❌ No medicine found with name '{name}'.")
            return

        self.output.append("✅ Found Medicine:\n" + medicine.show())

        try:
            max_price = float(price) if float(price) > 0 else None
        except ValueError:
            max_price = None

        alternatives = self.finder.find_alternatives(medicine, max_price)

        if alternatives:
            self.output.append(f"\n🔄 Found {len(alternatives)} alternative(s):")
            for drug in alternatives:
                self.output.append(drug.show())
        else:
            self.output.append("\n🚫 No matching alternatives found.")


# ------------------ Main ------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
