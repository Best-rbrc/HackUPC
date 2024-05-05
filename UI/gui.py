from PyQt5.QtWidgets import (
    QVBoxLayout, QListWidget, QListWidgetItem, QTextEdit,
    QInputDialog, QLineEdit, QPushButton, QMessageBox,
    QLabel, QWidget, QApplication, QStackedWidget,
    QMainWindow, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import sys
import auth
import travel
import match_users as match
import chat
import os

# Custom button class with modern styling
class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Arial", 12))
        self.setStyleSheet("""
            QPushButton {
                background-color: #555555; /* Dark grey */
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #666666; /* Slightly lighter grey on hover */
            }
            QPushButton:pressed {
                background-color: #444444; /* Slightly darker grey when pressed */
            }
        """)

# Custom line edit class with modern styling
class ModernLineEdit(QLineEdit):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setFont(QFont("Arial", 12))
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #666666;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
        """)

# Custom label class with modern styling
class ModernLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Arial", 12))
        self.setStyleSheet("""
            QLabel {
                color: #000000; /* Black color */
                font-size: 16px;
            }
        """)

# Login page class
class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)

        # Add a logo
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap("image.jpg").scaledToWidth(400, Qt.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo)

        # Username input field
        self.username_input = ModernLineEdit("Username", self)
        self.layout.addWidget(self.username_input)

        # Password input field
        self.password_input = ModernLineEdit("Password", self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        # 2FA token input field
        self.token_input = ModernLineEdit("2FA Token", self)
        self.layout.addWidget(self.token_input)

        # Login button
        self.login_button = ModernButton("Login", self)
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        # Register button
        self.register_button = ModernButton("Register", self)
        self.register_button.clicked.connect(self.register)
        self.layout.addWidget(self.register_button)

        # Error label
        self.error_label = ModernLabel("", self)
        self.layout.addWidget(self.error_label)

    # Login function
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        token = self.token_input.text()
        users = auth.load_users()
        authenticated_username = auth.login_user(users, username, password, token)
        if authenticated_username:
            # If login is successful, show the main menu page
            self.parent.show_main_menu_page()
        else:
            # If login fails, display an error message
            self.error_label.setText("Invalid credentials or 2FA token")

    # Register function
    def register(self):
        self.parent.show_register_page()


# Registration page class
class RegisterPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)

        # Username input field
        self.username_input = ModernLineEdit("New Username", self)
        self.layout.addWidget(self.username_input)

        # Password input field
        self.password_input = ModernLineEdit("New Password", self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        # Register button
        self.register_button = ModernButton("Register", self)
        self.register_button.clicked.connect(self.register)
        self.layout.addWidget(self.register_button)

        # Back to login button
        self.back_button = ModernButton("Back to Login", self)
        self.back_button.clicked.connect(self.back)
        self.layout.addWidget(self.back_button)

        # Message label
        self.message_label = ModernLabel("", self)
        self.layout.addWidget(self.message_label)

    # Register function
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        users = auth.load_users()
        if username in users:
            # If the username already exists, display an error message
            self.message_label.setText("Username already exists.")
        else:
            # Otherwise, register the new user
            auth.register_user(users, username, password)
            self.message_label.setText(f"User {username} registered successfully.")
            self.parent.show_login_page()

    # Back to login function
    def back(self):
        self.parent.show_login_page()

# Main menu page class
class MainMenuPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)

        # Button to explore activities
        self.explore_button = ModernButton("Explore Activities", self)
        self.explore_button.clicked.connect(self.parent.show_explore_page)
        self.layout.addWidget(self.explore_button)

        # Button to match with others
        self.match_button = ModernButton("Match with Others", self)
        self.match_button.clicked.connect(self.parent.show_match_page)
        self.layout.addWidget(self.match_button)

        # Button to open chat
        self.chat_button = ModernButton("Chats", self)
        self.chat_button.clicked.connect(self.parent.show_chat_page)
        self.layout.addWidget(self.chat_button)

        # Exit button
        self.exit_button = ModernButton("Exit", self)
        self.exit_button.clicked.connect(sys.exit)
        self.layout.addWidget(self.exit_button)

# Explore page class
class ExplorePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)

        # Load available activities
        self.activities = travel.load_activities()
        self.location_activities = []
        self.current_index = 0
        self.liked_activities = []

        # Location input field
        self.location_input = ModernLineEdit("Enter location", self)
        self.layout.addWidget(self.location_input)

        # Load activities button
        self.load_button = ModernButton("Load Activities", self)
        self.load_button.clicked.connect(self.load_activities)
        self.layout.addWidget(self.load_button)

        # Add activity button
        self.add_button = ModernButton("Add Activity", self)
        self.add_button.clicked.connect(self.add_activity)
        self.layout.addWidget(self.add_button)

        # Activity label
        self.activity_label = ModernLabel("No activities loaded", self)
        self.layout.addWidget(self.activity_label)

        # Yes button
        self.yes_button = ModernButton("Yes", self)
        self.yes_button.clicked.connect(self.like_activity)
        self.layout.addWidget(self.yes_button)

        # No button
        self.no_button = ModernButton("No", self)
        self.no_button.clicked.connect(self.dislike_activity)
        self.layout.addWidget(self.no_button)

        # Back to menu button
        self.back_button = ModernButton("Back to Menu", self)
        self.back_button.clicked.connect(self.go_back_to_menu)
        self.layout.addWidget(self.back_button)

    # Load activities for a given location
    def load_activities(self):
        location = self.location_input.text().strip()
        if location in self.activities:
            # If activities exist for the given location, load them
            self.location_activities = self.activities[location]
            self.current_index = 0
            self.liked_activities = []
            self.update_activity_display()
        else:
            # If no activities found, display a message
            QMessageBox.information(self, "No Activities", f"No activities found for {location}")

    # Update the display to show the current activity
    def update_activity_display(self):
        if self.current_index < len(self.location_activities):
            # Show the next activity
            self.activity_label.setText(f"Do you like this activity: {self.location_activities[self.current_index]}?")
        else:
            if self.liked_activities:
                # If there are liked activities, save them and go back to menu
                username = self.parent.login_page.username_input.text()
                location = self.location_input.text().strip()
                travel.swipe_on_activities(username, location, self.liked_activities)
                QMessageBox.information(self, "Activities Liked", f"You liked the following activities:\n" +
                                        "\n".join(self.liked_activities))
            self.go_back_to_menu()

    # Like the current activity
    def like_activity(self):
        if self.current_index < len(self.location_activities):
            # Add to liked activities and move to next
            self.liked_activities.append(self.location_activities[self.current_index])
            self.current_index += 1
            self.update_activity_display()

    # Dislike the current activity
    def dislike_activity(self):
        if self.current_index < len(self.location_activities):
            # Move to next activity
            self.current_index += 1
            self.update_activity_display()

    # Add a new activity
    def add_activity(self):
        # Get the location for the new activity
        location, ok = QInputDialog.getText(self, "Add Activity", "Enter the name of the place:")
        if ok and location:
            # Get the name of the new activity
            activity_name, ok = QInputDialog.getText(self, "Add Activity", f"Enter the name of the activity for {location}:")
            if ok and activity_name:
                # If location does not exist, create it
                if location not in self.activities:
                    self.activities[location] = []
                # Add the new activity
                self.activities[location].append(activity_name)
                travel.add_activity(location, self.activities[location])
                QMessageBox.information(self, "Success", f"Added activity '{activity_name}' in '{location}' successfully.")
                self.update_activity_display()

    # Go back to the main menu
    def go_back_to_menu(self):
        self.parent.show_main_menu_page()


# Match page class
class MatchPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)

        # Find matches button
        self.match_button = ModernButton("Find Matches", self)
        self.match_button.clicked.connect(self.find_matches)
        self.layout.addWidget(self.match_button)

        # List of matched users
        self.match_list = QListWidget(self)
        self.layout.addWidget(self.match_list)

        # Start chat button
        self.chat_button = ModernButton("Start Chat", self)
        self.chat_button.clicked.connect(self.start_chat)
        self.layout.addWidget(self.chat_button)

        # Back to menu button
        self.back_button = ModernButton("Back to Menu", self)
        self.back_button.clicked.connect(self.parent.show_main_menu_page)
        self.layout.addWidget(self.back_button)

    # Find matching users based on common activities
    def find_matches(self):
        self.match_list.clear()
        username = self.parent.login_page.username_input.text()
        user_activities = match.load_user_activities()
        matched_users = match.match_users(username, user_activities)
        if matched_users:
            for user, activities in matched_users.items():
                QListWidgetItem(f"{user} - common activities: {', '.join(activities)}", self.match_list)
        else:
            QMessageBox.information(self, "Matches", "No matches found.")

    # Start a chat with the selected matched user
    def start_chat(self):
        selected_item = self.match_list.currentItem()
        if selected_item:
            username = self.parent.login_page.username_input.text()
            selected_user = selected_item.text().split(' - ')[0]
            chat_key = tuple(sorted([username, selected_user]))
            if chat_key not in self.parent.active_chats:
                # Create a new chat file if it doesn't exist
                filename = f"chat_{chat_key[0]}_{chat_key[1]}.txt"
                self.parent.active_chats[chat_key] = filename
            # Set up the chat page for the selected users
            self.parent.chat_page.set_up_chat(username, selected_user, self.parent.active_chats[chat_key])
            self.parent.show_chat_page()


# Chat page class
class ChatPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)

        # Label to show chat info
        self.chat_label = ModernLabel("No chat selected", self)
        self.layout.addWidget(self.chat_label)

        # List of available chats
        self.chat_list = QListWidget(self)
        self.chat_list.itemClicked.connect(self.open_chat)
        self.layout.addWidget(self.chat_list)

        # Display area for chat messages
        self.chat_text_edit = QTextEdit(self)
        self.chat_text_edit.setReadOnly(True)
        self.layout.addWidget(self.chat_text_edit)

        # Input field for new chat message
        self.chat_line_edit = ModernLineEdit("", self)
        self.layout.addWidget(self.chat_line_edit)

        # Send message button
        self.send_button = ModernButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        # Back to matches button
        self.back_button = ModernButton("Back to Matches", self)
        self.back_button.clicked.connect(self.parent.show_match_page)
        self.layout.addWidget(self.back_button)

    # Set up the chat between two users
    def set_up_chat(self, user1, user2, filename):
        self.filename = filename
        self.other_user = user2
        self.chat_label.setText(f"Chat between {user1} and {user2}")
        self.load_chat_history()
        self.update_chat_list()

    # Load the chat history from file
    def load_chat_history(self):
        if self.filename:
            try:
                with open(self.filename, 'r') as file:
                    self.chat_text_edit.setPlainText(file.read())
            except FileNotFoundError:
                with open(self.filename, 'w') as file:
                    pass  # Create the file if it doesn't exist

    # Send a new message
    def send_message(self):
        message = self.chat_line_edit.text()
        if message and self.filename:
            with open(self.filename, 'a') as file:
                file.write(f"{self.parent.login_page.username_input.text()}: {message}\n")
            self.chat_text_edit.append(f"{self.parent.login_page.username_input.text()}: {message}")
            self.chat_line_edit.clear()

    # Update the list of available chats
    def update_chat_list(self):
        self.chat_list.clear()
        for chat_key, filename in self.parent.active_chats.items():
            other_user = chat_key[1] if chat_key[0] == self.parent.login_page.username_input.text() else chat_key[0]
            QListWidgetItem(f"Chat with {other_user}", self.chat_list)

    # Open a chat when selected
    def open_chat(self, item):
        other_user = item.text().split(" ")[2]
        chat_key = tuple(sorted([self.parent.login_page.username_input.text(), other_user]))
        filename = self.parent.active_chats[chat_key]
        self.set_up_chat(self.parent.login_page.username_input.text(), other_user, filename)


# Main window class
class TravelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel App")
        self.setGeometry(100, 100, 800, 600)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
        """)

        # Dictionary to hold active chats
        self.active_chats = {}

        # Create pages for the app
        self.login_page = LoginPage(self)
        self.register_page = RegisterPage(self)
        self.main_menu_page = MainMenuPage(self)
        self.explore_page = ExplorePage(self)
        self.match_page = MatchPage(self)
        self.chat_page = ChatPage(self)

        # Add pages to the stacked widget
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.register_page)
        self.stack.addWidget(self.main_menu_page)
        self.stack.addWidget(self.explore_page)
        self.stack.addWidget(self.match_page)
        self.stack.addWidget(self.chat_page)

        # Start with the login page
        self.show_login_page()

    # Show the login page
    def show_login_page(self):
        self.stack.setCurrentWidget(self.login_page)

    # Show the registration page
    def show_register_page(self):
        self.stack.setCurrentWidget(self.register_page)

    # Show the main menu page
    def show_main_menu_page(self):
        self.stack.setCurrentWidget(self.main_menu_page)

    # Show the explore page
    def show_explore_page(self):
        self.stack.setCurrentWidget(self.explore_page)

    # Show the match page
    def show_match_page(self):
        self.stack.setCurrentWidget(self.match_page)

    # Show the chat page
    def show_chat_page(self):
        self.chat_page.update_chat_list()
        self.stack.setCurrentWidget(self.chat_page)

# Main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TravelApp()
    window.show()
    sys.exit(app.exec_())
