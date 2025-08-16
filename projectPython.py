from tkinter import *
from tkinter import messagebox
import sqlite3 
from tkinter import ttk
import tkinter as tk
from tkinter import Label, Toplevel
from PIL import Image, ImageTk
from tkcalendar import Calendar
from datetime import datetime
import customtkinter as ctk
current_user_id = None
import time
import shutil
import re
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas as pdf_canvas  
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
import os
from tkcalendar import Calendar, DateEntry

root = Tk()
root.title('Joyful Kingdom')
root.geometry('925x500+300+200')
root.configure(bg='#fff')
root.resizable(False, False)
#####################################################################################################################################################
def create_database():
    conn = sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db")
    cursor = conn.cursor()

#     # สร้างตาราง users
#     cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#                         user_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         username TEXT NOT NULL UNIQUE,
#                         password TEXT NOT NULL,
#                         ticket_id INTEGER)''')

#     # สร้างตาราง tickets
    cursor.execute('''CREATE TABLE IF NOT EXISTS tickets_new (
                        ticket_id INTEGER,
                        user_id INTEGER NOT NULL,
                        ticket_date TEXT,
                        child_qty INTEGER,
                        adult_qty INTEGER,
                        additional_ticket_id INTEGER,
                        additional_child_qty INTEGER,
                        additional_adult_qty INTEGER,
                        total_qty INTEGER,
                        total_price INTEGER)''')

    conn.commit()
    conn.close()
    
    # cursor.execute('''CREATE TABLE IF NOT EXISTS cart (
    #                     cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                     user_id INTEGER NOT NULL,
    #                     ticket_date TEXT NOT NULL,
    #                     ticket_id INTEGER NOT NULL,
    #                     child_qty INTEGER DEFAULT 0,
    #                     adult_qty INTEGER DEFAULT 0,
    #                     additional_ticket_id INTEGER,
    #                     additional_child_qty INTEGER DEFAULT 0,
    #                     additional_adult_qty INTEGER DEFAULT 0,
    #                     total_qty INTEGER NOT NULL,
    #                     total_price REAL NOT NULL,
    #                     FOREIGN KEY (user_id) REFERENCES users(user_id),
    #                     FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id),
    #                     FOREIGN KEY (additional_ticket_id) REFERENCES tickets(ticket_id))''')
    
    # cursor.execute('''CREATE TABLE payment_proof2 (
    #                     payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                     user_id INTEGER NOT NULL,
    #                     file_path TEXT NOT NULL,
    #                     total_price REAL NOT NULL,
    #                     upload_time DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # cursor.execute("PRAGMA table_info(tickets_new)")
    # columns = [col[1] for col in cursor.fetchall()]
    # if "status" not in columns:
    #     cursor.execute("ALTER TABLE tickets_new ADD COLUMN status TEXT DEFAULT 'Pending';")

    # conn.commit()
    # print("Table created or updated successfully!")

    # conn.close()

create_database()

###########################################################################-----------------------------------------------------------------------------------
def signin():
    username = user.get()
    password = code.get()

    try:
        # เชื่อมต่อกับฐานข้อมูล SQLite
        conn = sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db")
        cursor = conn.cursor()
        
        # ค้นหาผู้ใช้จากฐานข้อมูล
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()

        if username == "admin" and password == "admin1234":  # แทนที่ "your_admin_password" ด้วยรหัสสำหรับ Admin
            root.withdraw()  # ซ่อนหน้าต่างหลัก
            open_admin_page()  # เรียกฟังก์ชันเพื่อแสดงหน้าต่าง Admin
            return

        # ค้นหาผู้ใช้จากฐานข้อมูล
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()

        if result:
            global current_user_id
            current_user_id = result[0]  # บันทึก user_id
            root.withdraw()
            # หากชื่อผู้ใช้และรหัสผ่านถูกต้อง ให้แสดงหน้าหลัก
            main_page()
        else:
            # แสดงข้อความแจ้งเตือนหากชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง
            messagebox.showerror('Invalid', 'Invalid username or password')
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
    finally:
        conn.close()
##########################################################################################################################################################################
screen = None

def on_close():
    root.quit()

def main_page():
    global screen
    if screen and screen.winfo_exists():
        screen.focus()
        return
    
    screen = Toplevel(root)
    screen.title("Main Page")
    screen.geometry('925x500+300+200')
    screen.config(bg='#5c609b')
    screen.resizable(False, False)

    # เพิ่มภาพในหน้าหลัก
    img_main = PhotoImage(file=r"C:\Users\HUAWEI\Downloads\main page.png")
    image_label = Label(screen, image=img_main, bg="#5c609b")
    image_label.image = img_main  # เก็บอ้างอิงรูปเพื่อป้องกันการเก็บภาพ
    image_label.pack(expand=True)

    # เพิ่มปุ่มในหน้าหลัก
    button_frame = ctk.CTkFrame(screen, fg_color='#5c609b', corner_radius=0, border_width=0)
    button_frame.place(relx=0.5, rely=0.8, anchor="center")
    
    create_button(button_frame, "Rides", go_to_rides_page)
    create_button(button_frame, "Ticket", go_to_ticket_page)
    create_button(button_frame, "Personal info", go_to_info_page)
    create_button(button_frame, "About us", go_to_contact_page)
    logout_button = ctk.CTkButton(
        screen, 
        text="Logout", 
        corner_radius=20, 
        width=115, 
        height=30, 
        fg_color="#ffc5e2", 
        hover_color="#6420AA", 
        text_color="white", 
        font=('Arial', 14, 'bold'), 
        border_width=0, 
        command=confirm_logout
    )
    logout_button.place(relx=0.01, rely=0.01, x=37, y=17, anchor="nw")

    screen.protocol('WM_DELETE_WINDOW', on_close_main_page)
    screen.mainloop()

def confirm_logout():
    result = messagebox.askyesno("ยืนยันการออกจากระบบ", "คุณแน่ใจที่จะออกจากระบบหรือไม่?")
    if result:  # ถ้าผู้ใช้กด "Yes"
        logout()

def logout():
    global screen
    if screen:
        screen.destroy()  # ปิดหน้าต่าง main_page
        screen = None
    root.deiconify()

def on_close_main_page():
    global screen
    if screen:
        screen.destroy()
        screen = None
##################################################################################--------------------------------------------------------------------------
def create_button(parent, text, command):
        button = ctk.CTkButton(parent, text=text, corner_radius=20,width=150,height=60, fg_color="#FF7ED4", hover_color="#6420AA", 
                            text_color="white", font=('Arial', 20, 'bold'), border_width=0, command=command)
        button.pack(side="left", padx=10, pady=20)

def back_to_main(current_page):
    current_page.destroy()  # ปิดหน้าปัจจุบัน
    main_page()             # เปิดหน้าหลัก

def create_back_button(parent, text, command):
    button = ctk.CTkButton(
        parent,
        text=text,
        corner_radius=20,
        width=80,
        height=40,
        fg_color="white",
        hover_color="#6420AA",
        text_color="#FF7ED4",
        font=('Arial', 16, 'bold'),
        border_width=0,
        command=command
    )
    button.pack(side="left", padx=10, pady=20)

#====================================================================================================================================

