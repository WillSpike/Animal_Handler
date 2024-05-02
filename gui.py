# gui.py
from typing import Tuple
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget,QButtonGroup,QRadioButton, QVBoxLayout, QHBoxLayout, QCheckBox ,QApplication, QLineEdit, QPushButton, QComboBox, QLabel, QDateEdit
from PyQt6.QtWidgets import QTextEdit ,QDoubleSpinBox ,QMessageBox ,QScrollArea ,QSpacerItem ,QSizePolicy ,QGridLayout ,QTableWidget ,QTableWidgetItem
from database_management import DatabaseManagement
from datetime import datetime

class GUI(QMainWindow):
    def __init__(self, db_manager: DatabaseManagement, app: QApplication):
        super().__init__()
        self.db_manager = db_manager
        self.app = app
        self.setWindowTitle("Gestion de la base de données")
        self.setGeometry(100, 100, 1000, 800)  # Taille de la fenêtre

        # Créer un onglet principal avec des options pour chaque type d'action
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Onglet "Animaux"
        self.animals_tab = AnimalsTab(self.db_manager)
        self.tab_widget.addTab(self.animals_tab, "Animaux")

        # Onglet "Habitats"
        self.habitats_tab = HabitatsTab(self.db_manager)
        self.tab_widget.addTab(self.habitats_tab, "Habitats")

        # Onglet "Stocks"
        self.stocks_tab = StocksTab(self.db_manager)
        self.tab_widget.addTab(self.stocks_tab, "Stocks")

        # Onglet "Rapports" ou "Statistiques" a venir

    def run(self):
        try:
            self.show()
            self.app.exec()
        except Exception as e:
            QMessageBox.critical(self, "Erreur inattendue", "Une erreur inattendue s'est produite. Veuillez redémarrer l'application.")
            print(f"Erreur inattendue : {str(e)}")

class AnimalsTab(QWidget):
    def __init__(self, db_manager: DatabaseManagement):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Créer un widget pour la gestion des animaux
        animal_management_widget = AnimalManagementWidget(self.db_manager)
        layout.addWidget(animal_management_widget)

        self.setLayout(layout)

