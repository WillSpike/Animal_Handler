# database_management.py
import sqlite3
import os
from datetime import datetime, date
from typing import Tuple, Optional

class DatabaseManagement:
    def __init__(self, db_name: str):
        self.db_name = os.path.join(os.getcwd(), db_name)
        self.conn: Optional[sqlite3.Connection] = None

    # Fonction qui crée les bases de données
    def create_database(self) -> None:
        self.conn = sqlite3.connect(self.db_name)
        self.create_animals_base()
        self.create_habitats_base()
        self.create_stock_db()
        print("Les bases de données ont été créées.")

    def create_animals_base(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Animals(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categories TEXT,
                nickname TEXT,
                age INTEGER,
                sex TEXT,
                weight REAL,
                state TEXT,
                health TEXT,
                notes TEXT,
                habitat_id INTEGER,
                FOREIGN KEY(habitat_id) REFERENCES Terrariums(id),
                FOREIGN KEY(habitat_id) REFERENCES Aquariums(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Snakes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                animal_id INTEGER,
                species TEXT,
                phase TEXT,
                length REAL,
                venomous BOOLEAN,
                shedding_dates TEXT,
                meal_date DATE,
                FOREIGN KEY(animal_id) REFERENCES Animals(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Fish(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                animal_id INTEGER,
                species TEXT,
                phase TEXT,
                size REAL,
                freshwater BOOLEAN,
                brackish_water BOOLEAN,
                sea_water BOOLEAN,
                feeding_type TEXT,
                meal_dates TEXT,
                FOREIGN KEY(animal_id) REFERENCES Animals(id)
            )
        """)
        self.conn.commit()

    def create_habitats_base(self) -> None:
        cursor = self.conn.cursor() 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Terrariums(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_habitat TEXT,
                day_temperature REAL,
                night_temperature REAL,
                hygrometry REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Aquariums(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_habitat TEXT,
                lighting_time REAL,
                pH REAL,
                gh REAL,
                kh REAL               
            )
        """)
        self.conn.commit()

    def add_animal(self, categories, nickname, age, sex, weight, state, health, notes, habitat_id):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Animals (categories, nickname, age, sex, weight, state, health, notes, habitat_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (categories, nickname, age, sex, weight, state, health, notes, habitat_id))
        self.conn.commit()
        return cursor.lastrowid

    def add_fish(self, animal_id, species, phase, size, freshwater, brackish_water, sea_water, feeding_type, meal_dates):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Fish (animal_id, species, phase, size, freshwater, brackish_water, sea_water, feeding_type, meal_dates) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (animal_id, species, phase, size, freshwater, brackish_water, sea_water, feeding_type, meal_dates))
        self.conn.commit()
        return cursor.lastrowid

    def add_snake(self, animal_id, species, phase, length, venomous, shedding_dates, meal_date):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Snakes (animal_id, species, phase, length, venomous, shedding_dates, meal_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (animal_id, species, phase, length, venomous, shedding_dates, meal_date))
        self.conn.commit()
        return cursor.lastrowid




    def get_all_habitats(self) -> list:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Terrariums")
        terrariums = cursor.fetchall()
        cursor.execute("SELECT * FROM Aquariums")
        aquariums = cursor.fetchall()
        cursor.close()
        return terrariums + aquariums


    def create_stock_db(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Stock(
                item_name TEXT PRIMARY KEY,
                quantity INTEGER
            )
        """)
        self.conn.commit()

    def close_database(self) -> None:
        if self.conn is not None:
            self.conn.close()
            print("Les bases de données ont été fermées.")
        else:
            print("Aucune base de données n'est actuellement ouverte.")