def open_admin_page():
    global win
    win = tk.Toplevel()
    win.geometry("1350x700+0+0")
    win.title("Customer Management System")

    title_label = tk.Label(win,text="Customer Management System", font=("Arial",30,"bold"),border=12,relief=tk.GROOVE,bg="lightgrey")
    title_label.pack(side=tk.TOP, fill=tk.X)
    
    logout_btn = tk.Button(title_label, bg="lightgrey", text="Logout", bd=5, font=("Arial", 10), width=10, command=confirm_logoutadmin)
    logout_btn.pack(side=tk.LEFT, padx=10)

    detail_frame = tk.LabelFrame(win, text="Enter Details", font=("Arial",20), bd=12,relief=tk.GROOVE, bg="lightgrey")
    detail_frame.place(x=20,y=90,width=420,height=575)

    data_frame = tk.Frame(win, bd=12,bg="lightgrey", relief=tk.GROOVE)
    data_frame.place(x=475,y=90,width=850,height=575)

    #3==================variable========================

    users_id=tk.StringVar()
    name=tk.StringVar()
    email=tk.StringVar()
    phone=tk.StringVar()
    ticket_type=tk.StringVar()
    child_qty=tk.StringVar()
    adult_qty=tk.StringVar()
    add_ticket=tk.StringVar()
    child_qty2=tk.StringVar()
    adult_qty2=tk.StringVar()
    total_price=tk.StringVar()
    payment_proof=tk.StringVar()
    date=tk.StringVar()
    purchase_date=tk.StringVar()
    search_by = tk.StringVar()
    search_value = tk.StringVar()
    year_var = tk.StringVar()
    month_var = tk.StringVar()
    day_var = tk.StringVar()

    #===========entry==============================
    fields = [
        ("User ID", users_id),
        ("Name", name),
        ("Email", email),
        ("Phone", phone),
        ("Date", date),
        ("Purchase Date", purchase_date),
        ("Ticket Type", ticket_type),
        ("Child Quantity", child_qty),
        ("Adult Quantity", adult_qty),
        ("Additional Ticket", add_ticket),
        ("Child Quantity 2", child_qty2),
        ("Adult Quantity 2", adult_qty2),
        ("Total Price", total_price),
        ("Payment Proof", payment_proof),
    ]

    # Generate labels and entries
    for i, (label_text, var) in enumerate(fields):
        tk.Label(
            detail_frame, text=label_text, font=("Arial",   10), bg="lightgrey"
        ).grid(row=i, column=0, padx=5, pady=3, sticky="w")  # Smaller font for labels
        tk.Entry(
            detail_frame, textvariable=var, bd=3, font=("Arial", 8), width=40
        ).grid(row=i, column=1, padx=5, pady=3, sticky="w")  # Smaller font and entry size

    #==============================function===================================

    def fetch_data():
        try:
            # เชื่อมต่อฐานข้อมูล
            conn = sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db")
            cursor = conn.cursor()

            # ใช้คำสั่ง SQL เพื่อดึงข้อมูลที่ต้องการ
            query = """
            SELECT 
                t.user_id, 
                u.name, 
                u.email, 
                u.phone_number AS phone, 
                t.ticket_date,
                t.purchase_date, 
                t.ticket_name, 
                t.child_qty, 
                t.adult_qty, 
                t.additional_ticket_name, 
                t.additional_child_qty AS additional_child, 
                t.additional_adult_qty AS additional_adult, 
                t.total_price, 
                t.status
            FROM tickets_new t
            JOIN users u ON t.user_id = u.user_id;
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # ล้างข้อมูลใน Treeview
            customer_table.delete(*customer_table.get_children())

            # กำหนดราคาบัตร
            prices = {
                "บัตรผ่านประตู": {"child_price": 250, "adult_price": 300},
                "บัตรรวมเครื่องเล่น": {"child_price": 600, "adult_price": 600},
                "บัตรจอยฟูลวีซ่า": {"child_price": 700, "adult_price": 800},
                "บัตรซุปเปอร์วีซ่า": {"child_price": 1000, "adult_price": 1000},
            }

            total_adult_price = 0
            total_child_price = 0

            # เติมข้อมูลใหม่ลงใน Treeview และคำนวณราคาทั้งหมด
            for row in rows:
                customer_table.insert('', tk.END, values=row)
                ticket_type = row[6]
                child_qty = int(row[7]) if row[7] else 0
                adult_qty = int(row[8]) if row[8] else 0
                ticket_type2 = row[9]
                child_qty2 = int(row[10]) if row[10] else 0
                adult_qty2 = int(row[11]) if row[11] else 0

                try:
                    # print(f"Prices dictionary: {prices}")

                    # # Debugging statements for ticket types
                    # print(f"Ticket Type 1: {ticket_type}, Ticket Type 2: {ticket_type2}")

                    child_price1 = child_qty * prices.get(ticket_type, {}).get("child_price", 0)
                    child_price2 = child_qty2 * prices.get(ticket_type2, {}).get("child_price", 0)
                    total_child_price += int(child_price1) + int(child_price2)

                    adult_price1 = adult_qty * prices.get(ticket_type, {}).get("adult_price", 0)
                    adult_price2 = adult_qty2 * prices.get(ticket_type2, {}).get("adult_price", 0)
                    total_adult_price += int(adult_price1) + int(adult_price2)

                    # Debugging statements
                #     print(f"Row: {row}")
                #     print(f"Ticket Type 1: {ticket_type}, Child Qty: {child_qty}, Adult Qty: {adult_qty}, Child Price: {child_price1}, Adult Price: {adult_price1}")
                #     print(f"Ticket Type 2: {ticket_type2}, Child Qty 2: {child_qty2}, Adult Qty 2: {adult_qty2}, Child Price 2: {child_price2}, Adult Price 2: {adult_price2}")
                #     print(f"Total child price so far: {total_child_price}")
                #     print(f"Total adult price so far: {total_adult_price}")
                except KeyError as e:
                    print(f"Error: {e}")

            total_price = total_child_price + total_adult_price

            # อัปเดตค่าใน Label
            total_child_value.config(text=f"{total_child_price:,} บาท")
            total_adult_value.config(text=f"{total_adult_price:,} บาท")
            total_price_value.config(text=f"{total_price:,} บาท")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    # Add Data Function
    def add_func():
        try:
            conn = sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db")
            cursor = conn.cursor()

            # ตรวจสอบว่าได้ค่าจาก name หรือไม่
            user_name = name.get()
            if not user_name:
                messagebox.showerror("Input Error", "Please enter a name.")
                return

            # เพิ่มข้อมูลใหม่ลงในตาราง users
            cursor.execute("""
                INSERT INTO users (user_id, name, username, email, phone_number, password)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                users_id.get(),  # user_id
                user_name,       # name
                "default username",  # username (ค่าเริ่มต้น)
                email.get(),     # email
                phone.get(),     # phone_number
                "default password"  # password (ค่าเริ่มต้น)
            ))

            # เพิ่มข้อมูลใหม่ลงในตาราง tickets_new
            cursor.execute("""
                INSERT INTO tickets_new (user_id, ticket_name, child_qty, adult_qty, additional_ticket_name, additional_child_qty, additional_adult_qty, total_price, status, ticket_date, purchase_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                users_id.get(),       # user_id
                ticket_type.get(),    # ticket_name
                child_qty.get(),      # child_qty
                adult_qty.get(),      # adult_qty
                add_ticket.get(),     # additional_ticket_name
                child_qty2.get(),     # additional_child_qty
                adult_qty2.get(),     # additional_adult_qty
                total_price.get(),    # total_price
                payment_proof.get(),  # status
                date.get(),           # ticket_date
                purchase_date.get()   # purchase_date
            ))

            conn.commit()
            messagebox.showinfo("Success", "Data added successfully!")
            fetch_data()  # รีเฟรชข้อมูลใน Treeview

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close() 

    def get_selected_row(event):
        # ดึงตำแหน่งของแถวที่เลือกใน Treeview
        selected_row = customer_table.focus()
        
        # ดึงค่าของข้อมูลในแถวที่เลือก
        data = customer_table.item(selected_row, 'values')
        
        if data:
            # นำข้อมูลจากแถวใน Treeview ไปแสดงใน Entry
            users_id.set(data[0])  # user_id
            name.set(data[1])     # name
            email.set(data[2])    # email
            phone.set(data[3])    # phone
            date.set(data[4])        # date
            purchase_date.set(data[5]) # purchase date
            ticket_type.set(data[6])  # ticket type
            child_qty.set(data[7])    # child qty
            adult_qty.set(data[8])    # adult qty
            add_ticket.set(data[9])   # additional ticket
            child_qty2.set(data[10])   # additional child qty
            adult_qty2.set(data[11])   # additional adult qty
            total_price.set(data[12]) # total price
            payment_proof.set(data[13]) # payment proof

    def update_data():
        try:
            conn = sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db")
            cursor = conn.cursor()

            # ตรวจสอบว่าเลือกแถวใน Treeview หรือไม่
            selected_row = customer_table.focus()
            data = customer_table.item(selected_row, 'values')
            if not data:
                messagebox.showerror("Error", "Please select a row to update!")
                return

            # อัปเดตข้อมูลในฐานข้อมูล
            cursor.execute("""
                UPDATE tickets_new
                SET ticket_name = ?, child_qty = ?, adult_qty = ?, 
                    additional_ticket_name = ?, additional_child_qty = ?, 
                    additional_adult_qty = ?, total_price = ?, status = ?, purchase_date = ?
                WHERE user_id = ? AND ticket_date = ?
            """, (
                ticket_type.get(), child_qty.get(), adult_qty.get(),
                add_ticket.get(), child_qty2.get(), adult_qty2.get(),
                total_price.get(), payment_proof.get(), purchase_date.get(),
                data[0], data[4]  # ใช้ User ID และ Date ในการอ้างอิง
            ))

            conn.commit()
            messagebox.showinfo("Success", "Data updated successfully!")
            fetch_data()  # รีเฟรชข้อมูลใน Treeview

            # ตรวจสอบว่า selected_row ยังคงอยู่ใน Treeview
            if selected_row in customer_table.get_children():
                # อัปเดตข้อมูลในแถวที่เลือกใน Treeview โดยตรง
                customer_table.item(selected_row, values=(
                    data[0], data[1], data[2], data[3], data[4], 
                    ticket_type.get(), child_qty.get(), adult_qty.get(),
                    add_ticket.get(), child_qty2.get(), adult_qty2.get(),
                    total_price.get(), payment_proof.get(), purchase_date.get()
                ))

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    from datetime import datetime

    def delete_data():
        try:
            conn = sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db")
            conn.execute("PRAGMA foreign_keys = ON;")  # เปิดใช้งาน Foreign Key
            cursor = conn.cursor()

            # ตรวจสอบว่าเลือกแถวใน Treeview หรือไม่
            selected_row = customer_table.focus()
            data = customer_table.item(selected_row, 'values')
            if not data:
                messagebox.showerror("Error", "Please select a row to delete!")
                return

            # ดึงข้อมูล user_id และ ticket_date
            user_id = data[0]
            ticket_date = data[4]

            # Debugging: ตรวจสอบค่าก่อนลบ
            # print(f"Trying to delete: user_id={user_id}, ticket_date={ticket_date}")

            # ตรวจสอบว่าข้อมูลนี้อยู่ในตาราง tickets_new
            cursor.execute("SELECT * FROM tickets_new WHERE user_id = ? AND ticket_date = ?", (user_id, ticket_date))
            result = cursor.fetchall()
            # print("Data found in tickets_new before delete:", result)

            if not result:
                messagebox.showerror("Error", "Data not found in tickets_new!")
                return

            # ลบข้อมูลในตาราง tickets_new
            cursor.execute("DELETE FROM tickets_new WHERE user_id = ?", (user_id,))
            conn.commit()

            # ตรวจสอบว่ามีข้อมูลใน tickets_new คงเหลือหรือไม่
            cursor.execute("SELECT * FROM tickets_new WHERE user_id = ?", (user_id,))
            result_after_tickets = cursor.fetchall()
            # print("Data found in tickets_new after delete:", result_after_tickets)

            if result_after_tickets:
                messagebox.showerror("Error", "Failed to delete data from tickets_new!")
                return

            # ลบข้อมูลในตาราง users
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            conn.commit()

            # ตรวจสอบว่าข้อมูลใน users คงเหลือหรือไม่
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            result_after_users = cursor.fetchall()
            # print("Data found in users after delete:", result_after_users)

            if result_after_users:
                messagebox.showerror("Error", "Failed to delete data from users!")
            else:
                messagebox.showinfo("Success", "Data deleted successfully from both tables!")
                fetch_data()  # รีเฟรชข้อมูลใน Treeview

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def clear_fields():
        users_id.set("")
        name.set("")
        email.set("")
        phone.set("")
        ticket_type.set("")
        child_qty.set("")
        adult_qty.set("")
        add_ticket.set("")
        child_qty2.set("")
        adult_qty2.set("")
        total_price.set("")
        payment_proof.set("")
        date.set("")
        purchase_date.set("")

    def search_data():
        search_by_value = search_by.get()
        search_text = search_value.get()

        try:
            conn = sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db")
            cursor = conn.cursor()

            if search_by_value == "Month":
                # สร้าง mapping ระหว่างชื่อเดือนภาษาอังกฤษกับตัวเลขเดือน
                month_mapping = {
                    "January": "01", "February": "02", "March": "03", "April": "04",
                    "May": "05", "June": "06", "July": "07", "August": "08",
                    "September": "09", "October": "10", "November": "11", "December": "12"
                }
                month_number = month_mapping.get(search_text)
                if month_number:
                    query = """
                    SELECT DISTINCT
                        t.user_id, 
                        u.name, 
                        u.email, 
                        u.phone_number AS phone, 
                        t.ticket_date,
                        t.purchase_date, 
                        t.ticket_name, 
                        t.child_qty, 
                        t.adult_qty, 
                        t.additional_ticket_name, 
                        t.additional_child_qty AS additional_child, 
                        t.additional_adult_qty AS additional_adult, 
                        t.total_price, 
                        t.status
                    FROM tickets_new t
                    JOIN users u ON t.user_id = u.user_id
                    WHERE strftime('%m', t.purchase_date) = ?;
                    """
                    cursor.execute(query, (month_number,))
                else:
                    print("กรุณาเลือกชื่อเดือนภาษาอังกฤษที่ถูกต้อง")
                    update_totals()

            elif search_by_value == "Day":
                year = year_var.get()
                month = month_var.get()
                day = day_var.get()
                
                if not year or not month or not day:
                    messagebox.showerror("Error", "กรุณาเลือกช่องค้นหาและป้อนค่าที่ต้องการค้นหา!")
                    return

                try:
                    selected_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    # print(f"Selected date: {selected_date}")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format!")
                    return

                query = """
                SELECT DISTINCT
                    t.user_id, 
                    u.name, 
                    u.email, 
                    u.phone_number AS phone, 
                    t.ticket_date,
                    t.purchase_date, 
                    t.ticket_name, 
                    t.child_qty, 
                    t.adult_qty, 
                    t.additional_ticket_name, 
                    t.additional_child_qty AS additional_child, 
                    t.additional_adult_qty AS additional_adult, 
                    t.total_price, 
                    t.status
                FROM tickets_new t
                JOIN users u ON t.user_id = u.user_id
                WHERE strftime('%Y-%m-%d', t.purchase_date) = ?;
                """
                # print(f"Executing query with date: {selected_date}")
                cursor.execute(query, (selected_date,))

            elif search_by_value == "Ticket type":
                query = """
                SELECT DISTINCT
                    t.user_id, 
                    u.name, 
                    u.email, 
                    u.phone_number AS phone, 
                    t.ticket_date,
                    t.purchase_date, 
                    t.ticket_name, 
                    t.child_qty, 
                    t.adult_qty, 
                    t.additional_ticket_name, 
                    t.additional_child_qty AS additional_child, 
                    t.additional_adult_qty AS additional_adult, 
                    t.total_price, 
                    t.status
                FROM tickets_new t
                JOIN users u ON t.user_id = u.user_id
                WHERE t.ticket_name = ? OR t.additional_ticket_name = ?;
                """
                cursor.execute(query, (search_text, search_text))
            else:
                messagebox.showerror("Error", "การค้นหานี้ไม่รองรับ!")
                return
            
            update_totals()

            rows = cursor.fetchall()

            # ล้างข้อมูลใน Treeview
            customer_table.delete(*customer_table.get_children())

            # แสดงผลลัพธ์ใน Treeview
            for row in rows:
                customer_table.insert('', 'end', values=row)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"เกิดข้อผิดพลาด: {e}")
        finally:
            if conn:
                update_totals()
                conn.close()
            
    def update_combobox2(event):
        selected = search_by.get()
        combobox2.grid_remove()
        year_combobox.grid_remove()
        month_combobox.grid_remove()
        day_combobox.grid_remove()

        if selected == "Month":
            combobox2["values"] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            combobox2.grid(row=0, column=2, padx=5, pady=2)
            combobox2.current(0)
        elif selected == "Day":
            year_combobox.grid(row=0, column=2, padx=5, pady=2)
            month_combobox.grid(row=0, column=3, padx=5, pady=2)
            day_combobox.grid(row=0, column=4, padx=5, pady=2)
        elif selected == "Ticket type":
            combobox2["values"] = ["บัตรผ่านประตู", "บัตรรวมเครื่องเล่น", "บัตรจอยฟูลวีซ่า", "บัตรซุปเปอร์วีซ่า"]
            combobox2.grid(row=0, column=2, padx=5, pady=2)
            combobox2.current(0)

    def update_totals():
        try:
            # รีเซ็ตยอดรวม
            total_child_price = 0
            total_adult_price = 0

            # ราคาบัตรที่กำหนด
            prices = {
                "บัตรผ่านประตู": {"child_price": 250, "adult_price": 300},
                "บัตรรวมเครื่องเล่น": {"child_price": 600, "adult_price": 600},
                "บัตรจอยฟูลวีซ่า": {"child_price": 700, "adult_price": 800},
                "บัตรซุปเปอร์วีซ่า": {"child_price": 1000, "adult_price": 1000},
            }

            # ดึงประเภทการค้นหา
            selected = search_by.get()
            selected_value = combobox2.get()
            selected_day = None

            # ถ้าการค้นหาเป็น "Day" ให้ดึงค่าวันที่
            if selected == "Day":
                year = year_var.get()
                month = month_var.get()
                day = day_var.get()
                if year and month and day:
                    selected_day = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

            # วนลูปคำนวณยอดรวมจากข้อมูลใน Treeview
            for row in customer_table.get_children():
                item = customer_table.item(row)
                values = item['values']

                # ฟังก์ชันช่วยแปลงข้อมูลให้เป็นตัวเลข
                def safe_int(value):
                    if isinstance(value, int):
                        return value
                    elif isinstance(value, str) and value.isdigit():
                        return int(value)
                    else:
                        return 0

                # ดึงค่าจาก Treeview
                ticket_type = values[6]
                child_qty = safe_int(values[7])
                adult_qty = safe_int(values[8])
                ticket_type2 = values[9]
                child_qty2 = safe_int(values[10])
                adult_qty2 = safe_int(values[11])
                purchase_date = values[5]

                # เงื่อนไขตรวจสอบการค้นหาใน "Day"
                if selected == "Day" and selected_day:
                    if purchase_date == selected_day:
                        # คำนวณราคาตามประเภทบัตร
                        if ticket_type in prices:
                            child_price = child_qty * prices[ticket_type]["child_price"]
                            adult_price = adult_qty * prices[ticket_type]["adult_price"]
                            total_child_price += child_price
                            total_adult_price += adult_price

                        if ticket_type2 in prices:
                            child_price2 = child_qty2 * prices[ticket_type2]["child_price"]
                            adult_price2 = adult_qty2 * prices[ticket_type2]["adult_price"]
                            total_child_price += child_price2
                            total_adult_price += adult_price2

                # เงื่อนไขสำหรับการค้นหาอื่นๆ เช่น "Month"
                elif selected == "Month":
                    purchase_month = datetime.strptime(purchase_date, "%Y-%m-%d").strftime("%B")
                    if purchase_month == selected_value:
                        if ticket_type in prices:
                            child_price = child_qty * prices[ticket_type]["child_price"]
                            adult_price = adult_qty * prices[ticket_type]["adult_price"]
                            total_child_price += child_price
                            total_adult_price += adult_price

                        if ticket_type2 in prices:
                            child_price2 = child_qty2 * prices[ticket_type2]["child_price"]
                            adult_price2 = adult_qty2 * prices[ticket_type2]["adult_price"]
                            total_child_price += child_price2
                            total_adult_price += adult_price2

            # รวมยอดทั้งหมด
            total_price = total_child_price + total_adult_price

            # อัปเดตค่าใน Label
            total_child_value.config(text=f"{total_child_price:,} บาท")
            total_adult_value.config(text=f"{total_adult_price:,} บาท")
            total_price_value.config(text=f"{total_price:,} บาท")

        except Exception as e:
            print(f"Error: {e}")

    
    #---------------button--------------------------------------------------------------------------------

    btn_frame = tk.Frame(detail_frame, bg="lightgrey", bd=10, relief=tk.GROOVE)
    btn_frame.place(x=22, y=410, width=340, height=120)  # ปรับค่า y จาก 390 เป็น 410

    add_btn = tk.Button(btn_frame, bg="lightgrey", text="Add", bd=7, font=("Arial", 13), width=15, command=add_func)
    add_btn.grid(row=0, column=0, padx=2, pady=2)

    update_btn = tk.Button(btn_frame, bg="lightgrey", text="Update", bd=7, font=("Arial", 13), width=15, command=update_data)
    update_btn.grid(row=0, column=1, padx=3, pady=2)

    delete_btn = tk.Button(btn_frame, bg="lightgrey", text="Delete", bd=7, font=("Arial", 13), width=15, command=delete_data)
    delete_btn.grid(row=1, column=0, padx=2, pady=2)

    clear_btn = tk.Button(btn_frame, bg="lightgrey", text="Clear", bd=7, font=("Arial", 13), width=15, command=clear_fields)
    clear_btn.grid(row=1, column=1, padx=3, pady=2)

    search_frame = tk.Frame(data_frame, bg="lightgrey", bd=10, relief=tk.GROOVE)
    search_frame.pack(side=tk.TOP, fill=tk.X)

    search_lbl = tk.Label(search_frame, text="Search", bg="lightgrey", font=("Arial", 10))
    search_lbl.grid(row=0, column=0, padx=5, pady=2)

    combobox1 = ttk.Combobox(search_frame, textvariable=search_by, font=("Arial", 10), state="readonly", width=15)
    combobox1["values"] = ["Month", "Day", "Ticket type"]
    combobox1.grid(row=0, column=1, padx=5, pady=2)
    combobox1.bind("<<ComboboxSelected>>", update_combobox2)

    combobox2 = ttk.Combobox(search_frame, textvariable=search_value, font=("Arial", 10), state="readonly", width=15)
    combobox2.grid(row=0, column=2, padx=5, pady=2)
    combobox2.grid_remove()

    years = [str(year) for year in range(2000, 2031)]
    months = [str(month).zfill(2) for month in range(1, 13)]
    days = [str(day).zfill(2) for day in range(1, 32)]

    year_combobox = ttk.Combobox(search_frame, values=years,textvariable=year_var, font=("Arial", 10), state="readonly", width=5)
    year_combobox.grid(row=0, column=2, padx=5, pady=2)
    year_combobox.grid_remove()

    month_combobox = ttk.Combobox(search_frame, values=months, textvariable=month_var, font=("Arial", 10), state="readonly", width=3)
    month_combobox.grid(row=0, column=3, padx=5, pady=2)
    month_combobox.grid_remove()

    day_combobox = ttk.Combobox(search_frame, values=days, textvariable=day_var, font=("Arial", 10), state="readonly", width=3)
    day_combobox.grid(row=0, column=4, padx=5, pady=2)
    day_combobox.grid_remove()

    search_btn = tk.Button(search_frame, bg="lightgrey", text="Search", bd=5, font=("Arial", 10), width=10, command=search_data)
    search_btn.grid(row=0, column=5, padx=5, pady=2)

    # ปุ่มแสดงทั้งหมด
    showall_btn = tk.Button(search_frame, bg="lightgrey", text="Show all", font=("Arial", 10), bd=5, width=10, command=fetch_data)
    showall_btn.grid(row=0, column=6, padx=5, pady=2)

    #======================================Data Frame=============================================

    main_frame = tk.Frame(data_frame, bg="lightgrey", bd=11, relief=tk.GROOVE)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Scrollbars
    y_scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
    x_scroll = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)

    # Treeview
    customer_table = ttk.Treeview(
        main_frame,
        columns=(
            "User_ID", "Name", "Email", "Phone", 
            "Date", "Purchase_date", "Ticket_type", "Child", "Adult", 
            "Ticket_type2", "Child_2", "Adult_2", 
            "Total_price", "Payment_proof"
        ),
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set,
    )

    # Configure Scrollbars
    y_scroll.config(command=customer_table.yview)
    x_scroll.config(command=customer_table.xview)

    # Place Scrollbars
    y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    # Place Treeview
    customer_table.pack(fill=tk.BOTH, expand=True)

    # กำหนด heading ให้ตรงกับ columns
    customer_table.heading("User_ID", text="User_ID")
    customer_table.heading("Name", text="Name")
    customer_table.heading("Email", text="Email")
    customer_table.heading("Phone", text="Phone")
    customer_table.heading("Date", text="Date")
    customer_table.heading("Purchase_date", text="Purchase_date")
    customer_table.heading("Ticket_type", text="Ticket_type")
    customer_table.heading("Child", text="Child")
    customer_table.heading("Adult", text="Adult")
    customer_table.heading("Ticket_type2", text="Ticket_type2")
    customer_table.heading("Child_2", text="Child_2")
    customer_table.heading("Adult_2", text="Adult 2")
    customer_table.heading("Total_price", text="Total_price")
    customer_table.heading("Payment_proof", text="Payment_proof")

    customer_table['show'] = 'headings'

    # กำหนด column ให้ตรงกับ columns
    customer_table.column("User_ID", width=100)
    customer_table.column("Name", width=100)
    customer_table.column("Email", width=100)
    customer_table.column("Phone", width=100)
    customer_table.column("Date", width=100)
    customer_table.column("Purchase_date", width=100)
    customer_table.column("Ticket_type", width=100)
    customer_table.column("Child", width=100)
    customer_table.column("Adult", width=100)
    customer_table.column("Ticket_type2", width=100)
    customer_table.column("Child_2", width=100)
    customer_table.column("Adult_2", width=100)
    customer_table.column("Total_price", width=100)
    customer_table.column("Payment_proof", width=100)

    customer_table.pack(fill=tk.BOTH, expand=True)

    customer_table.bind("<ButtonRelease-1>", get_selected_row)

    footer_frame = tk.Frame(data_frame, bg="lightgrey", bd=5, relief=tk.GROOVE)
    footer_frame.pack(fill=tk.X)

    # Labels for totals
    total_child_label = tk.Label(footer_frame, text="ยอดรวมเด็ก:", font=("Arial", 12), bg="lightgrey")
    total_child_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    total_child_value = tk.Label(footer_frame, text="0", font=("Arial", 12), bg="white", relief=tk.SUNKEN, width=10)
    total_child_value.grid(row=0, column=1, padx=10, pady=5)
    
    total_adult_label = tk.Label(footer_frame, text="ยอดรวมผู้ใหญ่:", font=("Arial", 12), bg="lightgrey")
    total_adult_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    total_adult_value = tk.Label(footer_frame, text="0", font=("Arial", 12), bg="white", relief=tk.SUNKEN, width=10)
    total_adult_value.grid(row=0, column=3, padx=10, pady=5)

    total_price_label = tk.Label(footer_frame, text="ยอดรวมทั้งหมด:", font=("Arial", 12), bg="lightgrey")
    total_price_label.grid(row=0, column=4, padx=10, pady=5, sticky="w")

    total_price_value = tk.Label(footer_frame, text="0", font=("Arial", 12), bg="white", relief=tk.SUNKEN, width=10)
    total_price_value.grid(row=0, column=5, padx=10, pady=5)

    fetch_data()

    win.mainloop()

def confirm_logoutadmin(): 
    result = messagebox.askyesno("ยืนยันการออกจากระบบ", "คุณแน่ใจที่จะออกจากระบบหรือไม่?") 
    if result:  # ถ้าผู้ใช้กด "Yes" 
        logoutadmin()

def logoutadmin():
    global win
    if win:
        win.destroy()  # ปิดหน้าต่างหลัก
        win = None
    root.deiconify()  # แสดงหน้าต่างหลักอีกครั้ง

##################################################################################################################################################################

def go_to_rides_page():
    rides_page = Toplevel(root)
    rides_page.title('Rides')
    rides_page.geometry('925x500+300+200')
    rides_page.resizable(False, False)

    # โหลดรูปภาพพื้นหลัง
    bg_image = PhotoImage(file=r"C:\Users\HUAWEI\Downloads\amusement (8).png")
    bg_label = Label(rides_page, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_image

    # รายชื่อไฟล์รูปภาพ
    image_files = [
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\1.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\2.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\3.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\4.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\5.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\6.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\7.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\8.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\9.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\10.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\11.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\12.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\13.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\14.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\15.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\16.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\17.png",
        r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\18.png",
    ]

    images_per_page = 4
    current_page = 0

    # ฟังก์ชันสำหรับแสดงรูปภาพในหน้าปัจจุบัน
    def show_images(page):
        start_index = page * images_per_page
        end_index = min(start_index + images_per_page, len(image_files))

        # ล้างรูปภาพก่อนหน้าทั้งหมด
        for widget in rides_page.winfo_children():
            if isinstance(widget, Label) and widget != bg_label:
                widget.destroy()

        # ตำแหน่งรูปภาพ: แถวบนและแถวล่าง
        positions = [
            (150, 50), (500, 50),  # แถวบน
            (150, 275), (500, 275)  # แถวล่าง
        ]

        for i, index in enumerate(range(start_index, end_index)):
            image = PhotoImage(file=image_files[index])
            resized_image = image.subsample(2, 2)  # ปรับขนาดรูปให้เหมาะสม
            image_label = Label(rides_page, image=resized_image, border=0, bg="#5c609b")
            image_label.image = resized_image
            image_label.place(x=positions[i][0], y=positions[i][1])

    # ฟังก์ชันสำหรับเปลี่ยนไปหน้าถัดไป
    def onclick_next():
        nonlocal current_page
        total_pages = (len(image_files) + images_per_page - 1) // images_per_page
        current_page = (current_page + 1) % total_pages
        show_images(current_page)

    # ฟังก์ชันสำหรับเปลี่ยนไปหน้าก่อนหน้า
    def onclick_back():
        nonlocal current_page
        total_pages = (len(image_files) + images_per_page - 1) // images_per_page
        current_page = (current_page - 1) % total_pages
        show_images(current_page)

    # ปุ่มย้อนกลับ
    back_button_photo = PhotoImage(file=r"C:\Users\HUAWEI\Downloads\back_button-removebg-preview (1).png")
    back_button = Button(
        rides_page,
        image=back_button_photo,
        command=onclick_back,
        border=0,
        bg="#5c609b",
        activebackground="#5c609b"
    )
    back_button.image = back_button_photo  # เก็บ reference รูปภาพ
    back_button.place(x=50, y=200)  # ตำแหน่งปุ่มย้อนกลับ

    # ปุ่มถัดไป
    next_button_photo = PhotoImage(file=r"C:\Users\HUAWEI\Downloads\next_button-removebg-preview (1).png")
    next_button = Button(
        rides_page,
        image=next_button_photo,
        command=onclick_next,
        border=0,
        bg="#5c609b",
        activebackground="#5c609b"
    )
    next_button.image = next_button_photo  # เก็บ reference รูปภาพ
    next_button.place(x=850, y=200)  # ตำแหน่งปุ่มถัดไป

    # เรียกแสดงรูปภาพครั้งแรก
    show_images(current_page)

    back_button_exit = Button(rides_page, text="Back", command=lambda: back_to_main(rides_page), bg='#ffc5e2')
    back_button_exit.place(x=50, y=450)

    rides_page.protocol('WM_DELETE_WINDOW', on_close)

#=============================================หน้าข้อมูลบัตร=====================================================================

def go_to_ticket_page():
    ticket_page = Toplevel(root)
    ticket_page.title("Ticket")
    ticket_page.geometry('925x500+300+200')
    ticket_page.config(bg="#5c609b")
    ticket_page.resizable(False, False)

    img = PhotoImage(file=r"C:\Users\HUAWEI\Downloads\ticketpage.png")
    image_label = Label(ticket_page, image=img, bg="#5c609b")
    image_label.image = img  # เก็บอ้างอิงรูปเพื่อป้องกันการเก็บภาพ
    image_label.pack(expand=True)  # ให้ภาพเต็มพื้นที่

    button_frame = ctk.CTkFrame(ticket_page, fg_color='#5c609b', corner_radius=0, border_width=0)
    button_frame.place(x=260, y=432)
    create_back_button(button_frame, "<Back", lambda: back_to_main(ticket_page))

    ticket_page.protocol('WM_DELETE_WINDOW', on_close)
    # สร้างปุ่มซื้อบัตรไว้ใต้ภาพ
    buy_button = ctk.CTkButton(
        ticket_page,
        text="Purchase now!",
        corner_radius=20,
        width=100,
        height=40,
        fg_color="#FF7ED4",
        hover_color="#6420AA",
        text_color="white",
        font=('Arial', 20, 'bold'),
        command=lambda: open_purchase_window(),
        border_width=0
    )
    buy_button.place(x=380, y=450)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def back_to_ticket_page(purchase_window):
        try:
            # ซ่อนหน้าปัจจุบัน
            purchase_window.destroy()
            
            # แสดงหน้า ticket_page ที่มีอยู่
            ticket_page.deiconify()  # ทำให้หน้า ticket_page กลับมาแสดงผล
        except Exception as e:
            messagebox.showerror("Error", f"ไม่สามารถกลับไปที่หน้า Ticket ได้: {e}") 

    def validate_spinbox_input(value):
        """ฟังก์ชันตรวจสอบค่าที่ใส่ใน Spinbox"""
        if value == "":  # อนุญาตให้เป็นค่าว่าง (เมื่อผู้ใช้ลบค่าทั้งหมด)
            return True
        if value.isdigit():  # ตรวจสอบว่าเป็นตัวเลขบวกหรือไม่
            return int(value) >= 0  # ไม่อนุญาตค่าติดลบ
        return False  # ปฏิเสธค่าที่ไม่ใช่ตัวเลข

#=========================================หน้าซื้อบัตร===============================================================================        
    def open_purchase_window():
        if current_user_id is None:
            messagebox.showerror("Error", "กรุณาเข้าสู่ระบบก่อนทำการซื้อบัตร")
            return
        purchase_window = Toplevel(root)
        purchase_window.title("Purchase tickets")
        purchase_window.geometry('925x500+300+200')
        purchase_window.resizable(False, False)

        canvas = Canvas(purchase_window, width=925, height=500)
        canvas.pack(fill="both", expand=True)

        img_pay = PhotoImage(file=r"C:\Users\HUAWEI\Downloads\pay.png")
        canvas.create_image(0, 0, image=img_pay, anchor="nw")
        canvas.image = img_pay

        selected_ticket = StringVar(purchase_window)
        selected_ticket.set("Ticket type")  # ค่าเริ่มต้น

        ticket_type_frame = Frame(purchase_window, bg='#f0f0f0')

        tickets = [
            {"id": 1, "name": "บัตรผ่านประตู", "child_price": 250, "adult_price": 300},
            {"id": 2, "name": "บัตรรวมเครื่องเล่น", "child_price": 600, "adult_price": 600},
            {"id": 3, "name": "บัตรจอยฟูลวีซ่า", "child_price": 700, "adult_price": 800},
            {"id": 4, "name": "บัตรซุปเปอร์วีซ่า", "child_price": 1000, "adult_price": 1000}
        ]
        ticket_names = [ticket["name"] for ticket in tickets]
        ticket_dropdown = OptionMenu(ticket_type_frame, selected_ticket, *ticket_names)
        ticket_dropdown.pack(side=RIGHT)
        
        purchase_window.protocol('WM_DELETE_WINDOW', on_close)
        canvas.create_window(160, 150, window=ticket_type_frame)

        child_check = IntVar()
        adult_check = IntVar()

        Checkbutton(purchase_window, text="บัตรเด็ก", variable=child_check, bg='#8ab7e2').place(x=250, y=110)
        child_qty = Spinbox(purchase_window,from_=0,to=float("inf"),width=10,bg='#8ab7e2',validate='key',validatecommand=(purchase_window.register(validate_spinbox_input), '%P'))
        child_qty.place(x=250, y=150)

        Checkbutton(purchase_window, text="บัตรผู้ใหญ่", variable=adult_check, bg='#8ab7e2').place(x=250, y=180)
        adult_qty = Spinbox(purchase_window,from_=0,to=float("inf"),width=10,bg='#8ab7e2',validate='key',validatecommand=(purchase_window.register(validate_spinbox_input), '%P'))
        adult_qty.place(x=250, y=220)

        additional_ticket_check = IntVar()
        Checkbutton(purchase_window, text="บัตรประเภทอื่นเพิ่มเติม", variable=additional_ticket_check, bg='#8ab7e2').place(x=100, y=250)

        additional_ticket_frame = Frame(purchase_window, bg='#8ab7e2')
        additional_selected_ticket = StringVar(additional_ticket_frame)
        additional_selected_ticket.set("Ticket type")
        additional_child_check = IntVar()
        additional_adult_check = IntVar()
        additional_child_qty = Spinbox(additional_ticket_frame, from_=0, to=float("inf"), width=5, 
                                       bg='#8ab7e2',validate='key',validatecommand=(purchase_window.register(validate_spinbox_input), '%P'))
        additional_adult_qty = Spinbox(additional_ticket_frame, from_=0, to=float("inf"), width=5, 
                                       bg='#8ab7e2',validate='key',validatecommand=(purchase_window.register(validate_spinbox_input), '%P'))

        def back_to_purchase_page(current_page):
            current_page.destroy()  # ปิดหน้าปัจจุบัน
            open_purchase_window()

    # สร้างตัวเลือกบัตรเพิ่มเติมเมื่อเลือกเช็คบ็อกซ์
        def toggle_additional_ticket_options():
            if additional_ticket_check.get():
                if not additional_ticket_frame.winfo_ismapped():  # ตรวจสอบว่าเฟรมยังไม่ถูกแสดง
                    additional_ticket_frame.place(x=100, y=280)  # ใช้ place() แทน pack()

            # สร้างตัวเลือกประเภทบัตรเพิ่มเติม ถ้าฟอร์มยังไม่ได้ถูกสร้าง
                    if not hasattr(toggle_additional_ticket_options, 'created_widgets'):
                        Label(additional_ticket_frame, text="เลือกประเภทบัตร:", bg='#8ab7e2').pack(side=LEFT, padx=5)
                        additional_ticket_dropdown = OptionMenu(additional_ticket_frame, additional_selected_ticket, *ticket_names)
                        additional_ticket_dropdown.pack(side=LEFT)

                        Checkbutton(additional_ticket_frame, text="บัตรเด็ก", variable=additional_child_check, bg='#8ab7e2').pack(pady=5)
                        additional_child_qty.pack()

                        Checkbutton(additional_ticket_frame, text="บัตรผู้ใหญ่", variable=additional_adult_check, bg='#8ab7e2').pack(pady=5)
                        additional_adult_qty.pack()

                        toggle_additional_ticket_options.created_widgets = True
            else:
                additional_ticket_frame.place_forget() 

        additional_ticket_check.trace("w", lambda *args: toggle_additional_ticket_options())

    # เลือกวัน
        def show_date(event):
            selected_date_str = cal.get_date()  # วันที่ที่เลือกจะเป็น string ในรูปแบบ "mm/dd/yy"
            
            try:
                # แปลง selected_date เป็น datetime โดยใช้รูปแบบ "mm/dd/yy"
                selected_date = datetime.strptime(selected_date_str, "%m/%d/%y")
                
                # แปลง selected_date ให้เป็นรูปแบบ "yyyy-mm-dd"
                formatted_date = selected_date.strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "วันที่ไม่ถูกต้อง")
                return False
            
            # แสดงวันที่ที่เลือกใน label
            date_label.config(text=f"วันที่เลือก: {formatted_date}")

            if not selected_date_str or selected_date_str == "":
                messagebox.showerror("Error", "กรุณาเลือกวันที่")
                return False

            # ตรวจสอบว่าเป็นวันที่ในอนาคต
            current_date = datetime.now()  # วันที่ปัจจุบัน
            if selected_date < current_date:
                messagebox.showerror("Error", "ไม่สามารถเลือกวันที่ที่ผ่านไปแล้วได้")
                return False
            
            if selected_date.date() == current_date.date():
                messagebox.showerror("Error", "ขออภัย ต้องจองล่วงหน้า")
                return False

            # คืนค่าที่ถูกแปลงเป็น "yyyy-mm-dd"
            return formatted_date

        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        current_day = current_date.day

        cal = Calendar(purchase_window, selectmode='day', year=current_year, month=current_month, day=current_day)
        cal.place(x=520, y=150)

        date_label = tk.Label(purchase_window, text="วันที่เลือก: ", bg='#8ab7e2')
        date_label.place(x=520, y=350)

        cal.bind("<<CalendarSelected>>", show_date)
    # open_purchase_window.()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # ฟังก์ชันคำนวณราคา
        def calculate_total():
            selected_ticket_name = selected_ticket.get()
            if selected_ticket_name == "Ticket type":
                messagebox.showerror("Error", "กรุณาเลือกประเภทบัตร")
                return

            selected_ticket_data = next(ticket for ticket in tickets if ticket["name"] == selected_ticket_name)
        
            child_count = int(child_qty.get()) if child_check.get() else 0
            adult_count = int(adult_qty.get()) if adult_check.get() else 0
            total_price = (child_count * selected_ticket_data["child_price"]) + (adult_count * selected_ticket_data["adult_price"])

        # คำนวณราคาบัตรเพิ่มเติมถ้าเลือกเช็คบ็อกซ์
            if additional_ticket_check.get():
                additional_ticket_name = additional_selected_ticket.get()
                if additional_ticket_name != "Ticket type":
                    additional_ticket_data = next(ticket for ticket in tickets if ticket["name"] == additional_ticket_name)
                    additional_child_count = int(additional_child_qty.get()) if additional_child_check.get() else 0
                    additional_adult_count = int(additional_adult_qty.get()) if additional_adult_check.get() else 0
                    total_price += (additional_child_count * additional_ticket_data["child_price"]) + (additional_adult_count * additional_ticket_data["adult_price"])
            
            formatted_price = f"{total_price:,}"
            total_label.config(text=f"ราคารวม : {formatted_price} บาท")

            global is_price_calculated
            is_price_calculated = True
        # ปุ่มคำนวณราคา
        total_button = Button(purchase_window, text="คำนวณราคา", command=calculate_total, bg='#ffc5e2')
        total_button.place(x=100, y=450)

        total_label = Label(purchase_window, text="ราคารวม : 0 บาท", bg='#5c609b', fg='white')
        total_label.place(x=200, y=450)

        back_button = Button(purchase_window, text="<Back", command=lambda: back_to_ticket_page(purchase_window), bg='#ffc5e2')
        back_button.place(x=600, y=450)

#===============================หน้ากรอกข้อมูลส่วนตัว==========================================================

        def open_info_window(purchase_window, total_price, selected_ticket_data, child_count, adult_count, additional_ticket_name, additional_child_count, additional_adult_count):
            # ซ่อนหน้าต่างการซื้อบัตร
            purchase_window.withdraw()
            # สร้างหน้าต่างกรอกข้อมูลส่วนตัว
            info_window = Toplevel(root)
            info_window.title("กรอกข้อมูลส่วนตัว")
            info_window.geometry('925x500+300+200')
            info_window.config(bg="#5c609b")
            
            bgImage = ImageTk.PhotoImage(file=r"C:\Users\HUAWEI\Downloads\amusement (5).png")
            image_label = Label(info_window, image=bgImage, bg="#5c609b")
            image_label.image = bgImage  # เก็บอ้างอิงรูปเพื่อป้องกันการเก็บภาพ
            image_label.pack(expand=True)

            frame = Frame(info_window, width=350, height=350, bg="#5c609b")
            frame.place(x=480, y=70)

            heading = Label(frame, text='Personal Information', fg='#ffc5e2', bg='#5c609b', font=('Microsoft YaHei UI Light', 23, 'bold'))
            heading.place(x=30, y=5)

            def on_enter_name(e):
                if name.get() == 'Name':
                    name.delete(0, 'end')

            def on_leave_name(e):
                if name.get() == '':
                    name.insert(0, 'Name')

            name = Entry(frame, width=25, fg='white', border=0, bg='#5c609b', font=('Microsoft YaHei UI Light', 11))
            name.place(x=30, y=80)
            name.insert(0, 'Name')
            name.bind('<FocusIn>', on_enter_name)
            name.bind('<FocusOut>', on_leave_name)

            Frame(frame, width=295, height=2, bg='white').place(x=25, y=107)

            def on_enter_tel(e):
                if tel.get() == 'Phone number':
                    tel.delete(0, 'end')

            def on_leave_tel(e):
                if tel.get() == '':
                    tel.insert(0, 'Phone number')

            tel = Entry(frame, width=25, fg='white', border=0, bg='#5c609b', font=('Microsoft YaHei UI Light', 11))
            tel.place(x=30, y=150)
            tel.insert(0, 'Phone number')
            tel.bind('<FocusIn>', on_enter_tel)
            tel.bind('<FocusOut>', on_leave_tel)

            Frame(frame, width=295, height=2, bg='white').place(x=25, y=177)

            def on_enter_email(e):
                if email.get() == 'Email':
                    email.delete(0, 'end')

            def on_leave_email(e):
                if email.get() == '':
                    email.insert(0, 'Email')

            email = Entry(frame, width=25, fg='white', border=0, bg='#5c609b', font=('Microsoft YaHei UI Light', 11))
            email.place(x=30, y=220)
            email.insert(0, 'Email')
            email.bind('<FocusIn>', on_enter_email)
            email.bind('<FocusOut>', on_leave_email)

            Frame(frame, width=295, height=2, bg='white').place(x=25, y=247)

            def confirm_info(name, email, tel):
                name_enter = name.strip()
                email_enter = email.strip()
                phone_enter = tel.strip()

                if name_enter in ['Name', ''] or phone_enter in ['Phone number', ''] or email_enter in ['Email', '']:
                    messagebox.showerror("Error", "กรุณากรอกข้อมูลให้ครบถ้วน")
                    return

                if not name_enter or len(name_enter) > 100:
                    messagebox.showerror("Error", "กรุณากรอกชื่อ-สกุลที่ถูกต้อง (ไม่เกิน 100 ตัวอักษร)")
                    return

        # เบอร์โทรศัพท์: ต้องเป็นตัวเลข 10 หลัก
                if not (phone_enter.isdigit() and len(phone_enter) == 10):
                    messagebox.showerror("Error", "กรุณากรอกเบอร์โทรศัพท์ให้ถูกต้อง (10 หลักและเป็นตัวเลขเท่านั้น)")
                    return

                # อีเมล: ตรวจสอบรูปแบบด้วย regex
                import re
                email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                if not re.match(email_pattern, email):
                    messagebox.showerror("Error", "กรุณากรอกอีเมลให้ถูกต้อง")
                    return

                confirm = messagebox.askyesno(
                    "ยืนยันข้อมูล",
                    f"โปรดตรวจสอบข้อมูลของคุณ :\n\n"
                    f"ชื่อ-สกุล : {name_enter}\n"
                    f"เบอร์โทรศัพท์ : {phone_enter}\n"
                    f"Email : {email_enter}\n\n"
                    f"ข้อมูลถูกต้องหรือไม่ ?"
                )
                if not confirm:
                    return
                
#================บันทึกข้อมูลส่วนตัวลงในฐานข้อมูล==========================================

                connection = sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db")
                cursor = connection.cursor()

                try:
                    cursor.execute("""
                        UPDATE users 
                        SET name=?, email=?, phone_number=? 
                        WHERE user_id=?
                    """, (name_enter, email_enter, phone_enter, current_user_id))
                    connection.commit()
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"ไม่สามารถบันทึกข้อมูลได้: {e}")
                finally:
                    connection.close()

                # ปิดหน้ากรอกข้อมูลส่วนตัว
                info_window.destroy()

                # เรียกหน้าสรุปรายการ
                proceed_to_summary(total_price, selected_ticket_data, child_count, adult_count, additional_ticket_name, additional_child_count, additional_adult_count)

            button_frame = ctk.CTkFrame(info_window, fg_color='#5c609b', corner_radius=0, border_width=0)
            button_frame.place(x=540, y=380)
            create_back_button(button_frame, "<Back", lambda: back_to_purchase_page(info_window))

            confirm_button = ctk.CTkButton(
                info_window,
                text="Next>",
                corner_radius=20,
                width=100,
                height=40,
                fg_color="#FF7ED4",
                hover_color="#6420AA",
                text_color="white",
                font=('Arial', 20, 'bold'),
                command=lambda: confirm_info(name.get(),email.get(),tel.get()),
                border_width=0
            )
            confirm_button.place(x=650, y=400)

            info_window.protocol('WM_DELETE_WINDOW', on_close)

#==========================ตรวจสอบว่าเลือกอะไรครบมั้ย===================================

        def purchase_check():
            global current_user_id 

            if current_user_id is None:
                messagebox.showerror("Error", "กรุณาเข้าสู่ระบบก่อนทำการซื้อบัตร")
                return False

            # ตรวจสอบว่ามีการเลือกประเภทบัตรหลักหรือไม่
            if selected_ticket.get() == "เลือกบัตร" or not (child_check.get() or adult_check.get()):
                messagebox.showerror("Error", "กรุณาเลือกประเภทบัตรและจำนวนบัตร")
                return False

            child_count = int(child_qty.get()) if child_check.get() else 0
            adult_count = int(adult_qty.get()) if adult_check.get() else 0

            # ตรวจสอบจำนวนบัตรหลัก
            if child_check.get() and child_count == 0:
                messagebox.showerror("Error", "กรุณาระบุจำนวนบัตรเด็ก")
                return False
            if adult_check.get() and adult_count == 0:
                messagebox.showerror("Error", "กรุณาระบุจำนวนบัตรผู้ใหญ่")
                return False

            selected_ticket_name = selected_ticket.get()  # ใช้ชื่อบัตรแทน ID
            additional_ticket_name = "เลือกบัตร"

            if additional_ticket_check.get():
                additional_ticket_name = additional_selected_ticket.get()
                if additional_ticket_name == "เลือกบัตร":
                    messagebox.showerror("Error", "กรุณาเลือกประเภทบัตรเพิ่มเติม")
                    return False

                if additional_ticket_name == selected_ticket_name:
                    messagebox.showerror("Error", "ประเภทบัตรเพิ่มเติมต้องไม่ซ้ำกับประเภทบัตรหลัก")
                    return False

                additional_child_count = int(additional_child_qty.get()) if additional_child_check.get() else 0
                additional_adult_count = int(additional_adult_qty.get()) if additional_adult_check.get() else 0

                if additional_child_check.get() and additional_child_count == 0:
                    messagebox.showerror("Error", "กรุณากรอกจำนวนบัตรเด็กเพิ่มเติม")
                    return False
                if additional_adult_check.get() and additional_adult_count == 0:
                    messagebox.showerror("Error", "กรุณากรอกจำนวนบัตรผู้ใหญ่เพิ่มเติม")
                    return False
            else:
                additional_child_count = 0
                additional_adult_count = 0

            number_of_tickets = child_count + adult_count + additional_child_count + additional_adult_count

            # ดึงข้อมูลบัตรหลักเพื่อคำนวณราคา
            selected_ticket_data = next(ticket for ticket in tickets if ticket["name"] == selected_ticket_name)
            total_price = (child_count * selected_ticket_data["child_price"]) + (adult_count * selected_ticket_data["adult_price"])

            ticket_date = cal.get_date()
            if additional_ticket_check.get() and additional_ticket_name != "เลือกบัตร":
                additional_ticket_data = next(ticket for ticket in tickets if ticket["name"] == additional_ticket_name)
                total_price += (additional_child_count * additional_ticket_data["child_price"]) + (additional_adult_count * additional_ticket_data["adult_price"])

            # บันทึกข้อมูลการซื้อโดยใช้ชื่อบัตรแทนไอดี
            if save_purchase(current_user_id, ticket_date, selected_ticket_name, child_count, adult_count, additional_ticket_name, additional_child_count, additional_adult_count, number_of_tickets, total_price):
                # เปิดหน้าต่างข้อมูลการซื้อ
                open_info_window(purchase_window, total_price, selected_ticket_data, child_count, adult_count, additional_ticket_name, additional_child_count, additional_adult_count)
            else:
                messagebox.showerror("Error", "การซื้อบัตรไม่สำเร็จ")
                return False

    # ปุ่มยืนยันการซื้อ
        purchase_button = Button(purchase_window, text="Next>", command=purchase_check, bg='#ffc5e2')
        purchase_button.place(x=650, y=450)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        def proceed_to_summary(total_price, ticket_data, child_count, adult_count, additional_ticket_name, additional_child_count, additional_adult_count):
            ticket_type = ticket_data["name"]
            child_qty_value = child_count
            adult_qty_value = adult_count
            additional_ticket_type = additional_ticket_name
            additional_child_qty_value = additional_child_count
            additional_adult_qty_value = additional_adult_count
            selected_date = cal.get_date()

            summary_window(ticket_type, child_qty_value, adult_qty_value, additional_ticket_type, additional_child_qty_value, additional_adult_qty_value, selected_date, total_price)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ฟังก์ชันหน้าต่างสรุปการซื้อ
        def summary_window(ticket_type, child_qty, adult_qty, additional_ticket_type, additional_child_qty_value, additional_adult_qty_value, selected_date, total_price):
            summary_window = Toplevel(root)
            summary_window.title("Summary")
            summary_window.geometry('925x500+300+200')
            summary_window.resizable(False, False)

            canvas = Canvas(summary_window, width=925, height=500)
            canvas.pack(fill="both", expand=True)

            img_sum = PhotoImage(file=r"C:\Users\HUAWEI\Downloads\amusement (1).png")
            canvas.create_image(0, 0, image=img_sum, anchor="nw")
            canvas.image = img_sum
            summary_window.protocol('WM_DELETE_WINDOW', on_close)

            formatted_total_price = f"{total_price:,}"
    # ข้อมูลที่แสดงในหน้าสรุป
            y_position = 140
            Label(summary_window, text=f"วันที่จอง : {selected_date}", bg='#8ab7e2').place(x=180, y=y_position)
            y_position += 30
            Label(summary_window, text=f"ประเภทบัตร : {ticket_type}", bg='#8ab7e2').place(x=180, y=y_position)
            y_position += 30

            if child_qty > 0:
                Label(summary_window, text=f"บัตรเด็ก : {child_qty} ใบ", bg='#8ab7e2').place(x=200, y=y_position)
                y_position += 30
            if adult_qty > 0:
                Label(summary_window, text=f"บัตรผู้ใหญ่ : {adult_qty} ใบ", bg='#8ab7e2').place(x=200, y=y_position)
                y_position += 30

           # ตรวจสอบว่ามีการเลือกบัตรเพิ่มเติมและจำนวนบัตรเด็กหรือผู้ใหญ่เพิ่มเติมมากกว่า 0
            if additional_ticket_type and additional_ticket_type != "เลือกบัตร" and (additional_child_qty_value > 0 or additional_adult_qty_value > 0):
                Label(summary_window, text=f"บัตรเพิ่มเติม : {additional_ticket_type}", bg='#8ab7e2').place(x=180, y=y_position)
                y_position += 30
                if additional_child_qty_value > 0:
                    Label(summary_window, text=f"บัตรเด็ก : {additional_child_qty_value} ใบ", bg='#8ab7e2').place(x=200, y=y_position)
                    y_position += 30
                if additional_adult_qty_value > 0:
                    Label(summary_window, text=f"บัตรผู้ใหญ่ : {additional_adult_qty_value} ใบ", bg='#8ab7e2').place(x=200, y=y_position)
                    y_position += 30

            Label(summary_window, text=f"ราคารวม : {formatted_total_price} บาท", bg='#8ab7e2').place(x=180, y=380)
            # y_position += 30

            Label(summary_window, text="แนบสลิปการโอน", bg='#8ab7e2').place(x=500, y=380)

            # สร้าง StringVar สำหรับเก็บชื่อไฟล์
            file_path_var = tk.StringVar()
            file_path_var.set("เลือกไฟล์")  # ข้อความเริ่มต้นที่แสดงในปุ่ม
            upload_button = tk.Button(summary_window, textvariable=file_path_var, command=lambda: upload_file(root, None, file_path_var))
            upload_button.place(x=580, y=380)

            # ฟังก์ชันยกเลิกการทำรายการ
            def cancel_order():
                # ยืนยันการยกเลิก
                confirm = messagebox.askyesno("ยืนยัน", "คุณแน่ใจหรือไม่ว่าต้องการยกเลิกการทำรายการนี้?")
                if not confirm:
                    return  # หากผู้ใช้เลือก "ไม่" ให้ยกเลิกการดำเนินการ

                # เชื่อมต่อฐานข้อมูล
                connection = sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db")
                cursor = connection.cursor()

                try:
                    # ลบข้อมูลส่วนตัวของผู้ใช้ออกจากตาราง users
                    cursor.execute("""
                        UPDATE users
                        SET name = NULL, email = NULL, phone_number = NULL
                        WHERE user_id = ?
                    """, (current_user_id,))  # current_user_id คือตัวแปรที่เก็บ id ของผู้ใช้งานปัจจุบัน

                    connection.commit()  # ยืนยันการเปลี่ยนแปลง

                    # แจ้งเตือนผู้ใช้ว่าลบข้อมูลสำเร็จ
                    messagebox.showinfo("สำเร็จ", "ข้อมูลส่วนตัวของคุณถูกลบเรียบร้อยแล้ว")
                except sqlite3.Error as e:
                    # แสดงข้อความแจ้งเตือนหากเกิดข้อผิดพลาด
                    messagebox.showerror("Database Error", f"ไม่สามารถลบข้อมูลได้: {e}")
                finally:
                    connection.close()

                # ปิดหน้าต่าง summary_window
                summary_window.destroy()
           
            def confirm_payment(summary_window, total_price, file_path_var):
                # ตรวจสอบว่าผู้ใช้ได้แนบไฟล์สลิปหรือยัง
                if not hasattr(file_path_var, "uploaded_file") or not file_path_var.uploaded_file:
                    messagebox.showwarning("ยังไม่ได้แนบไฟล์", "กรุณาแนบไฟล์สลิปก่อนยืนยันการชำระเงิน")
                    return

                payment_proof_path = file_path_var.uploaded_file  # ใช้ file_path_var เพื่อเก็บที่อยู่ของไฟล์

                try:

                    # เก็บข้อมูลการชำระเงินในฐานข้อมูล
                    complete_transaction(summary_window, total_price, payment_proof_path)
                    # save_payment_proof_to_db(user_id, payment_proof_path, total_price_value)
                    # แจ้งเตือนการชำระเงินสำเร็จ
                    messagebox.showinfo("ชำระเงินสำเร็จ", "การชำระเงินของคุณได้รับการยืนยันแล้ว!")
                    # ปิดหน้าต่างสรุป
                    summary_window.destroy()
                except Exception as e:
                    # หากเกิดข้อผิดพลาด แจ้งเตือนข้อผิดพลาด
                    messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {e}")

            Button(summary_window, text="Cancel", bg="#aa2135", fg="white", font=("Arial", 12, "bold"), command=cancel_order).place(x=630, y=450)
            Button(
                summary_window,
                text="Confirm",
                bg="#004aad",
                fg="white",
                font=("Arial", 12, "bold"),
                command=lambda: [confirm_payment(summary_window, total_price, file_path_var), show_order_bill_popup(total_price,current_user_id)]
            ).place(x=730, y=450)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        def upload_file(summary_window, total_price, file_path_var):
    # เปิด dialog เลือกไฟล์
            file_path = filedialog.askopenfilename(
                title="เลือกไฟล์",
                filetypes=[("Image files", ".jpg;.jpeg;*.png"), ("PDF files", ".pdf"), ("All files", ".*")]
            )
            if file_path:
                file_path_var.uploaded_file = file_path
                file_name = file_path.split("/")[-1]  # ดึงชื่อไฟล์จากเส้นทาง
                file_path_var.set(file_name)  # อัปเดตข้อความของปุ่ม
                
                # เก็บเส้นทางไฟล์เพื่อใช้งานในที่อื่น
                upload_file.uploaded_file = file_path
                
                # แปลงไฟล์เป็นไบนารี (ไบต์สตรีม) และเปลี่ยนชนิดไฟล์เป็น jpg, jpeg, png
                with open(file_path, "rb") as file:
                    file_binary_data = file.read()
                    
                # เปลี่ยนชนิดไฟล์ตามที่ต้องการ
                if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                    # สามารถแปลงเป็นรูปแบบอื่น ๆ ตามต้องการได้ เช่น PNG to JPEG หรือ vice versa
                    file_path_var.uploaded_file_data = file_binary_data  # เก็บข้อมูลไฟล์ในรูปแบบไบนารีในที่ที่ต้องการ
                else:
                    messagebox.showerror("Error", "ไฟล์ที่เลือกไม่ใช่ jpg, jpeg หรือ png")
                    return False
            else:
                file_path_var.set("เลือกไฟล์")  # ถ้าไม่มีไฟล์ให้แสดงข้อความนี้
                upload_file.uploaded_file = None  # ถ้าไม่มีไฟล์ให้ล้างค่าที่เก็บไว้

        def complete_transaction(payment_window, total_price, payment_proof_path):
            user_id = current_user_id
            ticket_date = cal.get_date()
            selected_ticket_name = selected_ticket.get()  # ใช้ชื่อบัตรแทน ID
            child_count = int(child_qty.get()) if child_check.get() else 0
            adult_count = int(adult_qty.get()) if adult_check.get() else 0
            additional_ticket_name = additional_selected_ticket.get()
            additional_child_count = int(additional_child_qty.get()) if additional_child_check.get() else 0
            additional_adult_count = int(additional_adult_qty.get()) if additional_adult_check.get() else 0
            number_of_tickets = child_count + adult_count + additional_child_count + additional_adult_count

            check_list = [
                user_id, ticket_date, selected_ticket_name, child_count, adult_count,
                additional_ticket_name, additional_child_count, additional_adult_count, number_of_tickets
            ]

            if all(check_list):  # เช็กว่าค่าทั้งหมดไม่เป็น None หรือว่าง
                save_payment_proof_to_db(user_id, payment_proof_path, total_price)
                payment_window.destroy()
                messagebox.showinfo("สำเร็จ", "บันทึกสลิปสำเร็จ!")

# ฟังก์ชันบันทึกข้อมูลการชำระเงินในฐานข้อมูล
        def save_payment_proof_to_db(user_id, payment_proof_path, total_price):
            connection = sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db")
            cursor = connection.cursor()
            upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO payment_proof2 (user_id, file_path, total_price, upload_time) VALUES (?, ?, ?, ?)",
                        (user_id, payment_proof_path, total_price, upload_time))

            connection.commit()
            connection.close()

#============================บันทึกข้อมูลการซื้อลงฐานข้อมูล===========================================

        def save_purchase(user_id, ticket_date, selected_ticket_name, child_qty, adult_qty, 
                  additional_ticket_name, additional_child_qty, additional_adult_qty, 
                  number_of_tickets, total_price):
            if user_id is None:
                messagebox.showerror("Error", "กรุณาเข้าสู่ระบบก่อนทำการซื้อบัตร")
                return False 

            conn = sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db")
            cursor = conn.cursor()

            try:
                # ดึงวันที่ปัจจุบันเป็นวันซื้อบัตร
                purchase_date = datetime.now().strftime("%Y-%m-%d")

                # บันทึกข้อมูลการซื้อบัตรลงในฐานข้อมูล
                cursor.execute("""
                    INSERT INTO tickets_new 
                    (user_id, ticket_date, purchase_date, ticket_name, child_qty, adult_qty, 
                    additional_ticket_name, additional_child_qty, additional_adult_qty, 
                    total_qty, total_price) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, ticket_date, purchase_date, selected_ticket_name, child_qty, adult_qty, 
                    additional_ticket_name, additional_child_qty, additional_adult_qty, 
                    number_of_tickets, total_price))

                conn.commit()
                return True
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"การซื้อบัตรล้มเหลว: {str(e)}")
                return False
            finally:
                conn.close()

