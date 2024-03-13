import sqlite3
import tkinter as tk
from tkinter import messagebox


conn = sqlite3.connect('raamatukataloog.db')
c = conn.cursor()



# база данных (.db) // добавляет определенные таблицы, если их нет

c.execute('''CREATE TABLE IF NOT EXISTS Autorid (
             autor_id INTEGER PRIMARY KEY,
             autor_nimi TEXT,
             sünnikuupäev TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Žanrid (
             žanr_id INTEGER PRIMARY KEY,
             žanri_nimi TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Raamatud (
             raamat_id INTEGER PRIMARY KEY,
             pealkiri TEXT,
             väljaandmise_kuupäev TEXT,
             autor_id INTEGER,
             žanr_id INTEGER,
             FOREIGN KEY (autor_id) REFERENCES Autorid(autor_id),
             FOREIGN KEY (žanr_id) REFERENCES Žanrid(žanr_id))''')



# добавление книг // INSERT INTO Raamatud (pealkiri, väljaandmise_kuupäev, autor_id, žanr_id) VALUES (?, ?, ?, ?)

def lisa_raamat():
    pealkiri = entry_title.get()
    kuupaev = entry_date.get()
    autor_id = entry_author_id.get()
    zanr_id = entry_genre_id.get()
    
    if pealkiri and kuupaev and autor_id and zanr_id:
        try:
            c.execute("INSERT INTO Raamatud (pealkiri, väljaandmise_kuupäev, autor_id, žanr_id) VALUES (?, ?, ?, ?)",
                      (pealkiri, kuupaev, int(autor_id), int(zanr_id)))
            conn.commit()
            messagebox.showinfo("Lisamine", "Uus raamat on edukalt lisatud.")
        except ValueError:
            messagebox.showerror("Viga", "Autori ja žanri ID peavad olema arvudena.")
    else:
        messagebox.showerror("Viga", "Palun täitke kõik väljad.")



# удаление книг // DELETE FROM Raamatud WHERE raamat_id=?

def kustuta_raamat():
    raamat_id = entry_book_id.get()
    if raamat_id.isdigit():
        # Проверяем, существует ли книга с указанным ID
        c.execute("SELECT * FROM Raamatud WHERE raamat_id=?", (raamat_id,))
        raamat = c.fetchone()
        if raamat:
            # Если книга существует, то выполняем удаление
            c.execute("DELETE FROM Raamatud WHERE raamat_id=?", (raamat_id,))
            conn.commit()
            messagebox.showinfo("Kustutamine", "Raamat on edukalt kustutatud.")
        else:
            messagebox.showerror("Viga", "Määratud raamatu ID-d pole olemas.")
    else:
        messagebox.showerror("Viga", "Sisestage kehtiv raamatu ID.")




# отображение всех книг // SELECT SELECT Raamatud.raamat_id, Raamatud.pealkiri, Raamatud.väljaandmise_kuupäev, 
#                                  Autorid.autor_nimi, Žanrid.žanri_nimi
#                           FROM Raamatud
#                           INNER JOIN Autorid ON Raamatud.autor_id = Autorid.autor_id
#                           INNER JOIN Žanrid ON Raamatud.žanr_id = Žanrid.žanr_id

def kuva_raamatud():
    print("Kuvatakse kõik raamatud:")
    raamatud = c.execute('''SELECT Raamatud.raamat_id, Raamatud.pealkiri, Raamatud.väljaandmise_kuupäev, 
                                   Autorid.autor_nimi, Žanrid.žanri_nimi
                            FROM Raamatud
                            INNER JOIN Autorid ON Raamatud.autor_id = Autorid.autor_id
                            INNER JOIN Žanrid ON Raamatud.žanr_id = Žanrid.žanr_id''').fetchall()
    for raamat in raamatud:
        print(raamat)
    print("\n")


# добавление нового автора // INSERT INTO Autorid (autor_nimi) VALUES (?)

def lisa_autor():

    autor_nimi = entry_author_name.get()
    if autor_nimi:
        try:
            c.execute("INSERT INTO Autorid (autor_nimi) VALUES (?)", (autor_nimi,))
            conn.commit()
            messagebox.showinfo("Lisamine", f"Uus autor '{autor_nimi}' on edukalt lisatud.")
        except ValueError:
            messagebox.showerror("Viga", "Autori nimi peab olema tekstina.")
    else:
        messagebox.showerror("Viga", "Palun sisestage autori nimi.")


# удаление автора // DELETE FROM Autorid WHERE autor_id=?

def kustuta_autor():
    autor_id = entry_author_id_del.get()
    if autor_id.isdigit():
        # Проверяем, существует ли автор с указанным ID
        c.execute("SELECT * FROM Autorid WHERE autor_id=?", (autor_id,))
        autor = c.fetchone()
        if autor:
            # Если автор существует, то выполняем удаление
            c.execute("DELETE FROM Autorid WHERE autor_id=?", (autor_id,))
            conn.commit()
            messagebox.showinfo("Kustutamine", "Autor on edukalt kustutatud.")
        else:
            messagebox.showerror("Viga", "Määratud autori ID-d pole olemas.")
    else:
        messagebox.showerror("Viga", "Sisestage kehtiv autori ID.")

# отображение всех авторов // SELECT autor_id, autor_nimi FROM Autorid

def kuva_autorid():
    print("Kuvatakse kõik autorid:")
    autorid = c.execute('''SELECT autor_id, autor_nimi FROM Autorid''').fetchall()
    for autor in autorid:
        print(autor)
    print("\n")

# добавление нового жанра // INSERT INTO Žanrid (žanri_nimi) VALUES (?)

