# save passwords in text file (data.txt)

from tkinter import *
from tkinter import messagebox
import random
import pyperclip  # use to copy something

FONT = ("times new roman", 14)


# ----------------------- PASSWORD GENERATOR ------------------------
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
               'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(5, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    [password_list.append(random.choice(letters)) for _ in range(nr_letters)]
    [password_list.append(random.choice(symbols)) for _ in range(nr_symbols)]
    [password_list.append(random.choice(numbers)) for _ in range(nr_numbers)]

    # print(f"{''.join(password_list)}")

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char

    password_entry.delete(0, END)  # clears the existing content in the password_entry field
    password_entry.insert(END, password)  # After clearing the entry field, this line inserts new password into it
    pyperclip.copy(password)
    # print(f"Your password is: {password}")


# ----------------------- SAVE PASSWORD -------------------------
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if not website or not password or not email or email == "yourmail@gmail.com":  # if any field empty
        messagebox.showerror(title="OOPS", message="Please don't leave any field empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\n\nEmail: {email}"
                                                              f"\nPassword: {password}\n\nIs is ok to save?")
        if is_ok:
            with open("data.txt", "a") as data:
                data.write(f"website: {website} | email: {email} | password: {password}\n")

            website_entry.delete(0, END)
            password_entry.delete(0, END)
            email_entry.delete(0, END)
            website_entry.focus()   # place cursor on this entry label
            email_entry.insert(0, "yourmail@gmail.com")
            email_entry.config(fg="gray")


# ------------------- working with placeholder --------------------

def on_focus_in(event):
    if email_entry.get() == "yourmail@gmail.com":
        email_entry.delete(0, END)
        email_entry.config(fg="black")  # Change text color when user types


def on_focus_out(event):
    if not email_entry.get():  # If the entry is empty, restore placeholder
        email_entry.insert(0, "yourmail@gmail.com")
        email_entry.config(fg="gray")  # Make placeholder text gray


# ----------------------- UI SETUP ------------------------

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200, bg='sky blue', highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image((100, 100), image=logo_img)
canvas.grid(row=0, column=1, pady=20)

# ------- label ----------
website_label = Label(pady=5, text="website:", font=FONT)
website_label.grid(row=1, column=0)  # sticky="e"

email_label = Label(pady=5, text="email id/username:", font=FONT)
email_label.grid(row=2, column=0)

password_label = Label(pady=5, text="password:", font=FONT)
password_label.grid(row=3, column=0)  # sticky="e"

# --------- entry ----------
website_entry = Entry(width=50, font=FONT)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2, )

email_entry = Entry(width=50, font=FONT, fg="gray")
email_entry.insert(0, "yourmail@gmail.com")  # insert a placeholder
email_entry.bind("<FocusIn>", on_focus_in)
email_entry.bind("<FocusOut>", on_focus_out)
email_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=34, font=FONT)
password_entry.grid(row=3, column=1, sticky="w")

# ---------- buttons -----------
password_generate_button = Button(text="generate password", bg="#a1ccd1", font=("times new roman", 13,),
                                  command=generate_password)
password_generate_button.grid(row=3, column=2)

add_button = Button(text="add", width=50, bg="#a1ccd1", font=("times new roman", 13,), command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
