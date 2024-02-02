import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import csv

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
        # Label pour le titre
        title_label = tk.Label(self.root, text="Tableau de Bord - Gestion de Stock", font=("Helvetica", 16))
        title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

        # Bouton pour exporter les produits en CSV
        export_button = tk.Button(self.root, text="Exporter CSV", command=self.export_csv)
        export_button.grid(row=1, column=0, padx=10, pady=10)

        # Liste déroulante pour choisir la catégorie de produits à filtrer
        categories = self.get_categories()
        self.selected_category = tk.StringVar()
        self.category_menu = ttk.Combobox(self.root, textvariable=self.selected_category, values=categories)
        self.category_menu.set("Toutes les catégories")
        self.category_menu.grid(row=1, column=1, padx=10, pady=10)

        # Bouton pour appliquer le filtre par catégorie
        filter_button = tk.Button(self.root, text="Filtrer", command=self.apply_category_filter)
        filter_button.grid(row=1, column=2, padx=10, pady=10)

        # Création d'un Treeview pour afficher les produits
        self.product_tree = ttk.Treeview(self.root, columns=("ID", "Nom", "Description", "Prix", "Quantité", "Catégorie"))
        self.product_tree.heading("#0", text="", anchor="w")
        self.product_tree.column("#0", anchor="w", width=1)
        self.product_tree["show"] = "headings"  # Masquer la première colonne vide

        for col in ["ID", "Nom", "Description", "Prix", "Quantité", "Catégorie"]:
            self.product_tree.heading(col, text=col, anchor="w")
            self.product_tree.column(col, anchor="w", width=100)

        self.populate_product_tree()
        self.product_tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def export_csv(self):
        try:
            filename = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(["ID", "Nom", "Description", "Prix", "Quantité", "Catégorie"])
                    query = "SELECT * FROM product"
                    if self.selected_category.get() != "Toutes les catégories":
                        query += f" WHERE id_category = {self.get_category_id(self.selected_category.get())}"
                    self.cursor.execute(query)
                    for row in self.cursor.fetchall():
                        csv_writer.writerow(row)
                messagebox.showinfo("Export CSV", "Exportation réussie.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export CSV : {str(e)}")

    def get_categories(self):
        self.cursor.execute("SELECT name FROM category")
        return [row[0] for row in self.cursor.fetchall()]

    def get_category_id(self, category_name):
        self.cursor.execute(f"SELECT id FROM category WHERE name = '{category_name}'")
        return self.cursor.fetchone()[0]

    def apply_category_filter(self):
        self.populate_product_tree()

    def populate_product_tree(self):
        self.product_tree.delete(*self.product_tree.get_children())
        query = "SELECT p.id, p.name, p.description, p.price, p.quantity, c.name " \
                "FROM product p LEFT JOIN category c ON p.id_category = c.id"
        if self.selected_category.get() != "Toutes les catégories":
            query += f" WHERE p.id_category = {self.get_category_id(self.selected_category.get())}"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            self.product_tree.insert("", "end", values=row)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = Stock(root)
    app.run()