def lisa_zanr():
    zanr_nimi = entry_genre_name.get()
    if zanr_nimi:
        try:
            c.execute("INSERT INTO Žanrid (žanri_nimi) VALUES (?)", (zanr_nimi,))
            conn.commit()
            messagebox.showinfo("Lisamine", f"Uus žanr '{zanr_nimi}' on edukalt lisatud.")
        except ValueError:
            messagebox.showerror("Viga", "Žanri nimi peab olema tekstina.")
    else:
        messagebox.showerror("Viga", "Palun sisestage žanri nimi.")

# удаление жанра // DELETE FROM Žanrid WHERE žanr_id=?

def kustuta_zanr():
    zanr_id = entry_genre_id_del.get()
    if zanr_id.isdigit():
        # Проверяем, существует ли жанр с указанным ID
        c.execute("SELECT * FROM Žanrid WHERE žanr_id=?", (zanr_id,))
        zanr = c.fetchone()
        if zanr:
            # Если жанр существует, то выполняем удаление
            c.execute("DELETE FROM Žanrid WHERE žanr_id=?", (zanr_id,))
            conn.commit()
            messagebox.showinfo("Kustutamine", "Žanr on edukalt kustutatud.")
        else:
            messagebox.showerror("Viga", "Määratud žanri ID-d pole olemas.")
    else:
        messagebox.showerror("Viga", "Sisestage kehtiv žanri ID.")

# отображение всех жанров // SELECT žanr_id, žanri_nimi FROM Žanrid

def kuva_zanrid():
    print("Kuvatakse kõik žanrid:")
    zanrid = c.execute('''SELECT žanr_id, žanri_nimi FROM Žanrid''').fetchall()
    for zanr in zanrid:
        print(zanr)
    print("\n")

# графический интерфейс
root = tk.Tk()
root.title("Raamatukataloog")
root.configure(bg='#ADD8E6')

# Первый столбик
frame1 = tk.Frame(root, bg='#ADD8E6')
frame1.pack(side=tk.LEFT, padx=10)
label_title = tk.Label(frame1, text="Pealkiri:", bg='#ADD8E6')
label_title.pack()
entry_title = tk.Entry(frame1, bg='white')
entry_title.pack()
label_date = tk.Label(frame1, text="Kuupäev (DD-MM-YYYY):", bg='#ADD8E6')
label_date.pack()
entry_date = tk.Entry(frame1, bg='white')
entry_date.pack()
label_author_id = tk.Label(frame1, text="Autori ID:", bg='#ADD8E6')
label_author_id.pack()
entry_author_id = tk.Entry(frame1, bg='white')
entry_author_id.pack()
label_genre_id = tk.Label(frame1, text="Žanri ID:", bg='#ADD8E6')
label_genre_id.pack()
entry_genre_id = tk.Entry(frame1, bg='white')
entry_genre_id.pack()
btn_add_book = tk.Button(frame1, text="Lisa raamat", command=lisa_raamat, bg='white')
btn_add_book.pack()
label_book_id = tk.Label(frame1, text="Sisestage kustutatava raamatu ID:", bg='#ADD8E6')
label_book_id.pack()
entry_book_id = tk.Entry(frame1, bg='white')
entry_book_id.pack()
btn_delete_book = tk.Button(frame1, text="Kustuta raamat", command=kustuta_raamat, bg='white')
btn_delete_book.pack()
btn_show_books = tk.Button(frame1, text="Kuva kõik raamatud", command=kuva_raamatud, bg='white')
btn_show_books.pack()

# Второй столбик
frame2 = tk.Frame(root, bg='#ADD8E6')
frame2.pack(side=tk.LEFT, padx=10)
label_author_name = tk.Label(frame2, text="Autori nimi:", bg='#ADD8E6')
label_author_name.pack()
entry_author_name = tk.Entry(frame2, bg='white')
entry_author_name.pack()
btn_add_author = tk.Button(frame2, text="Lisa autor", command=lisa_autor, bg='white')
btn_add_author.pack()
label_author_id_del = tk.Label(frame2, text="Sisestage kustutatava autori ID:", bg='#ADD8E6')
label_author_id_del.pack()
entry_author_id_del = tk.Entry(frame2, bg='white')
entry_author_id_del.pack()
btn_delete_author = tk.Button(frame2, text="Kustuta autor", command=kustuta_autor, bg='white')
btn_delete_author.pack()
btn_show_authors = tk.Button(frame2, text="Kuva kõik autoreid", command=kuva_autorid, bg='white')
btn_show_authors.pack()

# Третий столбик
frame3 = tk.Frame(root, bg='#ADD8E6')
frame3.pack(side=tk.LEFT, padx=10)
label_genre_name = tk.Label(frame3, text="Žanri nimi:", bg='#ADD8E6')
label_genre_name.pack()
entry_genre_name = tk.Entry(frame3, bg='white')
entry_genre_name.pack()
btn_add_genre = tk.Button(frame3, text="Lisa žanr", command=lisa_zanr, bg='white')
btn_add_genre.pack()
label_genre_id_del = tk.Label(frame3, text="Sisestage kustutatava žanri ID:", bg='#ADD8E6')
label_genre_id_del.pack()
entry_genre_id_del = tk.Entry(frame3, bg='white')
entry_genre_id_del.pack()
btn_delete_genre = tk.Button(frame3, text="Kustuta žanr", command=kustuta_zanr, bg='white')
btn_delete_genre.pack()
btn_show_genres = tk.Button(frame3, text="Kuva kõik žanreid", command=kuva_zanrid, bg='white')
btn_show_genres.pack()

root.mainloop()

conn.close()
