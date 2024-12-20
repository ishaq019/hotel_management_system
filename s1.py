import json
import os
import tkinter as tk
from tkinter import messagebox

# File paths

ROOM_FILE = 'C:/syed/rooms.txt'
BOOKING_FILE = 'C:/syed/hotel_bookings.txt'
EMPLOYEE_FILE = 'C:/syed/employees.txt'
USER_FILE = 'C:/syed/users.txt'

# Function to load data from a text file
def load_data(file_path):
    users = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                username, password, age, gender = line.strip().split(',')
                users.append({'username': username, 'password': password, 'age': age, 'gender': gender})
    except FileNotFoundError:
        pass  # If the file doesn't exist, return an empty list
    return users


def view_employees():
    employees = load_data(EMPLOYEE_FILE)  # Load employee data from the file
    if not employees:
        messagebox.showinfo("Employee Information", "No employees registered.")
        return

    # Prepare the table header and rows with consistent spacing
    header = f"{'Employee ID':<15} {'Name':<20} "
    separator = '-' * len(header)
    
    # Create rows with proper alignment
    rows = [f"{emp['employee_id']:<15} {emp['name']:<20} " for emp in employees]
    
    # Combine header, separator, and rows into a single string
    table = f"{header}\n{separator}\n" + "\n".join(rows)

    # Show the table in a message box
    messagebox.showinfo("Employee Information", table)

# Function to save data to a text file
def save_data(file_path, data):
    with open(file_path, 'w') as file:
        for user in data:
            file.write(f"{user['username']},{user['password']},{user['age']},{user['gender']}\n")


# Function to view user information in the admin interface
def view_users():
    users = load_data(USER_FILE)
    if not users:
        messagebox.showinfo("User  Information", "No users registered.")
        return

    # Prepare the table header and rows with consistent spacing
    header = f"{'Username':<20} {'Age':<5} {'Gender':<10}"
    separator = '-' * len(header)
    
    # Create rows with proper alignment
    rows = [f"{user['username']:<20} {user['age']:<5} {user['gender']:<10}" for user in users]
    
    # Combine header, separator, and rows into a single string
    table = f"{header}\n{separator}\n" + "\n".join(rows)

    # Show the table in a message box
    messagebox.showinfo("User  Information", table)

# Create the main window
root = tk.Tk()
root.title("Hotel Management System")
root.geometry("1920x1080")  # You can adjust this size as needed

# Show frame
def show_frame(frame):
    frame.tkraise()

# Initialize files if they don't exist
def initialize_files():
    for file in [USER_FILE, ROOM_FILE, BOOKING_FILE, EMPLOYEE_FILE]:
        if not os.path.exists(file):
            save_data(file, [])


# Create frames
frame_login = tk.Frame(root, bg="#735DA5")
frame_register = tk.Frame(root, bg="#735DA5")
frame_admin = tk.Frame(root, bg="#00246B")

for frame in (frame_login, frame_register, frame_admin):
    frame.grid(row=0, column=0, sticky='nsew')


# Helper functions for file operations
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Bubble Sort Function
def bubble_sort(rooms):
    n = len(rooms)
    for i in range(n):
        for j in range(0, n-i-1):
            if rooms[j]['room_id'] > rooms[j+1]['room_id']:
                rooms[j], rooms[j+1] = rooms[j+1], rooms[j]


