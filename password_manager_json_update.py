# save passwords in json file (data.json) and better UI

from tkinter import *
from tkinter import messagebox
import random
import json
import pyperclip  # use to copy something

FONT = ("times new roman", 14)
CANVAS_BACKGROUND = "#186f65"
BUTTON_COLOR = "#c1d8c3"


# ----------------- PASSWORD GENERATOR ---------------------

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


# ------------------- SAVE PASSWORD --------------------

def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # create a dictionary
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if not website or not email or not password or email == "yourmail@gmail.com":
        messagebox.showerror(title="OOPS", message="Please do not leave any field empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:" + "\n" +
                                                              f"\nEmail: {email}" + f"\nPassword:  {password}" + "\n" +
                                                              "\nIs is ok to save?")
        if is_ok:
            try:
                # open json file in read mode and update data with new data
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)

            except (FileNotFoundError, json.decoder.JSONDecodeError):
                # open json file in write mode and add updated data
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                if website in data:
                    is_yes = messagebox.askyesno(title=f"⚠️{website}",
                                                 message=f"website '{website}' already exist in data.\n\n"
                                                         f"Details:\nemail: {data[website]['email']}\npassword: {data[website]['password']}\n\n"
                                                         f"Do you want to overwrite the data?")
                    if is_yes:
                        # update json data
                        data.update(new_data)
                        # write updated data
                        with open("data.json", "w") as data_file:
                            json.dump(data, data_file, indent=4)
                else:
                    # update json data
                    data.update(new_data)
                    # write updated data
                    with open("data.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                email_entry.delete(0, END)
                website_entry.focus()  # place cursor on this entry label
                email_entry.insert(0, "yourmail@gmail.com")
                email_entry.config(fg="gray")


# --------------------- search from data --------------------

def search_data():
    try:
        with open("data.json", "r") as data_file:
            search = json.load(data_file)
            website_name = website_entry.get()
            website_search = search[website_name]
    except FileNotFoundError:
        messagebox.showerror(title="OOPS", message=" Data file does not exist.")

    except KeyError:  # when user type a website which does not exist in json file and hit search button
        messagebox.showerror(title="OOPS", message=f"Details of {website_name} website does not exist.")

    except json.decoder.JSONDecodeError:  # if json file exist but has no data inside and user hit search button
        messagebox.showwarning(title="OOPS", message="File has no data")
    else:
        messagebox.showinfo(title=website_name, message=f"website data found\n\nemail:  {website_search['email']}"
                                                        f"\npassword:  {website_search['password']}")
        if website_name in search:
            is_yes = messagebox.askyesno(title=f"⚠️{website_name}",
                                         message=f"website '{website_name}' already exist in data. Do you want to overwrite the data?")
            if not is_yes:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                email_entry.delete(0, END)
                website_entry.focus()  # place cursor on this entry label
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


# -------------------- UI SETUP --------------------

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)
window.resizable(0, 0)

canvas = Canvas(width=200, height=200, bg=CANVAS_BACKGROUND, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1, pady=20)

# label
website_label = Label(pady=5, text="website:", font=FONT)
website_label.grid(row=1, column=0)  # sticky="e"

email_label = Label(pady=5, text="email id/username:", font=FONT)
email_label.grid(row=2, column=0)

password_label = Label(pady=5, text="password:", font=FONT)
password_label.grid(row=3, column=0)  # sticky="e"

# entry
website_entry = Entry(width=34, font=FONT)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2, sticky="w")

email_entry = Entry(width=50, font=FONT, fg="gray")
email_entry.insert(0, "yourmail@gmail.com")  # insert a placeholder
email_entry.bind("<FocusIn>", on_focus_in)
email_entry.bind("<FocusOut>", on_focus_out)
email_entry.grid(row=2, column=1, columnspan=2)

password_entry = Entry(width=34, font=FONT)
password_entry.grid(row=3, column=1, sticky="w")

# buttons
password_generate_button = Button(text="generate password", bg=BUTTON_COLOR, font=("times new roman", 13,),
                                  command=generate_password)
password_generate_button.grid(row=3, column=2)

add_button = Button(text="add", width=50, bg=BUTTON_COLOR, font=("times new roman", 13,), command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="search", width=14, bg=BUTTON_COLOR, font=("times new roman", 13,), command=search_data)
search_button.grid(row=1, column=2)

window.mainloop()