#========================Bill==================================================================

        def show_order_bill_popup(total_price, current_user_id):
            # global current_user_id
            if current_user_id is None:
                messagebox.showerror("Error", "กรุณาเข้าสู่ระบบก่อนดูบิล")
                return
        # สร้างหน้าต่างป๊อปอัปใหม่
            bill_window = tk.Toplevel(root)
            bill_window.title("บิลรายการสั่งซื้อ")
            bill_window.geometry("400x600")  # ปรับขนาดได้ตามต้องการ

            # โหลดรูปภาพพื้นหลังและแสดง
            background_image_path = r"C:\Users\HUAWEI\Downloads\Thank you.png"  # ระบุพาธของรูปพื้นหลัง
            if not os.path.exists(background_image_path):
                messagebox.showerror("Error", "ไม่พบไฟล์รูปภาพที่กำหนด")
                return
            bg_image = Image.open(background_image_path)
            bg_image = bg_image.resize((400,600), Image.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_image)

            bg_label = tk.Label(bill_window, image=bg_photo)
            bg_label.image = bg_photo  # เก็บอ้างอิงรูปภาพ
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            conn = sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db")
            c = conn.cursor()

            c.execute("SELECT name FROM users WHERE user_id = ?", (current_user_id,))
            user_data = c.fetchone()
            if user_data:
                name = user_data
            else:
                name = "ไม่พบข้อมูล", "ไม่พบข้อมูล"
            # ดึงข้อมูลบัตรจากฐานข้อมูล
            c.execute("""
                SELECT ticket_date, ticket_name, child_qty, adult_qty, additional_ticket_name, additional_child_qty, additional_adult_qty, total_qty, total_price
                FROM tickets_new
                WHERE user_id = ?
            """, (current_user_id,))
            ticket_data = c.fetchone()

            if ticket_data:
                ticket_date, ticket_name, child_qty, adult_qty, additional_ticket_name, additional_child_qty, additional_adult_qty, total_qty, total_price = ticket_data
                ticket_name = ticket_name if ticket_name else "บัตรไม่ทราบประเภท"
                additional_ticket_name = additional_ticket_name if additional_ticket_name else "ไม่มีบัตรเพิ่มเติม"
            else:
                ticket_date, ticket_name, child_qty, adult_qty, additional_ticket_name, additional_child_qty, additional_adult_qty, total_qty, total_price = (
                    "-", "-", 0, 0, "-", 0, 0, 0, 0)
                
            conn.close()

            bill_text = f"""
            รายการสั่งซื้อ
            ------------------------------
            ชื่อจริง : {name}
            วันที่ : {ticket_date}
            ประเภทบัตรหลัก : {ticket_name}
            """
            if child_qty > 0:
                bill_text += f"บัตรเด็ก : {child_qty} ใบ\n"
            if adult_qty > 0:
                bill_text += f"            บัตรผู้ใหญ่ : {adult_qty} ใบ\n"
            if additional_ticket_name != "-":
                bill_text += f"            ประเภทบัตรเสริม : {additional_ticket_name}\n"
                if additional_child_qty > 0:
                    bill_text += f"            บัตรเสริมเด็ก : {additional_child_qty} ใบ\n"
                if additional_adult_qty > 0:
                    bill_text += f"            บัตรเสริมผู้ใหญ่ : {additional_adult_qty} ใบ\n"

            bill_text += f"""
            ------------------------------
            จำนวนบัตรทั้งหมด : {total_qty} ใบ
            ราคารวมทั้งหมด : {total_price} บาท
            ------------------------------
            ขอบคุณที่ใช้บริการ
            """
            # เพิ่มข้อความบิลลงในหน้าต่าง
            bill_label = tk.Label(bill_window, text=bill_text, bg="white", fg="black", justify="left")
            bill_label.pack(pady=150)