# Quick Sort Function
def quick_sort(rooms):
    if len(rooms) <= 1:
        return rooms
    pivot = rooms[len(rooms) // 2]['room_id']
    left = [x for x in rooms if x['room_id'] < pivot]
    middle = [x for x in rooms if x['room_id'] == pivot]
    right = [x for x in rooms if x['room_id'] > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Initialize files if they don't exist
def initialize_files():
    for file in [USER_FILE, ROOM_FILE, BOOKING_FILE, EMPLOYEE_FILE]:
        if not os.path.exists(file):
            save_data(file, [])

# Show frame
def show_frame(frame):
    frame.tkraise()

# Registration function
def register_user():
    username = entry_username_reg.get()
    password = entry_password_reg.get()
    age = entry_age.get()
    gender = gender_var.get()  # Get the selected gender

    users = load_data(USER_FILE)

    if any(user['username'] == username for user in users):
        messagebox.showerror("Error", "Username already exists.")
        return
    
    # Validate age input
    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a number.")
        return

    users.append({'username': username, 'password': password, 'age': age, 'gender': gender})
    save_data(USER_FILE, users)
    messagebox.showinfo("Success", "Registration successful!")
    show_frame(frame_login)

# Occupancy report using linear search
def view_occupancy_report():
    rooms = load_data(ROOM_FILE)  # Load room data from the file
    total_rooms = len(rooms)  # Total number of rooms
    booked_rooms = 0  # Initialize booked rooms counter

    # Linear search to count booked rooms
    for room in rooms:
        if not room['is_available']:  # Check if the room is not available
            booked_rooms += 1  # Increment booked rooms counter

    available_rooms = total_rooms - booked_rooms  # Calculate available rooms
    report = f"Total Rooms: {total_rooms}\nBooked Rooms: {booked_rooms}\nAvailable Rooms: {available_rooms}"
    messagebox.showinfo("Occupancy Report", report)  # Show occupancy report in a message box

def view_rooms():
    rooms = load_data(ROOM_FILE)  # Load room data from the file
    quick_sort(rooms)
    if not rooms:
        messagebox.showinfo("Room Information", "No rooms available.")
        return

    # Prepare the table header and rows with consistent spacing
    header = f"{'Room Number':<15} {'Type':<10} {'Price':<10} {'Status':<10}"
    separator = '-' * len(header)
    
    # Create rows with proper alignment
    rows = [f"{room['room_id']:<15} {room['room_type']:<10} {room['price']:<10} {'Available' if room['is_available'] else 'Booked':<10}" for room in rooms]
    
    # Combine header, separator, and rows into a single string
    table = f"{header}\n{separator}\n" + "\n".join(rows)

    # Show the table in a message box
    messagebox.showinfo("Room Information", table)

# Login function
def login():
    username = entry_username.get()
    password = entry_password.get()
    users = load_data(USER_FILE)

    for user in users:
        if user['username'] == username and user['password'] == password:
            messagebox.showinfo("Success", "Login successful!")
            if username == "admin":
                show_frame(frame_admin)
            else:
                show_frame(frame_user)
                label_user_welcome.config(text=f"Welcome, {username}")
            return
    
    messagebox.showerror("Error", "Invalid username or password.")



# Create frames for different functionalities
frame_login = tk.Frame(root, bg="#735DA5")
frame_register = tk.Frame(root,bg="dark gray")
frame_admin = tk.Frame(root, bg="#00246B")
frame_user = tk.Frame(root, bg="#735DA5")
frame_add_room = tk.Frame(root, bg="#735DA5")
frame_delete_room = tk.Frame(root, bg="#735DA5")
frame_book_room = tk.Frame(root, bg="#735DA5")
frame_cancel_booking = tk.Frame(root, bg="#735DA5")
frame_view_bookings = tk.Frame(root, bg="#735DA5")
frame_add_employee = tk.Frame(root, bg="#735DA5")

for frame in (frame_login, frame_register, frame_admin, frame_user, frame_add_room, frame_delete_room, frame_book_room, frame_cancel_booking, frame_view_bookings, frame_add_employee):
    frame.grid(row=0, column=0, sticky='news')

# Load the background image for the login frame
background_image_login = tk.PhotoImage(file='C:/syed/login.png')  # Update the path

# Configure the grid layout
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create frames
frame_login = tk.Frame(root, bg="dark gray")
frame_login.grid(row=0, column=0, sticky='nsew')


# Set the image to fill the frame
tk.Label(frame_login, image=background_image_login).place(relwidth=1, relheight=1)




# Adjusting the login frame
tk.Label(frame_login, text="WELCOME TO THE HOTEL",fg="white",bg="dark gray", font=("Copperplate Gothic Bold", 48)).pack(pady=(40, 20))

tk.Label(frame_login, text="Username:", bg="dark gray",fg="white", font=("Helvetica", 16)).pack(pady=(50, 30))  # Added bottom padding
entry_username = tk.Entry(frame_login, font=("Helvetica", 16))
entry_username.pack(pady=(0, 20), padx=20, fill='y')  # Increased bottom padding

tk.Label(frame_login, text="Password:", bg="dark gray",fg="white", font=("Helvetica", 16)).pack(pady=(10, 30))  # Added bottom padding
entry_password = tk.Entry(frame_login, show='*', font=("Helvetica", 16))
entry_password.pack(pady=(0, 20), padx=20, fill='y')  # Increased bottom padding

tk.Button(frame_login, text="Login", command=login,bg="dark gray",fg="white", font=("Helvetica", 16)).pack(pady=(50, 30))
tk.Button(frame_login, text="Don't have an Account? Register Now", command=lambda: show_frame(frame_register),bg="dark gray",fg="white", font=("Helvetica", 16),width=30, height=1).pack(pady=(5, 20))



# Register Frame
frame_register = tk.Frame(root)  # Keep the frame background for compatibility
frame_register.grid(row=0, column=0, sticky='nsew')

# Load the background image for the registration frame
background_image3 = tk.PhotoImage(file='C:/syed/login.png')  # Update the path
tk.Label(frame_register, image=background_image3).place(relwidth=1, relheight=1)  # Set the image to fill the frame

# Register Frame
tk.Label(frame_register, text="REGISTRATION",bg="dark gray",fg="white", font=("Copperplate Gothic Bold", 39), width=20, height=1 ).pack(pady=40)

# Username Entry
frame_username = tk.Frame(frame_register, width=30, height=2)
frame_username.pack(pady=(30, 20))
tk.Label(frame_username, text="Username:",width=15,height=1 ,bg="dark gray",fg="white", font=("Helvetica", 16)).pack(side=tk.LEFT)
entry_username_reg = tk.Entry(frame_username, font=("Helvetica", 16))
entry_username_reg.pack(side=tk.LEFT, padx=10)

# Password Entry
frame_password = tk.Frame(frame_register,width=30, height=2)
frame_password.pack(pady=(10, 20))
tk.Label(frame_password, text="Password:", width=15,height=1,bg="dark gray",fg="white", font=("Helvetica", 16)).pack(side=tk.LEFT)
entry_password_reg = tk.Entry(frame_password, show='*', font=("Helvetica", 16))
entry_password_reg.pack(side=tk.LEFT, padx=10)

# Age Entry
frame_age = tk.Frame(frame_register, width=30, height=2)
frame_age.pack(pady=(10, 20))
tk.Label(frame_age, text="Age:", width=15,height=1,bg="dark gray",fg="white", font=("Helvetica", 16)).pack(side=tk.LEFT)
entry_age = tk.Entry(frame_age, font=("Helvetica", 16))
entry_age.pack(side=tk.LEFT, padx=10)

# Gender Selection
frame_gender = tk.Frame(frame_register, width=30, height=2)
frame_gender.pack(pady=(10, 20))
tk.Label(frame_gender, text="Gender:", width=20,height=1,bg="dark gray",fg="white", font=("Helvetica", 16)).pack(side=tk.LEFT)

gender_var = tk.StringVar(value="Male")  # Default value
tk.Radiobutton(frame_gender, text="Male", variable=gender_var, value="Male", bg="dark gray", font=("Helvetica", 16)).pack(side=tk.LEFT, padx=5)
tk.Radiobutton(frame_gender, text="Female", variable=gender_var, value="Female", bg="dark gray", font=("Helvetica", 16)).pack(side=tk.LEFT, padx=5)

# Register Button
tk.Button(frame_register, text="Register", command=register_user,bg="dark gray",fg="white", font=("Helvetica", 16), width=20, height=2).pack(pady=(30, 10))
tk.Button(frame_register, text="Already have an Account? Login Now", command=lambda: show_frame(frame_login),bg="dark gray",fg="white", font=("Helvetica", 16), width=30, height=2).pack(pady=(15, 20))

# Create frames for different sections
frame_admin = tk.Frame(root)
frame_admin.grid(row=0, column=0, sticky='nsew')

# Load the background image for the admin menu frame
background_image_admin = tk.PhotoImage(file='C:/syed/admin.png')  # Update the path

# Create a canvas to hold the background image
canvas_admin = tk.Canvas(frame_admin, width=400, height=400)  # Adjust size as needed
canvas_admin.pack(fill="both", expand=True)

# Create a label with the background image
label_background_admin = tk.Label(canvas_admin, image=background_image_admin)
label_background_admin.place(relwidth=1, relheight=1)  # Set the image to fill the canvas

# Admin Menu Title
tk.Label(canvas_admin, text="ADMIN MENU", font=("Copperplate Gothic Bold", 24), bg="black",fg="white",width=35, height=2).pack(pady=50)

# Admin Menu Buttons
tk.Button(canvas_admin, text="Add Room", command=lambda: show_frame(frame_add_room), font=("Helvetica", 16), bg="dark gray",fg="white",  width=25, height=1).pack(pady=15)
tk.Button(canvas_admin, text="View Rooms", command=view_rooms, font=("Helvetica", 16), bg="dark gray",fg="white", width=25, height=1).pack(pady=15)
tk.Button(canvas_admin, text="View Occupancy Report", command=view_occupancy_report, font=("Helvetica", 16), bg="dark gray",fg="white",  width=25, height=1).pack(pady=15)
tk.Button(canvas_admin, text="View Users", command=view_users, font=("Helvetica", 16), bg="dark gray",fg="white",  width=25, height=1).pack(pady=15)
tk.Button(canvas_admin, text="View Employees", command=view_employees, font=("Helvetica", 16), bg="dark gray",fg="white",  width=25, height=1).pack(pady=15)  # New button to view employees
tk.Button(canvas_admin, text="Add Employee", command=lambda: show_frame(frame_add_employee), font=("Helvetica", 16), bg="dark gray",fg="white",  width=25, height=1).pack(pady=15)
tk.Button(canvas_admin, text="Delete Room", command=lambda: show_frame(frame_delete_room), font=("Helvetica", 16), bg="dark gray",fg="white",  width=25, height=1).pack(pady=15)
tk.Button(canvas_admin, text="Logout", command=lambda: show_frame(frame_login), font=("Helvetica", 16), bg="dark gray",fg="white",  width=25, height=1).pack(pady=15)


# User Menu Frame
background_image_user = tk.PhotoImage(file='C:/syed/user.png')  # Update with your image path
frame_user = tk.Frame(root)
# User Menu Frame
frame_user.grid(row=0, column=0, sticky='nsew')
tk.Label(frame_user, image=background_image_user).place(relwidth=1, relheight=1)  # Set the image to fill the frame

label_user_welcome = tk.Label(frame_user, text="", font=("Copperplate Gothic Bold", 32), bg="light gray",fg="white", width=28, height=1)
label_user_welcome.pack(pady=40)
tk.Button(frame_user, text="View Rooms", command=view_rooms, font=("Helvetica", 16), bg="#87CEEB", width=25, height=1).pack(pady=25)
tk.Button(frame_user, text="Book Room", command=lambda: show_frame(frame_book_room),font=("Helvetica", 16), bg="#87CEEB", width=25, height=1).pack(pady=25)
tk.Button(frame_user, text="View My Bookings", command=lambda: view_bookings(entry_username.get()),font=("Helvetica", 16), bg="#87CEEB", width=25, height=1).pack(pady=25)
tk.Button(frame_user, text="Cancel Booking", command=lambda: show_frame(frame_cancel_booking),font=("Helvetica", 16), bg="#87CEEB", width=25, height=1).pack(pady=25)
tk.Button(frame_user, text="Logout", command=lambda: show_frame(frame_login),font=("Helvetica", 16), bg="#87CEEB", width=25, height=1).pack(pady=25)

# Add Room Frame
# Load the background image for the registration frame
background_image1 = tk.PhotoImage(file='C:/syed/admin.png')  # Update the path
tk.Label(frame_add_room, image=background_image1).place(relwidth=1, relheight=1)  # Set the image to fill the frame


tk.Label(frame_add_room, text="Add Room", font=("Copperplate Gothic Bold", 32), bg="dark gray",fg="white", width=25, height=2).pack(pady=50)
tk.Label(frame_add_room, text="Room ID:", font=("Helvetica", 18), bg="dark gray",fg="white", width=25, height=1).pack(pady=20)
entry_room_id = tk.Entry(frame_add_room)
entry_room_id.pack()
tk.Label(frame_add_room, text="Room Type:", font=("Helvetica", 18),bg="dark gray",fg="white", width=25, height=1).pack(pady=20)
entry_room_type = tk.Entry(frame_add_room)
entry_room_type.pack()
tk.Label(frame_add_room, text="Price:", font=("Helvetica", 18),bg="dark gray",fg="white", width=25, height=1).pack(pady=20)
entry_price = tk.Entry(frame_add_room)
entry_price.pack()
tk.Button(frame_add_room, text="Add Room", font=("Helvetica", 18), command=lambda: add_room(entry_room_id.get(), entry_room_type.get(), entry_price.get()),bg="dark gray",fg="white", width=25, height=1).pack(pady=20)
tk.Button(frame_add_room, text="Back to Admin Menu", font=("Helvetica", 18), command=lambda: show_frame(frame_admin),bg="dark gray",fg="white", width=25, height=1).pack(pady=20)

# Function to add room
def add_room(room_id, room_type, price):
    rooms = load_data(ROOM_FILE)
    if any(room['room_id'] == room_id for room in rooms):
        messagebox.showerror("Error", f"Room ID {room_id} already exists.")
        return
    rooms.append({'room_id': room_id, 'room_type': room_type, 'price': price, 'is_available': True})
    bubble_sort(rooms)
    save_data(ROOM_FILE, rooms)
    messagebox.showinfo("Success", f"Room {room_id} added successfully!")
    show_frame(frame_admin)

# View Rooms Function
def view_rooms():
    rooms = load_data(ROOM_FILE)
    quick_sort(rooms)
    if rooms:
        rooms_str = "\n".join([f"ID: {room['room_id']}, Type: {room['room_type']}, Price: ${room['price']}, Available: {'Yes' if room['is_available'] else 'No'}" for room in rooms])
        messagebox.showinfo("Rooms", rooms_str)
    else:
        messagebox.showinfo("Rooms", "No rooms available.")

# Occupancy report
def view_occupancy_report():
    rooms = load_data(ROOM_FILE)
    total_rooms = len(rooms)
    booked_rooms = sum(1 for room in rooms if not room['is_available'])
    available_rooms = total_rooms - booked_rooms
    report = f"Total Rooms: {total_rooms}\nBooked Rooms: {booked_rooms}\nAvailable Rooms: {available_rooms}"
    messagebox.showinfo("Occupancy Report", report)

# Load the background image for the registration frame
background_image = tk.PhotoImage(file='C:/syed/admin.png')  # Update the path
tk.Label(frame_add_employee, image=background_image).place(relwidth=1, relheight=1)  

# Add Employee Frame
tk.Label(frame_add_employee, text="Add Employee", font=("Copperplate Gothic Bold", 32), bg="dark gray",fg="white", width=35, height=1).pack(pady=50)
tk.Label(frame_add_employee, text="Employee ID:",  bg="dark gray",fg="white", font=("Helvetica", 14), width=25, height=1).pack(pady=30)
entry_employee_id = tk.Entry(frame_add_employee)
entry_employee_id.pack()
tk.Label(frame_add_employee, text="Employee Name:", font=("Helvetica", 14),  bg="dark gray",fg="white", width=35, height=2).pack(pady=30)
entry_employee_name = tk.Entry(frame_add_employee)
entry_employee_name.pack()
tk.Button(frame_add_employee, text="Add Employee", font=("Helvetica", 14), command=lambda: add_employee(entry_employee_id.get(), entry_employee_name.get()), bg="dark gray",fg="white", width=25, height=1).pack(pady=30)
tk.Button(frame_add_employee, text="Back to Admin Menu",font=("Helvetica", 14), command=lambda: show_frame(frame_admin), bg="dark gray",fg="white", width=25, height=1).pack(pady=30)

# Function to add employee
def add_employee(employee_id, employee_name):
    employees = load_data(EMPLOYEE_FILE)
    employees.append({'employee_id': employee_id, 'name': employee_name})
    save_data(EMPLOYEE_FILE, employees)
    messagebox.showinfo("Success", f"Employee {employee_name} added successfully!")
    show_frame(frame_admin)

# Delete Room Frame
# Load the background image for the registration frame
background_image2 = tk.PhotoImage(file='C:/syed/admin.png')  # Update the path
tk.Label(frame_delete_room, image=background_image2).place(relwidth=1, relheight=1)  

tk.Label(frame_delete_room, text="Delete Room", font=("Copperplate Gothic Bold", 32), bg="dark gray",fg="white", width=35, height=1).pack(pady=50)
tk.Label(frame_delete_room, text="Room ID:", font=("Helvetica", 14), bg="dark gray",fg="white", width=25, height=1).pack(pady=30)
entry_delete_room_id = tk.Entry(frame_delete_room)
entry_delete_room_id.pack()
tk.Button(frame_delete_room, text="Delete Room", font=("Helvetica", 14), command=lambda: delete_room(entry_delete_room_id.get()),bg="dark gray",fg="white", width=25, height=1).pack(pady=20)
tk.Button(frame_delete_room, text="Back to Admin Menu", font=("Helvetica", 14), command=lambda: show_frame(frame_admin),bg="dark gray",fg="white", width=25, height=1).pack(pady=30)

# Function to delete room
def delete_room(room_id):
    rooms = load_data(ROOM_FILE)
    for room in rooms:
        if room['room_id'] == room_id:
            rooms.remove(room)
            save_data(ROOM_FILE, rooms)
            messagebox.showinfo("Success", f"Room {room_id} deleted successfully!")
            show_frame(frame_admin)
            return
    messagebox.showerror("Error", f"Room ID {room_id} not found.")

# Book Room Frame
# Load the background image for the registration frame
background_image4 = tk.PhotoImage(file='C:/syed/user.png')  # Update the path
tk.Label(frame_book_room, image=background_image4).place(relwidth=1, relheight=1)  # Set the image to fill the frame

tk.Label(frame_book_room, text="Book a Room", font=("Copperplate Gothic Bold", 36),bg="light gray",fg="white", width=30, height=1).pack(pady=50)
tk.Label(frame_book_room, text="Enter Room ID:", font=("Helvetica", 15), bg="#87CEEB",width=35, height=2).pack(pady=30)
entry_book_room_id = tk.Entry(frame_book_room)
entry_book_room_id.pack()
tk.Button(frame_book_room, text="Book Room", font=("Helvetica", 15), bg="#87CEEB", command=lambda: book_room(entry_book_room_id.get(), entry_username.get()), width=25, height=1).pack(pady=30)
tk.Button(frame_book_room, text="Back to User Menu", font=("Helvetica", 15),bg="#87CEEB", command=lambda: show_frame(frame_user), width=20, height=1).pack(pady=30)

# Function to book room
def book_room(room_id, username):
    rooms = load_data(ROOM_FILE)
    bookings = load_data(BOOKING_FILE)
    
    for room in rooms:
        if room['room_id'] == room_id:
            if room['is_available']:
                room['is_available'] = False
                save_data(ROOM_FILE, rooms)
                
                bookings.append({'username': username, 'room_id': room_id})
                save_data(BOOKING_FILE, bookings)
                
                messagebox.showinfo("Success", f"Room {room_id} booked successfully!")
                show_frame(frame_user)
                return
            else:
                messagebox.showerror("Error", f"Room {room_id} is already booked.")
                return
    messagebox.showerror("Error", f"Room {room_id} not found.")

# Cancel Booking Frame
# Book Room Frame
# Load the background image for the registration frame
background_image5 = tk.PhotoImage(file='C:/syed/user.png')  # Update the path
tk.Label(frame_cancel_booking, image=background_image5).place(relwidth=1, relheight=1)  

tk.Label(frame_cancel_booking, text="Cancel Booking", font=("Copperplate Gothic Bold", 36), bg="light gray",fg="white", width=30, height=1).pack(pady=50)
tk.Label(frame_cancel_booking, text="Enter Room ID to cancel:", font=("Helvetica", 14), bg="#87CEEB", width=35, height=2).pack(pady=30)
entry_cancel_room_id = tk.Entry(frame_cancel_booking)
entry_cancel_room_id.pack()
tk.Button(frame_cancel_booking, text="Cancel Booking", font=("Helvetica", 14),bg="#87CEEB", command=lambda: cancel_booking(entry_cancel_room_id.get(), entry_username.get()), width=25, height=1).pack(pady=20)
tk.Button(frame_cancel_booking, text="Back to User Menu", font=("Helvetica", 14),bg="#87CEEB", command=lambda: show_frame(frame_user), width=25, height=2).pack(pady=30)

# Function to cancel booking
def cancel_booking(room_id, username):
    bookings = load_data(BOOKING_FILE)
    rooms = load_data(ROOM_FILE)

    for booking in bookings:
        if booking['username'] == username and booking['room_id'] == room_id:
            bookings.remove(booking)
            save_data(BOOKING_FILE, bookings)

            for room in rooms:
                if room['room_id'] == room_id:
                    room['is_available'] = True
                    break
            save_data(ROOM_FILE, rooms)

            messagebox.showinfo("Success", f"Booking for room {room_id} has been canceled successfully !")
            show_frame(frame_user)
            return

    messagebox.showerror("Error", f"No booking found for Room ID {room_id}.")

# User Bookings Frame
tk.Label(frame_view_bookings, text="My Bookings", font=("Copperplate Gothic Bold", 16), bg="#735DA5", width=35, height=2).pack(pady=30)
tk.Button(frame_view_bookings, text="View My Bookings", font=("Helvetica", 16), command=lambda: view_bookings(entry_username.get())).pack(pady=30)
tk.Button(frame_view_bookings, text="Back to User Menu", font=("Helvetica", 16), command=lambda: show_frame(frame_user), width=35, height=2).pack(pady=30)

# Function to view user bookings
def view_bookings(username):
    bookings = load_data(BOOKING_FILE)
    user_bookings = [booking for booking in bookings if booking['username'] == username]

    if user_bookings:
        sorted_bookings = bubble_sort(user_bookings)
        bookings_str = "\n".join([f"Room ID: {booking['room_id']}" for booking in user_bookings])
        messagebox.showinfo("My Bookings", f"Your Bookings:\n{bookings_str}")
    else:
        messagebox.showinfo("My Bookings", "You have no bookings.")

# Run the main program interface when the application starts
initialize_files()
show_frame(frame_login)
root.mainloop()