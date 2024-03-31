import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

 
connection = mysql.connector.connect(host='localhost', user='root', password='', port='3307', database='libraryproject')
cursor = connection.cursor()

def go_to_main_frame():
     
    for frame in [show_frame, find_frame, find_by_title_frame, find_by_author_frame, find_by_isbn_frame, find_by_genre_frame, update_frame, insert_frame, delete_frame]:
        if frame is not None:
            frame.grid_forget()
    main_frame.grid(row=0, column=0)
      
def show_books():
    
   # Ukryj ramkę główną
    main_frame.grid_forget()
    # Wyświetl ramkę z książkami
    show_frame.grid(row=0, column=0)
   
    query_availiable_books = "SELECT book_id, title, author, publication_year, isbn, genre FROM Books WHERE availability=1"
    query_borrowed_books = "SELECT book_id, title, author, publication_year, isbn, genre FROM Books WHERE availability=0"
    cursor.execute(query_availiable_books)
    
    Label(show_frame, text="Available books:", bg=bgcolor, font=('verdana',13, 'bold')).grid(row=0,column=0, padx=10, pady=5, sticky='w')
    Button(show_frame, text="Back", command=go_to_main_frame, font=('verdana',12), bg=button_color).grid(row=0,column=2, padx=10, pady=5, sticky='e')
    row_num = 1
    for (book_id, title, author, publication_year, isbn, genre) in cursor:
        Label(show_frame, text=f'{row_num}.  ID: {book_id}, "{title}", {author}, ({publication_year}), ISBN: {isbn}, Genre: {genre}', bg=bgcolor, font=('verdana',10)).grid(row=row_num, column=0, padx=10, pady=5, sticky='w')
        row_num += 1
    cursor.execute(query_borrowed_books)

    row_num2 = 1
    Label(show_frame, text="Borrowed  books:", bg=bgcolor, font=('verdana',13, 'bold')).grid(row=0,column=1, padx=10, pady=5, sticky='w')
    for (book_id, title, author, publication_year, isbn, genre) in cursor:
        Label(show_frame, text=f'{row_num2}. ID: {book_id}, "{title}", {author}, ({publication_year}), ISBN: {isbn}, Genre: {genre}', bg=bgcolor, font=('verdana',10)).grid(row=row_num2, column=1, padx=10, pady=5, sticky='w')
        row_num2 += 1
    connection.commit()

def find_book():
    main_frame.grid_forget()
    find_frame.grid(row=0, column=0)

    
