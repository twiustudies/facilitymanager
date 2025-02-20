import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QVBoxLayout, QWidget

class FacilitySwitcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Facility Selector")
        self.resize(400, 200)

        # Create a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        # new comment
        # Label for instructions
        self.instruction_label = QLabel("Select a facility:")
        layout.addWidget(self.instruction_label)
        # another new comment
        # Create a combo box (drop-down)
        self.combo_box = QComboBox()
        facilities = [
            'production unit 1', 
            'production unit 2', 
            'control', 
            'machinery', 
            'utilities'
        ]
        self.combo_box.addItems(facilities)
        self.combo_box.currentTextChanged.connect(self.facility_changed)
        layout.addWidget(self.combo_box)
        # other comment
        # Label to display the current selection
        self.current_facility_label = QLabel(f"Current Facility: {self.combo_box.currentText()}")
        layout.addWidget(self.current_facility_label)
    # new comment
    def facility_changed(self, facility):
        """Update the label when a new facility is selected."""
        self.current_facility_label.setText(f"Current Facility: {facility}")

# a new comment
# here is another comment
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FacilitySwitcher()
    window.show()
    sys.exit(app.exec_())
