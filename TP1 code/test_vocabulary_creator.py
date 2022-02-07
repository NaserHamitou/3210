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
        self.vocab_expected = {
            'p_sub_spam': 
                {
                'outdat': 0.3333333333333333, 
                'softwar': 0.3333333333333333, 
                'upgrad': 0.3333333333333333}, 
                'p_sub_ham': {}, 
                'p_body_spam': {
                    'get': 0.00641025641025641, 'best': 0.00641025641025641, 'deal': 0.00641025641025641, 'skip': 0.00641025641025641, 'retail': 0.00641025641025641, 'box': 0.00641025641025641, 'save': 0.01282051282051282, 'amaz': 0.02564102564102564, 'special': 0.02564102564102564, 'adob': 0.057692307692307696, 'photoshop': 0.019230769230769232, 'premier': 0.01282051282051282, 'illustr': 0.019230769230769232, 'window': 0.07051282051282051, 'profession': 0.04487179487179487, 'microsoft': 0.00641025641025641, 'offic': 0.05128205128205128, 'indesign': 0.00641025641025641, 'macromedia': 0.03205128205128205, 'dreamwav': 0.01282051282051282, 'flash': 0.01282051282051282, 'also': 0.00641025641025641, 'full': 0.00641025641025641, 'version': 0.00641025641025641, 'professionaloffic': 0.00641025641025641, 'edit': 0.038461538461538464, 'premium': 0.01282051282051282, 'plu': 0.00641025641025641, 'sql': 0.00641025641025641, 'server': 0.03205128205128205, 'enterpris': 0.019230769230769232, 'visual': 0.00641025641025641, 'studio': 0.00641025641025641, 'net': 0.00641025641025641, 'architect': 0.00641025641025641, 'encarta': 0.00641025641025641, 'encyclopedia': 0.00641025641025641, 'delux': 
                           0.00641025641025641, 'project': 0.00641025641025641, 'money': 0.01282051282051282, 'street': 0.00641025641025641, 'trip': 0.00641025641025641, 'work': 0.01282051282051282, 'pictur': 0.00641025641025641, 'exchang': 0.00641025641025641, 'workstat': 0.00641025641025641, 'advanc': 0.00641025641025641, 'datacent': 0.00641025641025641, 'millenium': 0.00641025641025641, 'second': 0.00641025641025641, 'corel': 0.02564102564102564, 'draw': 0.01282051282051282, 'graphic': 0.01282051282051282, 'suit': 0.01282051282051282, 'photo': 0.00641025641025641, 'painter': 0.00641025641025641, 'word': 0.00641025641025641, 'perfect': 0.00641025641025641, 'pagemak': 0.00641025641025641, 'acrobat': 0.00641025641025641, 'firework': 0.00641025641025641, 'freehand': 0.00641025641025641, 'norton': 0.00641025641025641, 'system': 0.00641025641025641, 'borland': 0.00641025641025641, 'delphi': 0.00641025641025641, 'quark': 0.00641025641025641, 'xpress': 0.00641025641025641, 'passport': 0.00641025641025641, 'multilanguag': 0.00641025641025641, 'need': 0.00641025641025641, 'somewher': 0.00641025641025641, 'let': 
                           0.01282051282051282, 'stop': 0.00641025641025641, 'mail': 0.00641025641025641, 'ask': 0.00641025641025641, 'advic': 0.00641025641025641, 'someth': 0.00641025641025641, 'import': 0.00641025641025641, 'bbq': 0.00641025641025641, 'tomorrow': 0.00641025641025641, 'celebr': 0.00641025641025641, 'guess': 0.00641025641025641, 'ffm': 0.00641025641025641, 'vym': 0.00641025641025641, 'nnu': 0.00641025641025641}, 'p_body_ham': {}
        }  
    # vocabulaire avec les valeurs de la probabilité calculées correctement

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
        mock_write_data_to_vocab_file.return_value = True
        list_of_values = [self.clean_subject_spam, self.clean_body_spam, self.clean_subject_ham, self.clean_body_ham]
        def side_effect(self):
            return list_of_values.pop()
        mock_clean_text.side_effect = side_effect
        vocab = VocabularyCreator()
        vocab.load_dict()
        vocab.write_data_to_vocab_file()
        vocab.create_vocab()
        self.assertEqual(vocab.voc_data, self.vocab_expected)
        
    ###########################################
    #               CUSTOM TEST               #
    ###########################################

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    @patch("vocabulary_creator.VocabularyCreator.clean_text")
    @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    def test_create_vocab_spam_Returns_vocabulary_when_not_spam(
        self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    ):
        """Description: Tester que le vocabulaire calculer ai les bonnes valeurs 
        de probabilités lorsqu'il ne s'agit pas d'un spam
        """
        mock_load_dict.return_value = {
            "dataset":[
                {
                    "mail": {
                    "Subject": " re : louise kitchen s visit to monterrey",
                    "From": "kitchen@paris.com",
                    "Date": "2001-06-28",
                    "Body":"louise i am sending you the agenda for your visit to monterrey .\n- 11 : 00 am - arrival to the airport . miguel angel rodriguez and i will pick you up at the exit of the international arrival area at the monterrey airport .\n- 12 : 00 pm - overall introduction to edem team participants : ( all the office ) .\n- 13 : 00 pm - lunch @ the office . we ll bring some non - spicy but traditional mexican food .\n- 14 : 00 pm - commercial meeting\nproject overview : vitro texmex fapsa baja coal project other .\nparticipants : irvin alatorre sabine duffy perez gonzalez lenci and williams .\n- 16 : 00 pm - commercial meeting\nrisk management overview : current structures marketing strategy for the remainder of the year .\nparticipants : irvin alatorre sabine duffy perez gonzalez lenci and williams .\n- 17 : 45 pm - departure to airport ( plane leaves at 7 : 20 so there should be plenty of time ) .\nbest regards \n",
                    "Spam": "false",
                    "File": "enronds//enron3/ham/1362.2001-06-28.kitchen.ham.txt"
                    }
                }
            ]
        }
        mock_write_data_to_vocab_file.return_value = True
        expected_Value = {
            'p_sub_spam': {}, 
            'p_sub_ham': {
                'louis': 0.25, 'kitchen': 0.25, 'visit': 0.25, 'monterrey': 0.25}, 
            'p_body_spam': {}, 
            'p_body_ham': {'louis': 0.01282051282051282, 'send': 0.01282051282051282, 'agenda': 0.01282051282051282, 'visit': 0.01282051282051282, 'monterrey': 0.02564102564102564, 'arriv': 0.02564102564102564, 'airport': 0.038461538461538464, 'miguel': 0.01282051282051282, 'angel': 0.01282051282051282, 'rodriguez': 0.01282051282051282, 'pick': 0.01282051282051282, 'exit': 0.01282051282051282, 'intern': 0.01282051282051282, 'area': 0.01282051282051282, 'overal': 0.01282051282051282, 'introduct': 0.01282051282051282, 'edem': 0.01282051282051282, 'team': 0.01282051282051282, 'particip': 0.038461538461538464, 'offic': 0.02564102564102564, 'lunch': 0.01282051282051282, 'bring': 0.01282051282051282, 'non': 0.01282051282051282, 'spici': 0.01282051282051282, 'tradit': 0.01282051282051282, 'mexican': 0.01282051282051282, 'food': 0.01282051282051282, 'commerci': 0.02564102564102564, 'meet': 0.02564102564102564, 'project': 0.02564102564102564, 'overview': 0.02564102564102564, 'vitro': 0.01282051282051282, 'texmex': 0.01282051282051282, 'fapsa': 0.01282051282051282, 'baja': 0.01282051282051282, 'coal': 0.01282051282051282, 'irvin': 0.02564102564102564, 'alatorr': 0.02564102564102564, 'sabin': 0.02564102564102564, 'duffi': 0.02564102564102564, 'perez': 0.02564102564102564, 'gonzalez': 0.02564102564102564, 'lenci': 0.02564102564102564, 'william': 0.02564102564102564, 'risk': 0.01282051282051282, 'manag': 0.01282051282051282, 'current': 0.01282051282051282, 'structur': 0.01282051282051282, 'market': 0.01282051282051282, 'strategi': 0.01282051282051282, 'remaind': 0.01282051282051282, 'year': 0.01282051282051282, 'departur': 0.01282051282051282, 'plane': 0.01282051282051282, 'leav': 0.01282051282051282, 'plenti': 0.01282051282051282, 'time': 0.01282051282051282, 'best': 0.01282051282051282, 'regard': 0.01282051282051282}}
        list_of_values = [self.clean_subject_spam, self.clean_body_spam, self.clean_subject_ham, self.clean_body_ham]
        def side_effect(self):
            return list_of_values.pop()
        mock_clean_text.side_effect = side_effect
        vocab = VocabularyCreator()
        vocab.load_dict()
        vocab.write_data_to_vocab_file()
        vocab.create_vocab()
        self.assertEqual(vocab.voc_data, expected_Value)
        