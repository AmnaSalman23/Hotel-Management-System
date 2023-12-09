from PyQt5.QtWidgets import QMessageBox

def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(f"<b>Error:</b> {message}")
        error_dialog.setWindowTitle("Error")
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec_()

def show_success_message(self, message):
        success_dialog = QMessageBox()
        success_dialog.setIcon(QMessageBox.Information)
        success_dialog.setText(f"<b>Success:</b> {message}")
        success_dialog.setWindowTitle("Success")
        success_dialog.setStandardButtons(QMessageBox.Ok)
        success_dialog.exec_()
