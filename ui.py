import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import auth
import travel
import match_users as match
import chat

class TravelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Travel App")
        self.geometry("400x300")
        self.current_user = None
        self.users = auth.load_users()
        self.activities = travel.load_activities()
        self.setup_ui()

    def setup_ui(self):
        self.frames = {}

        for F in (LoginPage, MainPage, ExplorePage, MatchPage, ChatPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Welcome to the Travel App!")
        self.label.pack(pady=10)

        self.register_button = ttk.Button(self, text="Register", command=self.register)
        self.register_button.pack(pady=5)

        self.login_button = ttk.Button(self, text="Login", command=self.login)
        self.login_button.pack(pady=5)

    def register(self):
        def on_register():
            username = entry_username.get()
            password = entry_password.get()
            if username and password:
                auth.register_user(self.controller.users, username, password)
                messagebox.showinfo("Success", f"User {username} registered successfully!")
                register_window.destroy()
            else:
                messagebox.showwarning("Error", "Please enter both username and password")

        register_window = tk.Toplevel(self)
        register_window.title("Register")
        ttk.Label(register_window, text="Username:").pack()
        entry_username = ttk.Entry(register_window)
        entry_username.pack()
        ttk.Label(register_window, text="Password:").pack()
        entry_password = ttk.Entry(register_window, show="*")
        entry_password.pack()
        ttk.Button(register_window, text="Register", command=on_register).pack(pady=5)

    def login(self):
        def on_login():
            username = entry_username.get()
            password = entry_password.get()
            logged_in_username = auth.login_user(self.controller.users, username, password)
            if logged_in_username:
                self.controller.current_user = logged_in_username
                messagebox.showinfo("Success", f"Welcome, {username}!")
                login_window.destroy()
                self.controller.show_frame("MainPage")
            else:
                messagebox.showwarning("Error", "Invalid username or password")

        login_window = tk.Toplevel(self)
        login_window.title("Login")
        ttk.Label(login_window, text="Username:").pack()
        entry_username = ttk.Entry(login_window)
        entry_username.pack()
        ttk.Label(login_window, text="Password:").pack()
        entry_password = ttk.Entry(login_window, show="*")
        entry_password.pack()
        ttk.Button(login_window, text="Login", command=on_login).pack(pady=5)


class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Welcome!", font=("Arial", 16))
        self.label.pack(pady=10)

        self.explore_button = ttk.Button(self, text="Explore Activities", command=lambda: self.controller.show_frame("ExplorePage"))
        self.explore_button.pack(pady=5)

        self.match_button = ttk.Button(self, text="Match with Others", command=lambda: self.controller.show_frame("MatchPage"))
        self.match_button.pack(pady=5)

        self.chats_button = ttk.Button(self, text="Chats", command=lambda: self.controller.show_frame("ChatPage"))
        self.chats_button.pack(pady=5)

        self.exit_button = ttk.Button(self, text="Exit", command=self.quit)
        self.exit_button.pack(pady=5)


class ExplorePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Explore Activities", font=("Arial", 16))
        self.label.pack(pady=10)

        self.location_entry = ttk.Entry(self)
        self.location_entry.pack(pady=5)

        self.swipe_button = ttk.Button(self, text="Swipe on Activities", command=self.swipe_activities)
        self.swipe_button.pack(pady=5)

        self.add_button = ttk.Button(self, text="Add New Activity", command=self.add_activity)
        self.add_button.pack(pady=5)

        self.back_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("MainPage"))
        self.back_button.pack(pady=5)

    def swipe_activities(self):
        location = self.location_entry.get()
        if location in self.controller.activities:
            travel.swipe_on_activities(self.controller.current_user, location, self.controller.activities[location])
        else:
            messagebox.showinfo("No activities", f"No activities found for {location}")

    def add_activity(self):
        location = self.location_entry.get()
        if location:
            travel.add_activity(location, self.controller.activities.get(location, []))
            messagebox.showinfo("Success", f"Added new activity for {location}")
        else:
            messagebox.showwarning("Error", "Please enter a location")


class MatchPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Match with Others", font=("Arial", 16))
        self.label.pack(pady=10)

        self.match_button = ttk.Button(self, text="Find Matches", command=self.find_matches)
        self.match_button.pack(pady=5)

        self.back_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("MainPage"))
        self.back_button.pack(pady=5)

    def find_matches(self):
        user_activities = match.load_user_activities()
        matched_users = match.match_users(self.controller.current_user, user_activities)
        if matched_users:
            match_str = "\n".join([f"{user} - common activities: {', '.join(common_activities)}"
                                   for user, common_activities in matched_users.items()])
            messagebox.showinfo("Matches", f"Matching users:\n{match_str}")
        else:
            messagebox.showinfo("No Matches", "No matches found")


class ChatPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Chats", font=("Arial", 16))
        self.label.pack(pady=10)

        self.chat_listbox = tk.Listbox(self)
        self.chat_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        self.view_button = ttk.Button(self, text="View Chat", command=self.view_chat)
        self.view_button.pack(pady=5)

        self.back_button = ttk.Button(self, text="Back", command=lambda: self.controller.show_frame("MainPage"))
        self.back_button.pack(pady=5)

        self.update_chat_list()

    def update_chat_list(self):
        self.chat_listbox.delete(0, tk.END)
        chat_files = chat.list_chats(self.controller.current_user)
        self.chat_files = chat_files
        for i, (filename, other_person) in enumerate(chat_files):
            self.chat_listbox.insert(tk.END, f"Chat with {other_person}")

    def view_chat(self):
        selection = self.chat_listbox.curselection()
        if selection:
            index = selection[0]
            filename, other_person = self.chat_files[index]
            chat.start_chat(self.controller.current_user, other_person)


if __name__ == "__main__":
    app = TravelApp()
    app.mainloop()
