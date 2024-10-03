from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from fuzzywuzzy import fuzz

# Define program information (replace with actual data)
programs = {
    "Computer Science": ["BSc", "MSc"],
    "Mechanical Engineering": ["BEng", "MEng"]
}

# Define financial aid options (replace with actual data)
financial_aid = ["Scholarships", "Grants", "Work-Study"]


class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Student Registration Assistant")

        # Layout
        layout = QVBoxLayout(self)

        # Greeting message
        self.greeting_label = QLabel("Hi there! I'm your friendly registration assistant.")
        layout.addWidget(self.greeting_label)

        # Input field
        self.user_input = QLineEdit()
        self.user_input.returnPressed.connect(self.handle_user_query)
        layout.addWidget(self.user_input)

        # Send button (optional)
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_user_query)
        layout.addWidget(self.send_button)

        # Chat history
        self.chat_history = QLabel("")
        layout.addWidget(self.chat_history)

        self.setLayout(layout)
        self.show()

    def handle_user_query(self):
        user_query = self.user_input.text().strip()
        self.user_input.clear()

        # Update chat history
        self.chat_history.setText(self.chat_history.text() + f"\nYou: {user_query}")

        # Process user query
        response = self.process_query(user_query)
        self.chat_history.setText(self.chat_history.text() + f"\nAssistant: {response}")

    def process_query(self, query):
        """Analyzes user query and provides a response."""
        if "program" in query.lower() or "eligibility" in query.lower():
            program_name = query.split()[1]  # Extract program name after "program"
            return get_program_info(program_name)
        elif "financial aid" in query.lower() or "fees" in query.lower():
            topic = query.split()[1]  # Extract topic after "financial aid" or "fees"
            return get_financial_aid_info(topic)
        else:
            return (
                "I'm still under development, but I'm happy to answer any questions you have about registration. Try asking in a different way, or visit our website for detailed information."
            )


def get_program_info(program_name):
    """Provides information about a program based on user input."""
    # Use fuzzy matching to handle slight variations in program names
    best_match, score = "", 0
    for program, degrees in programs.items():
        match_score = fuzz.ratio(program_name.lower(), program.lower())
        if match_score > 60:  # Adjust threshold for acceptable match
            best_match = program
            score = match_score
    if score > 60:
        return f"The {best_match} program offers degrees in {', '.join(degrees)}."
    else:
        return f"Sorry, I couldn't find a program named '{program_name}'. "


def get_financial_aid_info(topic):
    """Provides information about financial aid based on user input."""
    if topic.lower() in [f.lower() for f in financial_aid]:
        return f"Yes, we offer {topic} as a financial aid option.  For more information, please visit our financial aid website."
    else:
        return f"I'm not sure about '{topic}', but we offer various financial aid options. Visit our website for details."


if __name__ == "__main__":
    app = QApplication([])
    chat_window = ChatWidget()
    app.exec_()