def find_by_title():
    for widget in find_by_title_frame.winfo_children():
        widget.destroy()
    find_frame.grid_forget()
    find_by_title_frame.grid(row=0, column=0) 
    Button(find_by_title_frame, text="Back", command=go_to_main_frame, font=('verdana',12), bg=button_color).grid(row=0,column=2, padx=10, pady=5, sticky='e')
    title = entry_find_by_title.get()
    query_select_by_title = 'SELECT book_id, title, author, publication_year, isbn, genre FROM Books WHERE title LIKE %s'
    
    try:
        cursor.execute(query_select_by_title, (f'%{title}%',))
        result = cursor.fetchall()
        
        if not result:
            Label(find_by_title_frame, text="No books found with this title.", bg=bgcolor, font=('verdana',13, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        else:
            Label(find_by_title_frame, text=f'Results for title: "{title}":', bg=bgcolor, font=('verdana',13, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky='w')
            row_num = 1
            for (book_id, title, author, publication_year, isbn, genre) in result:
                Label(find_by_title_frame, text=f'{row_num}. "{title}", {author}, ({publication_year}), ISBN: {isbn}, Genre: {genre}', bg=bgcolor, font=('verdana',10)).grid(row=row_num, column=0, padx=10, pady=5, sticky='w')
                row_num += 1
    except mysql.connector.Error as err:
        print("An error occurred:", err)
    entry_find_by_title.delete(0,'end')
      

def find_by_author():
    # Usunięcie wszystkich elementów z ramki przed wyświetleniem nowych wyników
    for widget in find_by_author_frame.winfo_children():
        widget.destroy()
    find_frame.grid_forget()
    find_by_author_frame.grid(row=0, column=0) 
    Button(find_by_author_frame, text="Back", command=go_to_main_frame, font=('verdana',12), bg=button_color).grid(row=0,column=2, padx=10, pady=5, sticky='e')
    author = entry_find_by_author.get()
    query_select_by_author = "SELECT book_id, title, author, publication_year, isbn, genre FROM Books WHERE author LIKE %s"
    
    try:
        cursor.execute(query_select_by_author, (f'%{author}%',))
        result = cursor.fetchall()
        
        if not result:
            Label(find_by_author_frame, text="No books found with this author.", bg=bgcolor, font=('verdana',13, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        else:
            Label(find_by_author_frame, text=f'Results for author: "{author}":', bg=bgcolor, font=('verdana',13, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky='w')
            row_num = 1
            for (book_id, title, author, publication_year, isbn, genre) in result:
                Label(find_by_author_frame, text=f'{row_num}. "{title}", {author}, ({publication_year}), ISBN: {isbn}, Genre: {genre}', bg=bgcolor, font=('verdana',10)).grid(row=row_num, column=0, padx=10, pady=5, sticky='w')
                row_num += 1
    except mysql.connector.Error as err:
        print("An error occurred:", err)
    entry_find_by_author.delete(0,'end')

def find_by_isbn():
    for widget in find_by_isbn_frame.winfo_children():
        widget.destroy()
    find_frame.grid_forget()
    find_by_isbn_frame.grid(row=0, column=0) 
    Button(find_by_isbn_frame, text="Back", command=go_to_main_frame, font=('verdana',12), bg=button_color).grid(row=0,column=1, padx=10, pady=5, sticky='e')
    isbn = entry_find_by_isbn.get()
    query_select_by_isbn = 'SELECT book_id, title, author, publication_year, isbn, genre FROM Books WHERE isbn LIKE %s'
    
    try:
        cursor.execute(query_select_by_isbn, (f'%{isbn}%',))
        result = cursor.fetchall()
        
        if not result:
            Label(find_by_isbn_frame, text="No books found with this ISBN.", bg=bgcolor, font=('verdana',13, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        else:
            Label(find_by_isbn_frame, text=f'Results for ISBN: "{isbn}":', bg=bgcolor, font=('verdana',13, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky='w')
            row_num = 1
            for (book_id, title, author, publication_year, isbn, genre) in result:
                Label(find_by_isbn_frame, text=f'{row_num}. "{title}", {author}, ({publication_year}), ISBN: {isbn}, Genre: {genre}', bg=bgcolor, font=('verdana',10)).grid(row=row_num, column=0, padx=10, pady=5, sticky='w')
                row_num += 1
    except mysql.connector.Error as err:
        print("An error occurred:", err)
    entry_find_by_isbn.delete(0,'end')

def find_by_genre():
    find_frame.grid_forget()
    find_by_genre_frame.grid(row=0, column=0) 
    Button(find_by_genre_frame, text="Back", command=go_to_main_frame, font=('verdana',12), bg=button_color).grid(row=0,column=1, padx=10, pady=5, sticky='e')
    genre = value_inside.get()
    query_select_by_genre = 'SELECT book_id, title, author, publication_year, isbn, genre FROM Books WHERE genre=%s'
    
    try:
        cursor.execute(query_select_by_genre, (genre,))
        result = cursor.fetchall()
        
        if not result:
            Label(find_by_genre_frame, text=f"No books found in the {genre} genre.", bg=bgcolor).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        else:
            Label(find_by_genre_frame, text=f'Results for genre: "{genre}":', bg=bgcolor, font=('verdana',13, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky='w')
            row_num = 1
            for (book_id, title, author, publication_year, isbn, genre) in result:
                Label(find_by_genre_frame, text=f'{row_num}. "{title}", {author}, ({publication_year}), ISBN: {isbn}, Genre: {genre}', bg=bgcolor, font=('verdana',10)).grid(row=row_num, column=0, padx=10, pady=5, sticky='w')
                row_num += 1
    except mysql.connector.Error as err:
        print("An error occurred:", err)
   
def update_book_in_library():
    id = entry_id.get()
    updated_title = entry_update_title.get()
    updated_author = entry_update_author.get()
    updated_year = entry_update_year.get()
    updated_isbn = entry_update_isbn.get()
    updated_genre = entry_update_genre.get()
    updated_availability = availability_update_var.get()
    if id =='':
        messagebox.showerror("Error", "You have to insert ID to update record")
    else:
        query_update = 'UPDATE `books` SET `title`=%s,`author`=%s,`publication_year`=%s,`isbn`=%s,`genre`=%s,`availability`=%s WHERE `book_id`=%s'
        values_to_query = (updated_title,updated_author,updated_year,updated_isbn,updated_genre,updated_availability,id)
        cursor.execute(query_update,values_to_query)
        connection.commit()
        messagebox.showinfo("Information", f"Record with ID='{id}' has been updated")

def update_book():
    main_frame.grid_forget()
    update_frame.grid(row=0, column=0)
    global entry_id
    global entry_update_title
    global entry_update_author
    global entry_update_year
    global entry_update_isbn
    global entry_update_genre
    global availability_update_var
    Label(update_frame, text="Update records in library",bg=bgcolor, font=('verdana',13, 'bold')).grid(row=0,column=0, padx=10, pady=5, sticky='w', columnspan=2)
    Button(update_frame, text="Back", command=go_to_main_frame, font=('verdana',12), bg=button_color).grid(row=0,column=1, padx=10, pady=5, sticky='e')

    Label(update_frame, text="ID:", font=('verdana',12,'bold'), bg=bgcolor).grid(row=1,column=0, padx=10, pady=5, sticky='e')
    entry_id=Entry(update_frame, font=('verdana',12), bg=entry_color)
    entry_id.grid(row=1,column=1, padx=10, pady=5, sticky='e')

    Label(update_frame, text="Title:", font=('verdana',12), bg=bgcolor).grid(row=2,column=0, padx=10, pady=5, sticky='e')
    entry_update_title=Entry(update_frame, font=('verdana',12), bg=entry_color)
    entry_update_title.grid(row=2,column=1, padx=10, pady=5, sticky='e')

    Label(update_frame, text="Author:", font=('verdana',12), bg=bgcolor).grid(row=3,column=0, padx=10, pady=5, sticky='e')
    entry_update_author=Entry(update_frame, font=('verdana',12), bg=entry_color)
    entry_update_author.grid(row=3,column=1, padx=10, pady=5, sticky='e')

    Label(update_frame, text="Publication year:", font=('verdana',12), bg=bgcolor).grid(row=4,column=0, padx=10, pady=5, sticky='e')
    entry_update_year=Entry(update_frame, font=('verdana',12), bg=entry_color)
    entry_update_year.grid(row=4,column=1, padx=10, pady=5, sticky='e')

    Label(update_frame, text="ISBN:", font=('verdana',12), bg=bgcolor).grid(row=5,column=0, padx=10, pady=5, sticky='e')
    entry_update_isbn=Entry(update_frame, font=('verdana',12), bg=entry_color)
    entry_update_isbn.grid(row=5,column=1, padx=10, pady=5, sticky='e')

    Label(update_frame, text="Genre:", font=('verdana',12), bg=bgcolor).grid(row=6,column=0, padx=10, pady=5, sticky='e')
    entry_update_genre=Entry(update_frame, font=('verdana',12), bg=entry_color)
    entry_update_genre.grid(row=6,column=1, padx=10, pady=5, sticky='e')

    availability_update_var = IntVar()  # Zmienna, która będzie przechowywać wybór użytkownika
    
    Label(update_frame, text="Availability:", font=('verdana',12), bg=bgcolor).grid(row=7, column=0, padx=10, pady=5, sticky='e')

    # Utwórz przyciski radiowe i przypisz im odpowiednie wartości
    Radiobutton(update_frame, text="Available", font=('verdana',12), bg=bgcolor, variable=availability_update_var, value=1).grid(row=7, column=1, padx=10, pady=5, sticky='w')
    Radiobutton(update_frame, text="Not available", font=('verdana',12), bg=bgcolor, variable=availability_update_var, value=0).grid(row=8, column=1, padx=10, pady=5, sticky='w')

    Button(update_frame, text="Update", font=('verdana',12), command=update_book_in_library, bg=button_color).grid(row=9,column=1, padx=10, pady=5)

def insert_book_to_library():
    title = entry_title.get()
    author = entry_author.get()
    year = entry_year.get()
    isbn = entry_isbn.get()
    genre = entry_genre.get()
    availability = availability_var.get()

    if title == '' or author == '' or year == '' or isbn == '' or genre == '' or not isbn.isdigit() or not year.isdigit():
        messagebox.showerror("Error", "Wrong values or empty fields")
    if len(isbn) not in (10, 13):
        messagebox.showerror("Error", "ISBN number must have 10 or 13 digits.")
        return   
    else:
        query_insert = 'INSERT INTO books (title, author, publication_year, isbn, genre, availability) VALUES (%s,%s,%s,%s,%s,%s)'
        values_to_query = (title,author,year,isbn,genre,availability)

        cursor.execute(query_insert,values_to_query)
        connection.commit()
        messagebox.showinfo("Information", "The book has been added")
        entry_title.delete(0, 'end')
        entry_author.delete(0, 'end')
        entry_year.delete(0, 'end')
        entry_genre.delete(0, 'end')
        entry_isbn.delete(0, 'end')

def insert_book():
    main_frame.grid_forget()
    insert_frame.grid(row=0, column=0)
    global entry_title
    global entry_author
    global entry_year
    global entry_isbn
    global entry_genre
    global availability_var
    Label(insert_frame, text="Insert book to library",bg=bgcolor, font=('verdana',13, 'bold')).grid(row=0,column=0, padx=10, pady=5, sticky='w', columnspan=2)
    Button(insert_frame, text="Back", command=go_to_main_frame, font=('verdana',12), bg=button_color).grid(row=0,column=1, padx=10, pady=5, sticky='e')
    Label(insert_frame, text="Title:", font=('verdana',12), bg=bgcolor).grid(row=1,column=0, padx=10, pady=5, sticky='e')
    
    entry_title=Entry(insert_frame, font=('verdana',12), bg=entry_color)
    entry_title.grid(row=1,column=1, padx=10, pady=5, sticky='e')

    Label(insert_frame, text="Author:", font=('verdana',12), bg=bgcolor).grid(row=2,column=0, padx=10, pady=5, sticky='e')
    entry_author=Entry(insert_frame, font=('verdana',12),bg=entry_color)
    entry_author.grid(row=2,column=1, padx=10, pady=5, sticky='e')

    Label(insert_frame, text="Publication year:", font=('verdana',12), bg=bgcolor).grid(row=3,column=0, padx=10, pady=5, sticky='e')
    entry_year=Entry(insert_frame, font=('verdana',12),bg=entry_color)
    entry_year.grid(row=3,column=1, padx=10, pady=5, sticky='e')

    Label(insert_frame, text="ISBN:", font=('verdana',12), bg=bgcolor).grid(row=4,column=0, padx=10, pady=5, sticky='e')
    entry_isbn=Entry(insert_frame, font=('verdana',12),bg=entry_color)
    entry_isbn.grid(row=4,column=1, padx=10, pady=5, sticky='e')

    Label(insert_frame, text="Genre:", font=('verdana',12), bg=bgcolor).grid(row=5,column=0, padx=10, pady=5, sticky='e')
    entry_genre=Entry(insert_frame, font=('verdana',12),bg=entry_color)
    entry_genre.grid(row=5,column=1, padx=10, pady=5, sticky='e')

    availability_var = IntVar()  # Zmienna, która będzie przechowywać wybór użytkownika
    
    Label(insert_frame, text="Availability:", font=('verdana',12), bg=bgcolor).grid(row=6, column=0, padx=10, pady=5, sticky='e')

    # Utwórz przyciski radiowe i przypisz im odpowiednie wartości
    Radiobutton(insert_frame, text="Available", font=('verdana',12), bg=bgcolor, variable=availability_var, value=1).grid(row=6, column=1, padx=10, pady=5, sticky='w')
    Radiobutton(insert_frame, text="Not available", font=('verdana',12), bg=bgcolor, variable=availability_var, value=0).grid(row=7, column=1, padx=10, pady=5, sticky='w')

    Button(insert_frame, text="Insert", font=('verdana',12), command=insert_book_to_library, bg=button_color).grid(row=8,column=1, padx=10, pady=5)
    
    
def delete_book():
    main_frame.grid_forget()
    delete_frame.grid(row=0, column=0)
    global entry_isbn
    global entry_id
    Label(delete_frame, text="Delete book",bg=bgcolor, font=('verdana',13, 'bold')).grid(row=0,column=0, padx=10, pady=5, sticky='w')
    Button(delete_frame, text="Back", command=go_to_main_frame, font=('verdana',12), bg=button_color).grid(row=0,column=2, padx=10, pady=5, sticky='e')

    Label(delete_frame, text="By ISBN number:", font=('verdana',12), bg=bgcolor).grid(row=1,column=0, padx=10, pady=5, sticky='e')
    entry_isbn=Entry(delete_frame, font=('verdana',12), width=15, bg=entry_color)
    entry_isbn.grid(row=1,column=1, padx=10, pady=5, sticky='w')
    Button(delete_frame, text="Delete", font=('verdana',12), command=delete_by_isbn, bg=button_color).grid(row=1,column=2, padx=10, pady=5)
    Label(delete_frame, text="By ID number:", font=('verdana',12), bg=bgcolor).grid(row=2,column=0, padx=10, pady=5, sticky='e')
    entry_id=Entry(delete_frame, font=('verdana',12), width=15, bg=entry_color)
    entry_id.grid(row=2,column=1, padx=10, pady=5, sticky='w')
    Button(delete_frame, text="Delete", font=('verdana',12), command=delete_by_id, bg=button_color).grid(row=2,column=2, padx=10, pady=5)

def delete_by_isbn():
    isbn = entry_isbn.get()
    query_delete_by_isbn = 'DELETE FROM books WHERE isbn=%s'

    if isbn == '':
        messagebox.showerror("Error", "Please enter the book ISBN.")
        return
    query_check_book = "SELECT * FROM Books WHERE isbn = %s"
    cursor.execute(query_check_book, (isbn,))
    existing_book = cursor.fetchone() #jeśli wynik zapytania zawiera jakieś dane, to ta linijka zwróci ten pierwszy rekord jako krotkę

    if not existing_book:
        messagebox.showerror("Error", "A book with this ISBN number does not exist in the database.")
        return
    if len(isbn) not in (10, 13):
        messagebox.showerror("Error", "ISBN number must have 10 or 13 digits.")
        return
    
    cursor.execute(query_delete_by_isbn,(isbn,))
    connection.commit()
    messagebox.showinfo("Information", "Book has been deleted!")

    # Usunięcie etykiety z ramki show_frame ---------------------------------------------------------------------------------------------
    for widget in show_frame.winfo_children():
        if isinstance(widget, Label) and f'ISBN: {isbn}' in widget.cget("text"):
            widget.grid_remove()

    entry_isbn.delete(0,'end')

def delete_by_id():
    id = entry_id.get()
    query_delete_by_id = 'DELETE FROM books WHERE book_id=%s'

    if id == '':
        messagebox.showerror("Error", "Please enter the book ID.")
        return
    query_check_book = "SELECT * FROM Books WHERE book_id = %s"
    cursor.execute(query_check_book, (id,))
    existing_book = cursor.fetchone() #jeśli wynik zapytania zawiera jakieś dane, to ta linijka zwróci ten pierwszy rekord jako krotkę

    if not existing_book:
        messagebox.showerror("Error", "A book with this ID does not exist in the database.")
        return
    
    cursor.execute(query_delete_by_id,(id,))
    connection.commit()
    messagebox.showinfo("Information", "Book has been deleted!")

    for widget in show_frame.winfo_children():
        if isinstance(widget, Label) and f'ID: {id}' in widget.cget("text"):
            widget.grid_remove()

    entry_id.delete(0,'end')
    
def quit_app():
    root.destroy()

root = Tk()
root.title("Library Management System")
bgcolor = "#F0FFF0"
entry_color="#F8F8FF"
button_color = "#FFFFF0"
root.configure(bg=bgcolor)


main_frame = tk.Frame(root)
show_frame = tk.Frame(root)
find_frame = tk.Frame(root)
find_by_title_frame = tk.Frame(root)
find_by_author_frame = tk.Frame(root)
find_by_isbn_frame = tk.Frame(root)
find_by_genre_frame = tk.Frame(root)
update_frame = tk.Frame(root)
insert_frame = tk.Frame(root)
delete_frame = tk.Frame(root)

main_frame.configure(bg=bgcolor)
show_frame.configure(bg=bgcolor)
find_frame.configure(bg=bgcolor)
find_by_title_frame.configure(bg=bgcolor)
find_by_author_frame.configure(bg=bgcolor)
find_by_isbn_frame.configure(bg=bgcolor)
find_by_genre_frame.configure(bg=bgcolor)
update_frame.configure(bg=bgcolor)
insert_frame.configure(bg=bgcolor)
delete_frame.configure(bg=bgcolor)

Label(main_frame, text="Welcome to",font=('verdana',12, 'bold'), bg=bgcolor, fg='#000066').grid(row=0, column=0, padx=10, pady=10, columnspan=2,sticky='s')
Label(main_frame, text="LIBRARY MANAGMENT SYSTEM",font=('verdana',15, 'bold'), bg=bgcolor, fg='#000066').grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky='n') #tekst w kolumnie 0, ale rozciągnięty do 0,1,2

#image_path = "logo.png"
#logo_image = PhotoImage(file=image_path)
#logo_label = Label(main_frame, image=logo_image).grid(row=0,column=0, sticky='w', padx=10)
Label(main_frame, text="_________________________________________________________________________", bg=bgcolor).grid(row=2, column=0, columnspan=2)
Label(main_frame, text="Choose an action:", font=('verdana',13, 'bold'), bg=bgcolor).grid(row=3, column=0, padx=10, pady=5,columnspan=2)

Label(main_frame, text="Show available books:", font=('verdana',12), bg=bgcolor).grid(row=4, column=0, padx=10, pady=5, sticky='e')
Button(main_frame, text="Show", font=('verdana',12,'bold'), command=show_books, bg=button_color).grid(row=4, column=1, padx=10, pady=5, sticky='nesw')
Label(main_frame, text="Find your book:", font=('verdana',12), bg=bgcolor).grid(row=5,column=0, padx=10, pady=5, sticky='e')
Button(main_frame, text="Find", font=('verdana',12,'bold'), command=find_book, bg=button_color).grid(row=5, column=1, padx=10, pady=5, sticky='nesw')
Label(main_frame, text="Update library:", font=('verdana',12), bg=bgcolor).grid(row=6,column=0,padx=10, pady=5, sticky='e')
Button(main_frame, text="Update", font=('verdana',12,'bold'), command=update_book, bg=button_color).grid(row=6, column=1, padx=10, pady=5, sticky='nesw')
Label(main_frame, text="Insert book:", font=('verdana',12), bg=bgcolor).grid(row=7, column=0, padx=10, pady=5, sticky='e')
Button(main_frame, text="Insert", font=('verdana',12,'bold'), command=insert_book, bg=button_color).grid(row=7, column=1, padx=10, pady=5, sticky='nesw')
Label(main_frame, text="Delete book:", font=('verdana',12), bg=bgcolor).grid(row=8, column=0, padx=10, pady=5, sticky='e')
Button(main_frame, text="Delete",font=('verdana',12,'bold'), command=delete_book, bg=button_color).grid(row=8, column=1, padx=10, pady=5, sticky='nesw')
Label(main_frame, text="_________________________________________________________________________", bg=bgcolor).grid(row=9, column=0, columnspan=2)


photo = PhotoImage(file = r"x.png")
photoimage = photo.subsample(8, 8)
Button(main_frame,text="Quit", image=photoimage, font=('verdana',12,'bold'), compound = LEFT, command=quit_app, width=80, bg=button_color).grid(row=10, column=0, padx=10, pady=5, sticky='e',columnspan=1)




main_frame.grid(row=0,column=0)

# Elementy ramki find_frame

Label(find_frame, text="Insert values to find book", bg=bgcolor, font=('verdana',13, 'bold')).grid(row=0,column=0, padx=10, pady=5, sticky='w', columnspan=2)
Button(find_frame, text="Back", command=go_to_main_frame, font=('verdana',12), bg=button_color).grid(row=0,column=2, padx=10, pady=5, sticky='e')
Label(find_frame, text="Find by title:", bg=bgcolor, font=('verdana',12)).grid(row=1,column=0, padx=10, pady=5, sticky='e')
entry_find_by_title=Entry(find_frame, font=('verdana',12), bg=entry_color)
entry_find_by_title.grid(row=1,column=1, padx=10, pady=5, sticky='w')
Button(find_frame, text="Ok", font=('verdana',12), command=find_by_title, bg=button_color).grid(row=1,column=2, padx=10, pady=5, sticky='e')



Label(find_frame, text="Find by author:", bg=bgcolor, font=('verdana',12)).grid(row=2,column=0, padx=10, pady=5, sticky='e')
entry_find_by_author=Entry(find_frame, font=('verdana',12), bg=entry_color)
entry_find_by_author.grid(row=2,column=1, padx=10, pady=5, sticky='w')
Button(find_frame, text="Ok", font=('verdana',12), command=find_by_author, bg=button_color).grid(row=2,column=2, padx=10, pady=5, sticky='e')

Label(find_frame, text="Find by ISBN:", bg=bgcolor, font=('verdana',12)).grid(row=3,column=0, padx=10, pady=5, sticky='e')
entry_find_by_isbn=Entry(find_frame, font=('verdana',12), bg=entry_color)
entry_find_by_isbn.grid(row=3,column=1, padx=10, pady=5, sticky='w')
Button(find_frame, text="Ok", font=('verdana',12), command=find_by_isbn, bg=button_color).grid(row=3,column=2, padx=10, pady=5, sticky='e')

Label(find_frame, text="Find by genre:", bg=bgcolor, font=('verdana',12)).grid(row=4,column=0, padx=10, pady=5, sticky='e')
options_list = ["Fantasy", "Literary Fiction", "Dystopian Fiction", "Classic", "Coming-of-Age Fiction", "Science Fiction", "Action & Adventure","Romance","Children’s"]
value_inside = tk.StringVar(root) 
value_inside.set("Science Fiction")
question_menu = OptionMenu(find_frame, value_inside, *options_list)  
question_menu.grid(row=4,column=1, padx=10, pady=5, sticky='nesw')
Button(find_frame, text="Ok", font=('verdana',12), command=find_by_genre, bg=button_color).grid(row=4,column=2, padx=10, pady=5, sticky='e')

# Elementy ramki find_frame


Label(find_by_title_frame, text="Books:").grid(row=0,column=0, padx=10, pady=5, sticky='w', columnspan=2)

# Elementy ramki update_frame
Label(update_frame, text="do zrobienia", bg=bgcolor).grid(row=0,column=0, padx=10, pady=5, sticky='w')
button_back_to_main = Button(update_frame, text="Back", command=go_to_main_frame, bg=button_color).grid(row=0,column=1, padx=10, pady=5, sticky='e')

# Elementy ramki insert_frame

 


# Elementy ramki delete_frame

root.mainloop()


connection.close()