import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib


# Database setup
def setup_database():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )''')

    # Create inventory table
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                quantity INTEGER,
                price REAL
            )''')
    conn.commit()
    conn.close()


# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# User authentication functions
def register_user(username, password):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    hashed_password = hash_password(password)

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    hashed_password = hash_password(password)
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    result = c.fetchone()
    conn.close()

    return result is not None


# Inventory management functions
def add_product(name, quantity, price):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    c.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()
    conn.close()


def update_product(product_id, name, quantity, price):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    c.execute("UPDATE products SET name = ?, quantity = ?, price = ? WHERE id = ?", (name, quantity, price, product_id))
    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


def get_all_products():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()

    return products


def low_stock_alert(threshold=5):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    c.execute("SELECT * FROM products WHERE quantity <= ?", (threshold,))
    products = c.fetchall()
    conn.close()

    return products


# GUI setup
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")

        # Frames for login/register
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=10)

        self.inventory_frame = tk.Frame(self.root)
        self.inventory_frame.pack(pady=10)

        self.create_login_widgets()

    def create_login_widgets(self):
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Username").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.login_frame, text="Register", command=self.register).grid(row=3, column=0, columnspan=2)

    def create_inventory_widgets(self):
        self.inventory_frame.pack()

        tk.Label(self.inventory_frame, text="Product Name").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.inventory_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.inventory_frame, text="Quantity").grid(row=1, column=0)
        self.quantity_entry = tk.Entry(self.inventory_frame)
        self.quantity_entry.grid(row=1, column=1)

        tk.Label(self.inventory_frame, text="Price").grid(row=2, column=0)
        self.price_entry = tk.Entry(self.inventory_frame)
        self.price_entry.grid(row=2, column=1)

        tk.Button(self.inventory_frame, text="Add Product", command=self.add_product).grid(row=3, column=0, columnspan=2)

        tk.Button(self.inventory_frame, text="Show Inventory", command=self.show_inventory).grid(row=4, column=0, columnspan=2)
        tk.Button(self.inventory_frame, text="Low Stock Alert", command=self.show_low_stock).grid(row=5, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if login_user(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.login_frame.pack_forget()  # Hide login frame
            self.create_inventory_widgets()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            register_user(username, password)
        else:
            messagebox.showerror("Error", "Please enter both username and password.")

    def add_product(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if name and quantity.isdigit() and price.replace('.', '', 1).isdigit():
            add_product(name, int(quantity), float(price))
            messagebox.showinfo("Success", "Product added successfully!")
        else:
            messagebox.showerror("Error", "Please provide valid product details.")

    def show_inventory(self):
        products = get_all_products()

        inventory_window = tk.Toplevel(self.root)
        inventory_window.title("Inventory List")

        for idx, product in enumerate(products):
            tk.Label(inventory_window, text=f"{product[1]} | Qty: {product[2]} | Price: ${product[3]}").pack()

    def show_low_stock(self):
        low_stock_products = low_stock_alert()

        alert_window = tk.Toplevel(self.root)
        alert_window.title("Low Stock Alerts")

        if low_stock_products:
            for product in low_stock_products:
                tk.Label(alert_window, text=f"{product[1]} | Qty: {product[2]}").pack()
        else:
            tk.Label(alert_window, text="No products are low on stock.").pack()


if __name__ == "__main__":
    setup_database()

    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
