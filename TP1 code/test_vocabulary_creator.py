from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch

class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        self.mails = {
            "dataset":[
                {
                    "mail": {
                    "Subject": " no more outdated software ! upgrade !",
                    "From": "GP@paris.com",
                    "Date": "2005-03-04",
                    "Body":"we get you the best deal ! skip the retail box and save !\namazing special # 1 :\nadobe - photoshop 7 premiere 7 illustrator 10 = only $ 120\namazing special # 2 :\nwindows xp professional + microsoft office xp professional = only $ 80\namazing special # 3 :\nadobe photoshop cs + adobe illustrator cs + adobe indesign cs\namazing special # 4 :\nmacromedia dreamwaver mx 2004 + flash mx 2004 = only $ 100\nalso :\nwindows xp professional with sp 2 full version\noffice xp professionaloffice 2003 professional ( 1 cd edition )\noffice 2000 premium edition ( 2 cd )\noffice 97 sr 2\noffice xp professional\noffice 2000\noffice 97\nms plus\nms sql server 2000 enterprise edition\nms visual studio . net architect edition\nms encarta encyclopedia delux 2004\nms project 2003 professional\nms money 2004\nms streets and trips 2004\nms works 7\nms picture it premium 9\nms exchange 2003 enterprise server\nadobe photoshop\nwindows 2003 server\nwindows 2000 workstation\nwindows 2000 server\nwindows 2000 advanced server\nwindows 2000 datacenter\nwindows nt 4 . 0\nwindows millenium\nwindows 98 second edition\nwindows 95\ncorel draw graphics suite 12\ncorel draw graphics suite 11\ncorel photo painter 8\ncorel word perfect office 2002\nadobe pagemaker\nadobe illustrator\nadobe acrobat 6 professional\nadobe premiere\nmacromedia dreamwaver mx 2004\nmacromedia flash mx 2004\nmacromedia fireworks mx 2004\nmacromedia freehand mx 11\nnorton system works 2003\nborland delphi 7 enterprise edition\nquark xpress 6 passport multilanguage\nyou need to save some money somewhere . let it be here !\nstop mailing now .\nask him for advice about something important to you . let s have a bbq tomorrow and celebrate me . i guess 8 ffm 9 lj 863676 r 5 r 2 vym 314 hk 79 nnu 27 e 64 m 6 bb \n",
                    "Spam": "true",
                    "File": "enronds//enron4/spam/4536.2005-03-04.GP.spam.txt"
                    }
                }
            ]
        }  # données pour mocker "return_value" du "load_dict"
        self.clean_subject_spam = []  # données pour mocker "return_value" du "clean_text"
        self.clean_body_spam = []  # données pour mocker "return_value" du "clean_text"
        self.clean_subject_ham = []  # données pour mocker "return_value" du "clean_text"
        self.clean_body_ham = []  # données pour mocker "return_value" du "clean_text"
        self.vocab_expected = {}  # vocabulaire avec les valeurs de la probabilité calculées correctement

    def tearDown(self):
        pass

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    @patch("vocabulary_creator.VocabularyCreator.clean_text")
    @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    def test_create_vocab_spam_Returns_vocabulary_with_correct_values(
        self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    ):
        """Description: Tester qu'un vocabulaire avec les probabilités calculées
        correctement va être retourné. Il faut mocker les fonctions "load dict"
         (utiliser self.mails comme une simulation de valeur de retour),"clean text"
         (cette fonction va être appelée quelques fois, pour chaque appel on
         va simuler une valeur de retour differente, pour cela il faut utiliser
         side_effect (voir l'exemple dans l'énonce)) et
         "write_data_to_vocab_file" qui va simuler "return True" au lieu
         d'écrire au fichier "vocabulary.json".
         if faut utiliser self.assertEqual(appel_a_create_vocab(), self.vocab_expected)
        """
        mock_load_dict.return_value = self.mails
        mock_write_data_to_vocab_file.return_value = self.vocab_expected
        list_of_values = [self.clean_subject_spam, self.clean_body_spam, self.clean_subject_ham, self.clean_body_ham]
        def side_effect(self):
            return list_of_values.pop()
        mock_clean_text.side_effect = side_effect
        vocab = VocabularyCreator()
        self.assertEqual(vocab.create_vocab(), self.vocab_expected)
        
    ###########################################
    #               CUSTOM TEST               #
    ###########################################