class AnimalManagementWidget(QWidget):
    def __init__(self, db_manager: DatabaseManagement):
        super().__init__()
        self.db_manager = db_manager

        # Création du layout principal en horizontal
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Création du layout pour le formulaire à gauche
        self.form_layout = QVBoxLayout()
        self.main_layout.addLayout(self.form_layout)

        # Création du layout pour l'affichage des informations à droite
        self.info_layout = QVBoxLayout()
        self.main_layout.addLayout(self.info_layout)

        # Création des QLabel pour afficher les statistiques
        self.total_animals_label = QLabel()
        self.num_snakes_label = QLabel()
        self.num_fish_label = QLabel()
        self.average_age_label = QLabel()
        self.average_weight_label = QLabel()

        # Création et ajout du bouton "Afficher les animaux" au layout
        self.display_button = QPushButton("Afficher les animaux")
        self.display_button.setFixedWidth(150)
        self.form_layout.addWidget(self.display_button)
        self.display_button.clicked.connect(self.display_animals)

        # Création du QTextEdit pour afficher les informations des animaux
        self.animal_info_text_edit = QTextEdit()
        self.animal_info_text_edit.setReadOnly(True)
        self.info_layout.addWidget(self.animal_info_text_edit)

        # Création et ajout du bouton "Enregistrer" au layout
        self.submit_button = QPushButton("Ajouter l'animal")
        self.submit_button.setFixedWidth(150)
        self.form_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.submit)

        # Création du champ de sélection de la catégorie
        self.categories_field = QComboBox()
        self.categories_field.addItem("Serpent")
        self.categories_field.addItem("Poisson")
        self.form_layout.addWidget(QLabel("Catégorie"))
        self.form_layout.addWidget(self.categories_field)
        self.categories_field.setFixedWidth(100)

        # Création du champ de saisie du surnom
        self.nickname_field = QLineEdit()
        self.form_layout.addWidget(QLabel("Surnom"))
        self.form_layout.addWidget(self.nickname_field)
        self.nickname_field.setFixedWidth(100)

        # Création du champ de sélection de l'âge
        self.age_combobox = QComboBox()
        self.age_combobox.setFixedWidth(40)
        for age in range(101):  # de 0 à 100 ans
            self.age_combobox.addItem(str(age))
        self.form_layout.addWidget(QLabel("Age"))
        self.form_layout.addWidget(self.age_combobox)

        # Création des boutons radio pour le sexe
        self.gender_group = QButtonGroup()
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Femelle")
        self.undefined_radio = QRadioButton("Indéfini")
        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)
        self.gender_group.addButton(self.undefined_radio)
        self.form_layout.addWidget(QLabel("Sexe"))
        self.form_layout.addWidget(self.male_radio)
        self.form_layout.addWidget(self.female_radio)
        self.form_layout.addWidget(self.undefined_radio)

        # Création des autres champs du formulaire
        self.weight_field = QLineEdit()
        self.form_layout.addWidget(QLabel("Poids"))
        self.form_layout.addWidget(self.weight_field)
        self.weight_field.setFixedWidth(100)

        self.state_field = QLineEdit()
        self.form_layout.addWidget(QLabel("Stade"))
        self.form_layout.addWidget(self.state_field)
        self.state_field.setFixedWidth(100)

        self.health_field = QLineEdit()
        self.form_layout.addWidget(QLabel("Santé"))
        self.form_layout.addWidget(self.health_field)
        self.health_field.setFixedWidth(100)

        self.notes_field = QLineEdit()
        self.form_layout.addWidget(QLabel("Notes"))
        self.form_layout.addWidget(self.notes_field)
        self.notes_field.setFixedWidth(100)

        self.habitat_id_field = QLineEdit()
        self.habitat_id_field.setEnabled(False)  # Griser le champ pour le rendre non modifiable
        self.form_layout.addWidget(QLabel("Habitat ID (généré automatiquement)"))
        self.form_layout.addWidget(self.habitat_id_field)
        self.habitat_id_field.setFixedWidth(100)

        # Création des widgets pour les serpents et les poissons
        self.snake_widgets = self.create_snake_widgets()
        self.fish_widgets = self.create_fish_widgets()

        # Stockage des widgets actuellement affichés
        self.current_widgets = []

        # Connexion du signal currentTextChanged au slot update_form
        self.categories_field.currentTextChanged.connect(self.update_form)

        # Définition de la valeur par défaut pour le QComboBox
        self.categories_field.setCurrentIndex(1)  # "Serpent" par défaut

    def display_animals(self) -> None:
        # Récupération des données de la base de données
        data = self.db_manager.get_all_animals()

        # Créer un layout vertical principal
        main_layout = QVBoxLayout()

        # Créer un layout horizontal pour la barre de recherche
        search_layout = QHBoxLayout()
        main_layout.addLayout(search_layout)

        # Afficher la barre de recherche
        self.display_search_bar(search_layout)

        # Créer un layout horizontal pour l'affichage des animaux et des statistiques
        animals_stats_layout = QHBoxLayout()
        main_layout.addLayout(animals_stats_layout)

        # Créer un layout vertical pour les informations des animaux
        animals_layout = QVBoxLayout()

        # Créer un layout vertical pour les statistiques
        stats_layout = QVBoxLayout()

        # Calculer les statistiques
        total_animals, average_age, average_weight, num_snakes, num_fish = self.calculate_statistics(data)

        # Ajouter les statistiques au layout de droite
        self.display_statistics(total_animals, average_age, average_weight, num_snakes, num_fish)

        # Créer un QScrollArea pour encadrer l'affichage des animaux
        animals_scroll_area = QScrollArea()
        animals_scroll_area.setWidgetResizable(True)
        animals_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        animals_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Créer un nouveau widget pour afficher les informations des animaux
        self.animal_info_widget = QWidget()
        self.animal_info_widget.setLayout(animals_layout)

        # Ajouter le nouveau widget à QScrollArea
        animals_scroll_area.setWidget(self.animal_info_widget)

        # Parcourir tous les animaux et afficher leurs informations
        for animal in data:
            animal_info = self.format_animal_info(animal)
            animal_info_label = QLabel(animal_info)
            animal_info_label.setWordWrap(True)
            animals_layout.addWidget(animal_info_label)

        # Ajouter le QScrollArea et le layout des statistiques au layout principal
        animals_stats_layout.addWidget(animals_scroll_area)
        animals_stats_layout.addLayout(stats_layout)

        # Définir le layout principal sur QTextEdit
        self.animal_info_text_edit.setLayout(main_layout)

    def display_statistics(self, total_animals, average_age, average_weight, num_snakes, num_fish):
        # Supprimer l'ancien widget stats_table s'il existe
        if hasattr(self, 'stats_table'):
            self.main_layout.removeWidget(self.stats_table)
            self.stats_table.deleteLater()
            self.stats_table = None

        # Créer un nouveau widget stats_table
        self.stats_table = QTableWidget()
        self.stats_table.setRowCount(5)
        self.stats_table.setColumnCount(1)

        # Définir les en-têtes verticaux
        self.stats_table.setVerticalHeaderLabels(["Nombre total d'animaux", "Nombre de serpents", "Nombre de poissons", "Moyenne d'âge", "Moyenne de poids"])

        # Remplir le tableau avec les statistiques
        self.stats_table.setItem(0, 0, QTableWidgetItem(str(total_animals)))
        self.stats_table.setItem(1, 0, QTableWidgetItem(str(num_snakes)))
        self.stats_table.setItem(2, 0, QTableWidgetItem(str(num_fish)))
        self.stats_table.setItem(3, 0, QTableWidgetItem(f"{average_age:.2f} ans"))
        self.stats_table.setItem(4, 0, QTableWidgetItem(f"{average_weight:.2f} kg"))

        # Cacher l'en-tête horizontal
        self.stats_table.horizontalHeader().setVisible(False)

        # Ajouter le nouveau widget stats_table à main_layout
        self.main_layout.addWidget(self.stats_table)

    def calculate_statistics(self, data: list) -> Tuple[int, float, float, int, int]:
        total_animals = len(data)
        total_age = sum(animal[3] for animal in data)
        average_age = total_age / total_animals if total_animals else 0
        total_weight = sum(animal[5] for animal in data)
        average_weight = total_weight / total_animals if total_animals else 0
        num_snakes = sum(1 for animal in data if animal[1] == "Serpent")
        num_fish = sum(1 for animal in data if animal[1] == "Poisson")
        return total_animals, average_age, average_weight, num_snakes, num_fish

    def update_display_animals(self):
        # Effacer les widgets existants
        for i in reversed(range(self.animal_info_widget.layout().count())): 
            self.animal_info_widget.layout().itemAt(i).widget().setParent(None)

        # Récupération des données de la base de données
        data = self.db_manager.get_all_animals()

        # Calculer les statistiques
        total_animals, average_age, average_weight, num_snakes, num_fish = self.calculate_statistics(data)

        # Mettre à jour les labels des statistiques
        self.display_statistics(total_animals, average_age, average_weight, num_snakes, num_fish)

        # Parcourir tous les animaux et afficher leurs informations
        for animal in data:
            animal_info = self.format_animal_info(animal)
            animal_info_label = QLabel(animal_info)
            animal_info_label.setWordWrap(True)
            self.animal_info_widget.layout().addWidget(animal_info_label)

        self.update()

    def format_animal_info(self, animal: tuple) -> str:        
        animal_info = f"<b>Catégorie:</b> {animal[1]}<br>"
        animal_info += f"<b>Nom:</b> {animal[2]}<br>"
        animal_info += f"<b>Age:</b> {animal[3]}<br>"
        animal_info += f"<b>Sexe:</b> {animal[4]}<br>"
        animal_info += f"<b>Poids:</b> {animal[5]}<br>"
        animal_info += f"<b>Stade:</b> {animal[6]}<br>"
        animal_info += f"<b>Santé:</b> {animal[7]}<br>"
        animal_info += f"<b>Notes:</b> {animal[8]}<br>"        

        if animal[1] == "Serpent":           
            animal_info += f"<b>Espèce:</b> {animal[12]}<br>"
            animal_info += f"<b>Phase:</b> {animal[13]}<br>"
            animal_info += f"<b>Longueur:</b> {animal[14]}<br>"
            animal_info += f"<b>Venimeux:</b> {animal[15]}<br>"
            animal_info += f"<b>Dates de mue:</b> {animal[16]}<br>"
            animal_info += f"<b>Date du dernier repas:</b> {animal[17]}<br>"
        elif animal[1] == "Poisson":            
            animal_info += f"<b>Espèce:</b> {animal[12]}<br>"
            animal_info += f"<b>Phase:</b> {animal[13]}<br>"
            animal_info += f"<b>Taille:</b> {animal[14]}<br>"
            animal_info += f"<b>Eau douce:</b> {animal[15]}<br>"
            animal_info += f"<b>Eau saumâtre:</b> {animal[16]}<br>"
            animal_info += f"<b>Eau de mer:</b> {animal[17]}<br>"
            animal_info += f"<b>Type d'alimentation:</b> {animal[18]}<br>"
            animal_info += f"<b>Dates des repas:</b> {animal[19]}<br>"

        return animal_info
        
    def create_snake_widgets(self) -> list:
        snake_widgets = []
        self.snake_species_field = QLineEdit()
        self.snake_species_field.setFixedWidth(100)
        snake_widgets.append(QLabel("Espece"))
        snake_widgets.append(self.snake_species_field)

        self.snake_phase_field = QLineEdit()
        self.snake_phase_field.setFixedWidth(100)
        snake_widgets.append(QLabel("Phase"))
        snake_widgets.append(self.snake_phase_field)

        self.length_field = QDoubleSpinBox()
        self.length_field.setRange(0, 1000)
        self.length_field.setSingleStep(0.1)
        self.length_field.setFixedWidth(100)
        snake_widgets.append(QLabel("Longueur"))
        snake_widgets.append(self.length_field)

        self.venomous_field = QCheckBox("Venimeux")
        self.venomous_field.setFixedWidth(100)
        snake_widgets.append(self.venomous_field)

        self.shedding_dates_field = QDateEdit()
        self.shedding_dates_field.setFixedWidth(100)
        snake_widgets.append(QLabel("Dates de mues"))
        snake_widgets.append(self.shedding_dates_field)

        self.meal_date_field = QDateEdit()
        self.meal_date_field.setFixedWidth(100)
        snake_widgets.append(QLabel("Date du dernier repas"))
        snake_widgets.append(self.meal_date_field)

        return snake_widgets

    def create_fish_widgets(self) -> list:
        fish_widgets = []
        self.species_field = QLineEdit()
        self.species_field.setFixedWidth(100)
        fish_widgets.append(QLabel("Espece"))
        fish_widgets.append(self.species_field)

        self.phase_field = QLineEdit()
        self.phase_field.setFixedWidth(100)
        fish_widgets.append(QLabel("Phase"))
        fish_widgets.append(self.phase_field)

        self.size_field = QDoubleSpinBox()
        self.size_field.setRange(0, 500)
        self.size_field.setSingleStep(0.1)
        self.size_field.setFixedWidth(100)
        fish_widgets.append(QLabel("Taille"))
        fish_widgets.append(self.size_field)

        self.freshwater_field = QCheckBox("Eau douce")
        self.freshwater_field.setFixedWidth(100)
        fish_widgets.append(self.freshwater_field)

        self.brackish_water_field = QCheckBox("Eau saumâtre")
        self.brackish_water_field.setFixedWidth(100)
        fish_widgets.append(self.brackish_water_field)

        self.sea_water_field = QCheckBox("Eau de mer")
        self.sea_water_field.setFixedWidth(100)
        fish_widgets.append(self.sea_water_field)

        self.feeding_type_field = QLineEdit()
        self.feeding_type_field.setFixedWidth(100)
        fish_widgets.append(QLabel("Type de nourriture"))
        fish_widgets.append(self.feeding_type_field)

        self.meal_dates_field = QDateEdit()
        self.meal_dates_field.setFixedWidth(100)
        fish_widgets.append(QLabel("Dates des repas"))
        fish_widgets.append(self.meal_dates_field)

        return fish_widgets

    def update_form(self, category) -> None:
        # Supprimez les widgets spécifiques à la catégorie précédente.
        for widget in self.current_widgets:
            self.form_layout.removeWidget(widget)
            widget.setParent(None)

        # Réinitialisez la liste des widgets actuellement affichés.
        self.current_widgets = []

        # Ajoutez les widgets appropriés au layout.
        if category == "Serpent":
            for widget in self.snake_widgets:
                self.form_layout.addWidget(widget)
                self.current_widgets.append(widget)
        elif category == "Poisson":
            for widget in self.fish_widgets:
                self.form_layout.addWidget(widget)
                self.current_widgets.append(widget)

    def submit(self):
        try:
            # Récupération des données du formulaire
            categories = self.categories_field.currentText()
            nickname = self.nickname_field.text()
            age = int(self.age_combobox.currentText())
            sex = "Male" if self.male_radio.isChecked() else "Femelle" if self.female_radio.isChecked() else "Indéfini"
            weight = float(self.weight_field.text())
            state = self.state_field.text()
            health = self.health_field.text()
            notes = self.notes_field.text()
            habitat_id = None  # Vous pouvez récupérer l'ID de l'habitat ici si nécessaire

            # Ajout de l'animal dans la table Animals
            animal_id = self.db_manager.add_animal(categories, nickname, age, sex, weight, state, health, notes, habitat_id)

            # Ajout des informations spécifiques selon la catégorie
            if categories == "Serpent":
                snake_species = self.snake_species_field.text()
                snake_phase = self.snake_phase_field.text()
                try:
                    length = self.length_field.value()
                except ValueError:
                    QMessageBox.critical(self, "Erreur", "Veuillez saisir une valeur numérique pour la longueur du serpent.")
                    return
                venomous = self.venomous_field.isChecked()
                shedding_dates = self.shedding_dates_field.text()
                meal_date = self.meal_date_field.text()
                self.db_manager.add_snake(animal_id, snake_species, snake_phase, length, venomous, shedding_dates, meal_date)

            elif categories == "Poisson":
                fish_species = self.species_field.text()
                fish_phase = self.phase_field.text()
                size = self.size_field.value()
                freshwater = self.freshwater_field.isChecked()
                brackish_water = self.brackish_water_field.isChecked()
                sea_water = self.sea_water_field.isChecked()
                feeding_type = self.feeding_type_field.text()
                meal_dates = self.meal_dates_field.text() 
                # Ajouter le poisson dans la table Fish
                self.db_manager.add_fish(animal_id, fish_species, fish_phase, size, freshwater, brackish_water, sea_water, feeding_type, meal_dates)

            QMessageBox.information(self, "Succès", "L'animal a été enregistré avec succès.")                   
            self.reset_form() # Remise à zéro des champs du formulaire
            self.update_display_animals() # Mise à jour de l'affichage display_animals     
                         
        except ValueError as e:
            # Affichage d'un message d'erreur à l'utilisateur en cas de problème de saisie
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite lors de la saisie des données : {str(e)}")
        except Exception as e:
            # Affichage d'un message d'erreur générique en cas d'erreur inattendue
            QMessageBox.critical(self, "Erreur", "Une erreur inattendue s'est produite. Veuillez réessayer.")
            print(f"Erreur lors de l'ajout de l'animal : {str(e)}")

    def reset_form(self):
        """Réinitialise les champs du formulaire"""
        self.nickname_field.clear()
        self.age_combobox.setCurrentIndex(0)
        self.male_radio.setChecked(True)
        self.weight_field.clear()
        self.state_field.clear()
        self.health_field.clear()
        self.notes_field.clear()

        if self.categories_field.currentText() == "Serpent":
            self.snake_species_field.clear()
            self.snake_phase_field.clear()
            self.length_field.clear()
            self.venomous_field.setChecked(False)
            self.shedding_dates_field.setDate(datetime.now().date())
            self.meal_date_field.setDate(datetime.now().date())
        elif self.categories_field.currentText() == "Poisson":
            self.species_field.clear()
            self.phase_field.clear()
            self.size_field.clear()
            self.freshwater_field.setChecked(False)
            self.brackish_water_field.setChecked(False)
            self.sea_water_field.setChecked(False)
            self.feeding_type_field.clear()
            self.meal_dates_field.setDate(datetime.now().date())

    def display_search_bar(self, search_layout: QHBoxLayout):
        # Créer le champ de recherche et le bouton
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Rechercher un animal...")
        self.search_field.setFixedWidth(150)
        self.search_button = QPushButton("Rechercher")
        self.search_button.setFixedWidth(100)
        self.search_button.clicked.connect(self.filter_animals)

        # Ajouter les widgets au layout de recherche
        search_layout.addWidget(self.search_field)
        search_layout.addWidget(self.search_button)

    def filter_animals(self):
        search_text = self.search_field.text().lower()

        # Effacer les widgets existants
        for i in reversed(range(self.animal_info_widget.layout().count())):
            self.animal_info_widget.layout().itemAt(i).widget().setParent(None)

        # Récupérer les données de la base de données
        data = self.db_manager.get_all_animals()

        # Filtrer les animaux en fonction de la recherche
        filtered_animals = [animal for animal in data if search_text in str(animal).lower()]

        # Afficher les animaux filtrés
        for animal in filtered_animals:
            animal_info = self.format_animal_info(animal)
            animal_info_label = QLabel(animal_info)
            animal_info_label.setWordWrap(True)
            self.animal_info_widget.layout().addWidget(animal_info_label)

class HabitatsTab(QWidget):
    def __init__(self, db_manager: DatabaseManagement):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        # Ajouter les widgets pour la gestion des habitats ici
        self.setLayout(layout)

class StocksTab(QWidget):
    def __init__(self, db_manager: DatabaseManagement):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        # Ajouter les widgets pour la gestion des stocks ici
        self.setLayout(layout)


