import sys
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QCheckBox, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QTimer, Qt
from plyer import notification

class NetworkMonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window icon
        self.setWindowIcon(QIcon('logo.png'))  # Replace 'logo.png' with the path to your icon file

        # Set window title
        self.setWindowTitle("Network Data Consumption Monitor")

        # Create main widget and set layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        # Add logo label
        logo_label = QLabel(self)
        pixmap = QPixmap("logo.png")  # Replace "logo.png" with the path to your logo image
        pixmap = pixmap.scaledToWidth(100)  # Resize the logo to width 100
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)  # Center the logo horizontally
        self.layout.addWidget(logo_label)

        # Add data usage label
        self.data_usage_label = QLabel()
        font = QFont()
        font.setPixelSize(30)  # Set font size to 30 pixels
        self.data_usage_label.setFont(font)
        self.data_usage_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.data_usage_label)

        # Add limit input
        limit_layout = QHBoxLayout()
        limit_label = QLabel("Set data limit (MB):")
        self.limit_input = QLineEdit(self)
        self.limit_input.setPlaceholderText("Enter data limit")
        limit_layout.addWidget(limit_label)
        limit_layout.addWidget(self.limit_input)
        self.layout.addLayout(limit_layout)

        # Add table widget for displaying apps consuming data
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Application", "Remote Address", "Data Consumed (MB)"])
        self.layout.addWidget(self.table_widget)

        # Add checkbox to control "Always on top" behavior
        self.always_on_top_checkbox = QCheckBox("Keep window always on top")
        self.always_on_top_checkbox.setChecked(True)  # Default to checked
        self.always_on_top_checkbox.stateChanged.connect(self.toggle_always_on_top)
        self.layout.addWidget(self.always_on_top_checkbox)

        # Add exit button
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        self.layout.addWidget(self.exit_button, alignment=Qt.AlignCenter)

        # Initialize timer for periodic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data_usage)
        self.timer.start(1000)  # Update every second

        # Initialize notification flag
        self.notification_sent = False

        self.update_data_usage()

    def toggle_always_on_top(self, state):
        if state == Qt.Checked:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(Qt.Widget)
            self.show()

    def update_data_usage(self):
        # Get current data usage
        data_usage = self.get_data_usage()
        self.data_usage_label.setText(f"Data Usage: {data_usage} MB")

        # Check if data usage exceeds limit
        if not self.notification_sent:
            limit = self.get_limit()
            if data_usage >= limit:
                self.send_notification()
                self.notification_sent = True

        # Update the table with app data
        self.update_app_list()

    def get_data_usage(self):
        net_io = psutil.net_io_counters()
        total_bytes = net_io.bytes_recv + net_io.bytes_sent
        total_mb = total_bytes / (1024 * 1024)
        return round(total_mb, 2)

    def get_limit(self):
        limit_str = self.limit_input.text()
        try:
            limit = float(limit_str)
            return limit
        except ValueError:
            return float('inf')  # Default to infinity if invalid input

    def update_app_list(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)
        connections = psutil.net_connections()
        app_data = {}
        
        for conn in connections:
            if conn.pid and conn.raddr:
                try:
                    process = psutil.Process(conn.pid)
                    app_name = process.name()
                    ip_address = conn.raddr.ip if conn.raddr else "N/A"
                    
                    # Check if the app is already in app_data, and update the count
                    if app_name in app_data:
                        count, existing_ip = app_data[app_name]
                        app_data[app_name] = (count + 1, ip_address)  # Increment count, keep or update IP
                    else:
                        app_data[app_name] = (1, ip_address)  # Initialize with count 1 and IP
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

        # Populate the table
        for app_name, (count, ip_address) in app_data.items():
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(app_name))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(ip_address))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(f"{count} Connections"))

        self.table_widget.resizeColumnsToContents()

    def send_notification(self):
        notification_title = "Network Usage Alert"
        notification_message = "Your network data consumption has reached the limit!"
        notification.notify(title=notification_title, message=notification_message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkMonitorWindow()
    window.show()
    sys.exit(app.exec_())
