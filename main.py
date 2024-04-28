# main.py
import sys
from database_management import DatabaseManagement
from gui import GUI
from PyQt6.QtWidgets import QApplication 

def main():
    # Créer une instance de DatabaseManagement et créer les bases de données
    db_manager = DatabaseManagement('my_database.db')
    db_manager.create_database()

    # Créer et exécuter l'interface utilisateur
    app = QApplication(sys.argv)
    gui = GUI(db_manager, app)
    gui.run()

    # Fermer les bases de données
    db_manager.close_database()

if __name__ == "__main__":
    main()