#########################################################################################################################################################################

def go_to_info_page():
    info_page = Toplevel(root)
    info_page.title("personal info")
    info_page.geometry('925x500+300+200')
    info_page.resizable(False, False)

    img_info = PhotoImage(file=r"C:\Users\HUAWEI\Downloads\amusement (7).png")
    image_label = Label(info_page, image=img_info, bg="#5c609b")
    image_label.image = img_info  # เก็บอ้างอิงรูปเพื่อป้องกันการเก็บภาพ
    image_label.pack(expand=True)

    def load_user_info():
        try:
            with sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT name, phone_number, email
                    FROM users
                    WHERE user_id = ?
                """, (current_user_id,))
                user_info = cursor.fetchone()

                if user_info:
                    name, phone_number, email = user_info
                    # ตรวจสอบเบอร์โทรศัพท์และเติม 0 ด้านหน้า
                    phone_number = f"{int(phone_number):0>10}"  # เติม 0 ด้านหน้าให้ครบ 10 หลัก
                    return (name, phone_number, email)
                return ("-", "-", "-")
        except:
            return ("-", "-", "-")
        
    def load_ticket_info():
        try:
            with sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT ticket_date, ticket_name, child_qty, adult_qty, additional_ticket_name, additional_child_qty, additional_adult_qty, total_qty, total_price
                    FROM tickets_new
                               
                    WHERE user_id = ?
                """, (current_user_id,))
                user_info = cursor.fetchall()
                if not user_info:
                    return []

                # คืนค่าข้อมูลที่ดึงมาได้
                return user_info
        except:
            # คืนค่ารายการว่างในกรณีเกิดข้อผิดพลาด
            return []

    user_info = load_user_info()
    if user_info:
        name, phone, email = user_info
        Label(info_page, text=f"{name}", bg="#fcf3f1", fg="black").place(x=150, y=110)
        Label(info_page, text=f"{phone}", bg="#fcf3f1", fg="black").place(x=570, y=170)
        Label(info_page, text=f"{email}", bg="#fcf3f1", fg="black").place(x=150, y=170)

    ticket_items = load_ticket_info()

    if ticket_items:
        y_position = 250  # ตั้งตำแหน่งเริ่มต้นในการแสดงข้อมูล
        item = ticket_items[0]
        ticket_date = item[0] if item[0] else "-"
        ticket_name = item[1] if item[1] else "-"
        child_qty = item[2] if item[2] else 0
        adult_qty = item[3] if item[3] else 0
        additional_ticket_name = item[4] if item[4] else "-"
        additional_child_qty = item[5] if item[5] else 0
        additional_adult_qty = item[6] if item[6] else 0
        total_qty = item[7] if item[7] else 0
        total_price = item[8] if item[8] else 0

        try:
            total_price = float(total_price)
        except ValueError:
            total_price = 0.0

        formatted_total_price = f"{total_price:,.2f}"

        Label(info_page, text=f"วันที่จอง : {ticket_date}", bg="white", fg="black").place(x=50, y=y_position)
        Label(info_page, text=f"{ticket_name}", bg="white", fg="black").place(x=50, y=y_position + 20)
        Label(info_page, text=f"เด็ก : {child_qty} ใบ", bg="white", fg="black").place(x=140, y=y_position + 20)
        Label(info_page, text=f"ผู้ใหญ่ : {adult_qty} ใบ", bg="white", fg="black").place(x=140, y=y_position + 40)

        if additional_ticket_name != "-":
            Label(info_page, text=f"{additional_ticket_name}", bg="white", fg="black").place(x=50, y=y_position + 60)
            Label(info_page, text=f"เด็ก : {additional_child_qty} ใบ", bg="white", fg="black").place(x=140, y=y_position + 60)
            Label(info_page, text=f"ผู้ใหญ่ : {additional_adult_qty} ใบ", bg="white", fg="black").place(x=140, y=y_position + 80)

        Label(info_page, text=f"จำนวนรวม : {total_qty} ใบ", bg="white", fg="black").place(x=50, y=y_position + 100)
        Label(info_page, text=f"ราคารวม : {formatted_total_price} บาท", bg="white", fg="black").place(x=50, y=y_position + 120)
        y_position += 140  # เพิ่มตำแหน่ง y สำหรับข้อมูลถัดไป
    else:
        Label(info_page, text="ไม่มีข้อมูลการซื้อ",  bg="white", fg="black").place(x=80, y=250)

    back_button = Button(info_page, text="Back", command=lambda: back_to_main(info_page), bg='#ffc5e2')
    back_button.place(x=650, y=450)
    info_page.protocol('WM_DELETE_WINDOW', on_close)

