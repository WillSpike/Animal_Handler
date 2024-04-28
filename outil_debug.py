    def display_animals(self):
        # Récupération des données de la base de données
        data = self.db_manager.get_all_animals()[:10]  # Récupère les 10 premiers animaux

        # Affichage des informations des animaux
        for animal in data:
            print(f"ID: {animal[0]}")
            print(f"Catégorie: {animal[1]}")
            print(f"Surnom: {animal[2]}")
            print(f"Age: {animal[3]}")
            print(f"Sexe: {animal[4]}")
            print(f"Poids: {animal[5]}")
            print(f"Stade: {animal[6]}")
            print(f"Santé: {animal[7]}")
            print(f"Notes: {animal[8]}")
            print(f"ID Habitat: {animal[9]}")

            # Afficher les informations spécifiques aux serpents
            if animal[1] == "Serpent":
                print(f"ID Serpent: {animal[10]}")
                print(f"Espèce: {animal[11]}")
                print(f"Phase: {animal[12]}")
                print(f"Longueur: {animal[13]}")
                print(f"Venimeux: {animal[14]}")
                print(f"Dates de mue: {animal[15]}")
                print(f"Date du dernier repas: {animal[16]}")

            # Afficher les informations spécifiques aux poissons
            elif animal[1] == "Poisson":
                print(f"ID Poisson: {animal[10]}")
                print(f"Espèce: {animal[11]}")
                print(f"Phase: {animal[12]}")
                print(f"Taille: {animal[13]}")
                print(f"Eau douce: {animal[14]}")
                print(f"Eau saumâtre: {animal[15]}")
                print(f"Eau de mer: {animal[16]}")
                print(f"Type d'alimentation: {animal[17]}")
                print(f"Dates des repas: {animal[18]}")

            print(f"<----------------->")