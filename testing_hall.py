import unittest
from Class import Camp


class TestAddDivision(unittest.TestCase):
    def test_add_division(self):
        # Créer un objet Camp fictif pour les besoins du test
        camp = Camp()

        # Appeler la fonction add_division avec des valeurs spécifiques
        camp.add_division("Division A")

        # Vérifier si la division a été ajoutée à la liste camp.divisions
        self.assertIn("Division A", camp.divisions)


if __name__ == '__main__':
    unittest.main()