################################################################################################################################################################################

def go_to_contact_page():
    contact_page = Toplevel(root)
    contact_page.title("contact")
    contact_page.geometry('925x500+300+200')
    contact_page.resizable(False, False)
    # Label(contact_page, text="Contact us", font=('Harrington', 30)).pack(pady=20)
    img_tel = PhotoImage(file=r"C:\Users\HUAWEI\Downloads\amusement (6).png")
    image_label = Label(contact_page, image=img_tel, bg="#5c609b")
    image_label.image = img_tel  # เก็บอ้างอิงรูปเพื่อป้องกันการเก็บภาพ
    image_label.pack(expand=True)
    back_button = Button(contact_page, text="Back", command=lambda: back_to_main(contact_page), bg='#ffc5e2')
    back_button.place(x=450, y=450)
    contact_page.protocol('WM_DELETE_WINDOW', on_close)

#########################################################################################################################################################################

def signup_command():
    window = Toplevel(root)
    window.title('Joyful Kingdom')
    window.geometry('925x500+300+200')
    window.configure(bg='#fff')
    window.resizable(False, False)

    def signup():
        username = user.get()
        password = code.get()
        confirm_password = comfirm_code.get()

        username = username.strip()
        if not re.match("^[A-Za-z0-9 ]{5,20}$", username):
            messagebox.showerror('Error', 'Username must be 5-20 characters and can contain only letters, numbers, and spaces')
            return


        if len(password) < 8 :
            messagebox.showerror('Error', 'Password must be at least 8 characters')
            return  # หยุดการทำงานของฟังก์ชันหากไม่ผ่านเงื่อนไข

        if password == confirm_password:
            try:
                # เชื่อมต่อกับฐานข้อมูล
                conn = sqlite3.connect(r"C:\Users\HUAWEI\OneDrive\Desktop\MyData\amusement_park.db")
                cursor = conn.cursor()
                
                # ตรวจสอบว่าผู้ใช้มีอยู่แล้วหรือไม่
                cursor.execute("SELECT * FROM users WHERE username=?", (username,))
                result = cursor.fetchone()

                if result:
                    messagebox.showerror('Error', 'Username already exists')
                else:
                    # เพิ่มข้อมูลผู้ใช้ลงในฐานข้อมูล
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                    conn.commit()
                    
                    user_id = cursor.lastrowid
                    messagebox.showinfo('Sign up', f'Successfully signed up!')
                
                # เก็บ user_id นี้ไว้ในตัวแปร global
                    global current_user_id
                    current_user_id = user_id  # เก็บค่า user_id เพื่อใช้งานในโปรแกรม
            except sqlite3.Error as e:
                messagebox.showerror('Database Error', f"An error occurred: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror('Invalid', 'Both passwords should match')

    img = PhotoImage(file=r"C:\Users\HUAWEI\Downloads\login.png")
    Label(window, image=img, bg='white').place(x=50, y=50)

    frame = Frame(window, width=350, height=350, bg="white")
    frame.place(x=480, y=70)

    heading = Label(frame, text='Sign up', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=100, y=5)

    def on_enter(e):
        user.delete(0, 'end')

    def on_leave(e):
        if user.get() == '':
            user.insert(0, 'Username')

    user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    def on_enter(e):
        code.delete(0, 'end')

    def on_leave(e):
        if code.get() == '':
            code.insert(0, 'Password')

    code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    code.place(x=30, y=150)
    code.insert(0, 'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    def on_enter(e):
        comfirm_code.delete(0, 'end')

    def on_leave(e):
        if comfirm_code.get() == '':
            comfirm_code.insert(0, 'Confirm Password')

    comfirm_code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    comfirm_code.place(x=30, y=220)
    comfirm_code.insert(0, 'Confirm Password')
    comfirm_code.bind('<FocusIn>', on_enter)
    comfirm_code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

    Button(frame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white', border=0, command=signup).place(x=35, y=280)

    window.mainloop()

img = PhotoImage(file=r"C:\Users\HUAWEI\Downloads\sign in.png")
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Arial', 23, 'bold'))
heading.place(x=100, y=5)

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    if user.get() == '':
        user.insert(0, 'Username')

user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

def on_enter(e):
    code.delete(0, 'end')

def on_leave(e):
    if code.get() == '':
        code.insert(0, 'Password')

code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=204)
label = Label(frame, text="Don't Have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75, y=270)

sign_up = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=signup_command)
sign_up.place(x=215, y=270)

root.mainloop()