from pickle import TRUE
from crud import CRUD
import unittest
from unittest.mock import patch

class TestCRUD(unittest.TestCase):
    def setUp(self):
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_users_file
        self.users_data = {
            "1": {
                "name": "alex@gmail.com",
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            },
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "SpamN": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }
        }
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_groups_file
        self.groups_data = {
            "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
            "2": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }

        self.users_lookup = {
            'alex@gmail.com': '1',
            'mark@mail.com': '2'
        }


    def tearDown(self):
        pass


    @patch("crud.CRUD.read_users_file")    
    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_add_new_user_Passes_correct_data_to_modify_users_file(
        self, mock_modify_users_file, mock_modify_groups_file, mock_read_users_file
    ):
        """Description: il faut utiliser les mocks des fonctions "read_users_file",
        "modify_users_file" pour tester que l'information a ajouter pour l'utilisateur a été formée correctement
        par la fonction, e.g. self.modify_users_file(data) -> "data" doit avoir un format et contenu expecté
        il faut utiliser ".assert_called_once_with(expected_data)"

        Note: Ce test a deja ete complete pour vous
        """

        # Ici on mock pour que read_users_file retourne la liste d'utilisateurs
        mock_read_users_file.return_value = self.users_data

        # Les informations du nouvel utilisateur
        new_user_data = {
                "name": "james@gmail.com",
                "Trust": 50,
                "SpamN": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }

        # On effectue une copie de la liste d'utilisateurs
        users_data_final = {}
        users_data_final["1"] = self.users_data["1"]
        users_data_final["2"] = self.users_data["2"]
        # On ajoute les infos du nouvel utilisateur
        users_data_final["0"] = new_user_data

        crud = CRUD()
        crud.add_new_user("james@gmail.com", "2020-08-08")
        # On vérifie que quand on ajoute un nouvel utilisateur, modify_users_file est appelée avec la nouvelle liste mise à jour
        mock_modify_users_file.assert_called_once_with(users_data_final)
          		

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")  
    def test_add_new_group_Passes_correct_data_to_modify_groups_file(
        self, mock_modify_groups_file, mock_read_groups_file
    ):

        """Description: il faut utiliser les mocks des fonctions "read_groups_file",
        "modify_groups_file" (ou selon votre realisation) pour tester que
        l'information a ajouter pour le groupe a été formée correctement par la fonction e.g.
        self.modify_groups_file(data) -> "data" doit avoir un format et contenu attendu
        il faut utiliser ".assert_called_once_with(expected_data)"
        """
        
        mock_read_groups_file.return_value = self.groups_data

        new_group_data = {
                "name": "test",
                "Trust": 30,
                "List_of_members": ["alex@gmail.com"],
            }

        groups_data_final = {}
        groups_data_final["1"] = self.groups_data["1"]
        groups_data_final["2"] = self.groups_data["2"]
        groups_data_final["0"] = new_group_data

        crud = CRUD()
        crud.users_lookup = {'alex@gmail.com': '1', 'mark@mail.com': '2'}
        crud.users_data = self.users_data
        crud.add_new_group("test", 30, ["alex@gmail.com"])
     
        mock_modify_groups_file.assert_called_once_with(groups_data_final)
        


    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_id(self, mock_read_users_file):
        """Description: il faut utiliser le mock de fonction "read_users_file",
        (ou selon votre realisation) pour tester que false (ou bien une exception)
        est retourne par la fonction si ID non-existant est utilisé
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.get_user_data(3, "SpamN"), False)

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_field(self, mock_read_users_file):
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que false (ou bien une exception)
        est retourne par la fonction si champ non-existant est utilisé
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.get_user_data(2, "spams"), False)

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_users_file
    ):
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que une bonne valeur est fournie
        si champ et id valide sont utilises
        il faut utiliser ".assertEqual()""
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        correct_value = crud.users_data['2']['SpamN']
        self.assertEqual(crud.get_user_data(2, "SpamN"), correct_value)

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_id(self, mock_read_groups_file):
        """
        Similaire au test_get_user_data_Returns_false_for_invalid_id mais pour un groupe
        """
        mock_read_groups_file.return_value = self.users_data
        crud = CRUD()
        invalid_id = 3
        self.assertEqual(crud.get_groups_data(invalid_id, "name"), False)

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_field(
        self, mock_read_groups_file
    ):
        """
        Similaire au test_get_user_data_Returns_false_for_invalid_field mais pour un groupe
        """
        mock_read_groups_file.return_value = self.users_data
        crud = CRUD()
        invalid_field = "test"
        self.assertEqual(crud.get_groups_data(2, invalid_field), False)

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_groups_file
    ):
        """
        Similaire au test_get_user_data_Returns_correct_value_if_field_and_id_are_valid mais pour un groupe
        """
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        expected_value = self.groups_data["2"]["name"]
        self.assertEqual(crud.get_groups_data(2, 'name'), expected_value)

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_false_for_invalid_user_name(
        self, mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        invalid_user_name = "test-name"
        self.assertEqual(crud.get_user_id(invalid_user_name), False)

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_id_for_valid_user_name(self, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        valid_user_name = "alex@gmail.com"
        self.assertEqual(crud.get_user_id(valid_user_name), "1")
        

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_false_for_invalid_group_name(self, mock_read_groups_file):
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        invalid_group_name = "invalid"
        self.assertEqual(crud.get_group_id(invalid_group_name), False)

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_id_for_valid_group_name(self, mock_read_groups_file):
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        valid_name = "friends"
        self.assertEqual(crud.get_group_id(valid_name), "2")

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    # Modify_user_file mock est inutile pour tester False pour update
    def test_update_users_Returns_false_for_invalid_id(
        self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        
        crud = CRUD()
        invalid_id = -3
        value = crud.update_users(invalid_id, "Trust", 10)
        self.assertEqual(value, False)


    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_update_users_Returns_false_for_invalid_field(
        self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        
        crud = CRUD()
        invalid_field = "invalid"
        value = crud.update_users("1", invalid_field, 10)
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_update_users_Passes_correct_data_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        self.users_data["1"]["Trust"] = 10
        crud = CRUD()
        crud.update_users("1", "Trust", 10)
        mock_modify_users_file.assert_called_once_with(self.users_data)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Returns_false_for_invalid_id(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True 
        crud = CRUD()
        invalid_id = -1
        value = crud.update_groups(invalid_id, "Trust", 10)
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Returns_false_for_invalid_field(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True 
        crud = CRUD()
        invalid_field = "invalid"
        value = crud.update_groups("1", invalid_field, 10)
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Passes_correct_data_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True 
        self.groups_data["1"]["Trust"] = 10
        crud = CRUD()
        crud.update_groups(1, "Trust", 10)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)
         
        

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_Returns_false_for_invalid_id(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        invalid_id = -1
        value = crud.remove_user(invalid_id)
        self.assertEqual(value, False)
        

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_Passes_correct_value_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        crud.remove_user(1)
        mock_modify_users_file.assert_called_once_with(self.users_data)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_group_Returns_false_for_invalid_id(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        invalid_id = -1
        value = crud.remove_user_group(invalid_id, "default")
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_group_Returns_false_for_invalid_group(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        invalid_group = "invalid"
        value = crud.remove_user_group(1, invalid_group)
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Passes_correct_value_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        crud.remove_user_group(1, "default")
        mock_modify_users_file.assert_called_once_with(self.users_data)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_Returns_false_for_invalid_id(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True
        crud = CRUD()
        invalid_id = -1
        value = crud.remove_group(invalid_id)
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_Passes_correct_value_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True
        crud = CRUD()
        crud.remove_group(1)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Returns_false_for_invalid_id(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True
        crud = CRUD()
        invalid_id = -1
        value = crud.remove_group_member(invalid_id, "alex@gmail.com")
        self.assertEqual(value, False)
    

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Returns_false_for_invalid_group_member(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True
        crud = CRUD()
        invalid_member = "invalid@invalid.com"
        value = crud.remove_group_member(1, invalid_member)
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Passes_correct_value_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True
        crud = CRUD()
        crud.remove_group_member(1, "alex@gmail.com")
        mock_modify_groups_file.assert_called_once_with(self.groups_data)
    
    ###########################################
    #               CUSTOM TEST               #
    ###########################################

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")  
    def test_update_users_Returns_False_when_new_name_is_invalid(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        invalid_data = "invaliddata"
        value = crud.update_users(1, "name", invalid_data)
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_False_when_new_last_date_is_invalid(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        invalid_data = '2001-09-11'
        value = crud.update_users(1, "Date_of_last_seen_message", invalid_data)
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_False_when_new_first_date_is_invalid(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        invalid_data = '2069-04-20'
        value = crud.update_users(1, "Date_of_first_seen_message", invalid_data)
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_False_when_Trust_is_superior_to_100(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        invalid_data = 101
        value = crud.update_users(1, "Trust", invalid_data)
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_False_when_Trust_is_inferior_to_0(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        invalid_data = -1
        value = crud.update_users(1, "Trust", invalid_data)
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_False_when_SpamN_is_inferior_to_0(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        invalid_data = -1
        value = crud.update_users(1, "SpamN", invalid_data)
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_False_when_HamN_is_inferior_to_0(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        invalid_data = -1
        value = crud.update_users(1, "HamN", invalid_data)
        self.assertEqual(value, False)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Returns_False_when_new_name_lenght_is_inferior_to_1(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True 
        crud = CRUD()
        invalid_name = ""
        value = crud.update_groups(1, "name", invalid_name)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Returns_False_when_new_name_lenght_is_supperior_to_64(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True 
        crud = CRUD()
        invalid_name = ""
        number_supperior_to_64 = 70
        for i in range(number_supperior_to_64):
            invalid_name += "a"
        value = crud.update_groups(1, "name", invalid_name)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Returns_False_when_Trust_is_inferior_to_1(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True 
        crud = CRUD()
        invalid_trust = -1
        value = crud.update_groups(1, "Trust", invalid_trust)

    @patch("crud.CRUD.read_users_file")    
    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_add_new_user_Returns_False_if_email_format_is_wrong(
        self, mock_modify_users_file, mock_modify_groups_file, mock_read_users_file
    ):
        mock_modify_groups_file.return_value = True 
        mock_modify_users_file.return_value = True
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        invalid_email = "invalidemail"
        value = crud.add_new_user(invalid_email, "2020-01-01")
        self.assertEqual(value, False)

    @patch("crud.CRUD.read_users_file")    
    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_add_new_user_Returns_False_if_email_already_exist(
        self, mock_modify_users_file, mock_modify_groups_file, mock_read_users_file
    ):
        mock_modify_groups_file.return_value = True 
        mock_modify_users_file.return_value = True
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        invalid_email = "alex@gmail.com"
        value = crud.add_new_user(invalid_email, "2020-08-08")
        self.assertEqual(value, False)
