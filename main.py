from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout
import sys
from core import logic

class VendingMachineWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vending Machine")

        self.label_amount = QLabel(f"Current amount: {logic.state['current_amount']} baht")
        self.label_message = QLabel("")

        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(self.label_amount)
        self.layout_main.addWidget(self.label_message)

        # --- Coin buttons ---
        self.layout_coins = QHBoxLayout()
        for coin in [1, 5, 10]:
            btn = QPushButton(f"Insert {coin} baht")
            btn.clicked.connect(lambda checked, c=coin: self.insert_coin(c))
            self.layout_coins.addWidget(btn)
        self.layout_main.addLayout(self.layout_coins)

        # --- Product buttons ---
        self.product_buttons = []
        self.layout_products = QVBoxLayout()
        self.refresh_product_buttons()
        self.layout_main.addLayout(self.layout_products)

        container = QWidget()
        container.setLayout(self.layout_main)
        self.setCentralWidget(container)

    def refresh_product_buttons(self):
        # Clear old buttons
        for i in reversed(range(self.layout_products.count())):
            widget = self.layout_products.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Create buttons dynamically
        products = logic.db.get_products()
        self.product_buttons = []
        for p in products:
            product_id, name, price, stock = p
            btn = QPushButton(f"Buy {name} ({price} baht) - Stock: {stock}")
            btn.clicked.connect(lambda checked, pid=product_id: self.buy_product(pid))
            self.layout_products.addWidget(btn)
            self.product_buttons.append(btn)

    def insert_coin(self, coin):
        msg = logic.insert_coin(coin)
        self.label_amount.setText(f"Current amount: {logic.state['current_amount']} baht")
        self.label_message.setText(msg)

    def buy_product(self, product_id):
        msg = logic.purchase_product(product_id)
        self.label_amount.setText(f"Current amount: {logic.state['current_amount']} baht")
        self.label_message.setText(msg)
        self.refresh_product_buttons()  # Update stock display

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VendingMachineWindow()
    window.show()
    sys.exit(app.exec())
