# gui.py
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget,QButtonGroup,QRadioButton, QVBoxLayout,QCheckBox ,QApplication, QLineEdit, QPushButton,  QComboBox, QLabel, QSpacerItem,QSizePolicy 
from database_management import DatabaseManagement


class GUI(QMainWindow):
    def __init__(self, db_manager: DatabaseManagement, app: QApplication):
        super().__init__()
        self.db_manager = db_manager
        self.app = app
        self.setWindowTitle("Gestion de la base de données")
        self.setGeometry(100, 100, 800, 600)

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

    def run(self):
        self.show()
        self.app.exec()

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

        layout = QVBoxLayout()
        self.setLayout(layout)
      
        self.categories_field = QComboBox()
        self.categories_field.addItem("Serpent")
        self.categories_field.addItem("Poisson")
        layout.addWidget(QLabel("Catégorie"))
        layout.addWidget(self.categories_field)
        self.categories_field.setFixedWidth(100)

        self.nickname_field = QLineEdit()
        layout.addWidget(QLabel("Surnom"))
        layout.addWidget(self.nickname_field) 
        self.nickname_field.setFixedWidth(100)             

        # Création d'un QComboBox pour l'âge
        self.age_combobox = QComboBox()
        self.age_combobox.setFixedWidth(40)
        
        for age in range(101):  # de 0 à 100 ans
            self.age_combobox.addItem(str(age))    

        layout.addWidget(QLabel("Age"))
        layout.addWidget(self.age_combobox)

        # Création d'un groupe de boutons radio
        self.gender_group = QButtonGroup()        

        # Création des boutons radio
        self.male_radio = QRadioButton("Male")
        self.female_radio = QRadioButton("Femelle")
        self.undefined_radio = QRadioButton("Indéfini")

        # Ajout des boutons radio au groupe
        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)
        self.gender_group.addButton(self.undefined_radio)

        # Ajout des boutons radio à un layout
        layout.addWidget(QLabel("Sexe"))
        layout.addWidget(self.male_radio)
        layout.addWidget(self.female_radio)
        layout.addWidget(self.undefined_radio)

        self.weight_field = QLineEdit()
        layout.addWidget(QLabel("Poids"))
        layout.addWidget(self.weight_field)
        self.weight_field.setFixedWidth(100)

        self.state_field = QLineEdit()
        layout.addWidget(QLabel("Stade"))
        layout.addWidget(self.state_field)
        self.state_field.setFixedWidth(100)

        self.health_field = QLineEdit()
        layout.addWidget(QLabel("Santé"))
        layout.addWidget(self.health_field)
        self.health_field.setFixedWidth(100)

        self.notes_field = QLineEdit()
        layout.addWidget(QLabel("Notes"))
        layout.addWidget(self.notes_field)
        self.notes_field.setFixedWidth(100)

        self.habitat_id_field = QLineEdit()
        self.habitat_id_field.setEnabled(False)  # Griser le champ pour le rendre non modifiable
        layout.addWidget(QLabel("Habitat ID (généré automatiquement)"))
        layout.addWidget(self.habitat_id_field)
        self.habitat_id_field.setFixedWidth(100)



        # Créez les widgets pour les serpents et les poissons       
        self.snake_widgets = self.create_snake_widgets()
        self.fish_widgets = self.create_fish_widgets()

        # Stockez les widgets actuellement affichés ici.
        self.current_widgets = []

        # Connectez le signal currentTextChanged au slot update_form.
        self.categories_field.currentTextChanged.connect(self.update_form)

        # Définissez une valeur par défaut pour le QComboBox.
        self.categories_field.setCurrentIndex(1)  # Sélectionnez "Serpent" par défaut.

        # Création et ajout du bouton "Enregistrer" au layout
        submit_button = QPushButton("Enregistrer")
        submit_button.setFixedWidth(100)
        layout.addWidget(submit_button)
        submit_button.clicked.connect(self.submit)


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

        self.length_field = QLineEdit()
        self.length_field.setFixedWidth(100)
        snake_widgets.append(QLabel("Longueur"))
        snake_widgets.append(self.length_field)

        self.venomous_field = QCheckBox("Veneneux")
        self.venomous_field.setFixedWidth(100)
        snake_widgets.append(self.venomous_field)

        self.shedding_dates_field = QLineEdit()
        self.shedding_dates_field.setFixedWidth(100)
        snake_widgets.append(QLabel("Dates de mues"))
        snake_widgets.append(self.shedding_dates_field)

        self.meal_date_field = QLineEdit()
        self.meal_date_field.setFixedWidth(100)
        snake_widgets.append(QLabel("Dates repas"))
        snake_widgets.append(self.meal_date_field)

        return snake_widgets
      
    def create_fish_widgets(self)->list:
        fish_widgets = []

        self.species_field = QLineEdit()
        self.species_field.setFixedWidth(100)
        fish_widgets.append(QLabel("Espece"))
        fish_widgets.append(self.species_field)

        self.phase_field = QLineEdit()
        self.phase_field.setFixedWidth(100)
        fish_widgets.append(QLabel("Phase"))
        fish_widgets.append(self.phase_field)

        self.size_field = QLineEdit()
        self.size_field.setFixedWidth(100)
        fish_widgets.append(QLabel("Taille"))
        fish_widgets.append(self.size_field)

        self.freshwater_field = QCheckBox("Eau douce")
        self.freshwater_field.setFixedWidth(100)
        fish_widgets.append(self.freshwater_field)

        self.brackish_water_field = QCheckBox("Eau saumatre")
        self.brackish_water_field.setFixedWidth(100)
        fish_widgets.append(self.brackish_water_field)

        self.sea_water_field = QCheckBox("Eau de mer")
        self.sea_water_field.setFixedWidth(100)
        fish_widgets.append(self.sea_water_field)

        self.feeding_type_field = QLineEdit()
        self.feeding_type_field.setFixedWidth(100)
        fish_widgets.append(QLabel("Type de nourriture"))
        fish_widgets.append(self.feeding_type_field)

        self.meal_dates_field = QLineEdit()
        self.meal_dates_field.setFixedWidth(100)
        fish_widgets.append(QLabel("Dates repas"))
        fish_widgets.append(self.meal_dates_field)

        return fish_widgets
       
    def update_form(self, category)->None:
        # Supprimez les widgets spécifiques à la catégorie précédente.
        for widget in self.current_widgets:
            self.layout().removeWidget(widget)
            widget.setParent(None)

        # Réinitialisez la liste des widgets actuellement affichés.
        self.current_widgets = []

        # Ajoutez les widgets appropriés au layout.
        if category == "Serpent":
            for widget in self.snake_widgets:
                self.layout().addWidget(widget)
                self.current_widgets.append(widget)
        elif category == "Poisson":
            for widget in self.fish_widgets:
                self.layout().addWidget(widget)
                self.current_widgets.append(widget)

    def submit(self):
        categories = self.categories_field.currentText()
        nickname = self.nickname_field.text()
        age = int(self.age_combobox.currentText())
        sex = "Male" if self.male_radio.isChecked() else "Femelle" if self.female_radio.isChecked() else "Indéfini"
        weight = float(self.weight_field.text())
        state = self.state_field.text()
        health = self.health_field.text()
        notes = self.notes_field.text()
        habitat_id = None  # Vous pouvez récupérer l'ID de l'habitat ici si nécessaire

        # Ajouter l'animal dans la table Animals
        animal_id = self.db_manager.add_animal(categories, nickname, age, sex, weight, state, health, notes, habitat_id)

        if categories == "Serpent":
            snake_species = self.snake_species_field.text()
            snake_phase = self.snake_phase_field.text()
            length = float(self.length_field.text())
            venomous = self.venomous_field.isChecked()
            shedding_dates = self.shedding_dates_field.text()
            meal_date = self.meal_date_field.text()

            # Ajouter le serpent dans la table Snakes
            self.db_manager.add_snake(animal_id, snake_species, snake_phase, length, venomous, shedding_dates, meal_date)
        elif categories == "Poisson":
            fish_species = self.species_field.text()
            fish_phase = self.phase_field.text()
            size = float(self.size_field.text())
            freshwater = self.freshwater_field.isChecked()
            brackish_water = self.brackish_water_field.isChecked()
            sea_water = self.sea_water_field.isChecked()
            feeding_type = self.feeding_type_field.text()
            meal_dates = self.meal_dates_field.text()

            # Ajouter le poisson dans la table Fish
            self.db_manager.add_fish(animal_id, fish_species, fish_phase, size, freshwater, brackish_water, sea_water, feeding_type, meal_dates)

        # Réinitialiser les champs du formulaire
        self.nickname_field.clear()
        self.age_combobox.setCurrentIndex(0)
        self.male_radio.setChecked(True)
        self.weight_field.clear()
        self.state_field.clear()
        self.health_field.clear()
        self.notes_field.clear()

        if categories == "Serpent":
            self.species_field.clear()
            self.phase_field.clear()
            self.length_field.clear()
            self.venomous_field.setChecked(False)
            self.shedding_dates_field.clear()
            self.meal_date_field.clear()
        elif categories == "Poisson":
            self.species_field.clear()
            self.phase_field.clear()
            self.size_field.clear()
            self.freshwater_field.setChecked(False)
            self.brackish_water_field.setChecked(False)
            self.sea_water_field.setChecked(False)
            self.feeding_type_field.clear()
            self.meal_dates_field.clear()

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


