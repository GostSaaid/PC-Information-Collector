import tkinter as tk
from tkinter import messagebox

def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

screen = tk.Tk()
screen.geometry("400x400")
screen.title("Login Page")
screen.config(background="#023047")

title_label = tk.Label(
    text="Login Best Chat",
    font=("Arial", 20, "bold"),
    bg="#023047",
    fg="#fb8500"
)
title_label.pack(pady=10)

username_label = tk.Label(
    text="Username",
    font=("Arial", 14),
    bg="#023047",
    fg="#8ecae6"
)
username_label.pack(pady=5)

entry_username = tk.Entry(
    font=("Arial", 14),
    bg="white",
    fg="black"
)
entry_username.pack(pady=5)

password_label = tk.Label(
    text="Password",
    font=("Arial", 14),
    bg="#023047",
    fg="#8ecae6"
)
password_label.pack(pady=5)

entry_password = tk.Entry(
    font=("Arial", 14),
    bg="white",
    fg="black",
    show="*"  
)
entry_password.pack(pady=5)

login_button = tk.Button(
    text="Login",
    font=("Arial", 14),
    bg="#219ebc",
    fg="#f1faee",
    command=login
)
login_button.pack(pady=20)

screen.mainloop()