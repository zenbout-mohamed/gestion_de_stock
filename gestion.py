import tkinter as tk
from tkinter import messagebox
import mysql.connector

class Stock:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Stock")

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="0000",
            database="store"
        )
        self.cursor = self.connection.cursor()

        self.create_tables()

        self.create_widgets()

    def create_tables(self):
        # Création de la table category si elle n'existe pas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
        """)

        # Création de la table product si elle n'existe pas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS product (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price INT,
                quantity INT,
                id_category INT,
                FOREIGN KEY (id_category) REFERENCES category(id)
            )
        """)
        self.connection.commit()

    def create_widgets(self):
        # TODO: Ajoutez ici la création des widgets pour l'interface graphique
        pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Stock(root)
    app.run()
