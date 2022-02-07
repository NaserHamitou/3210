import json

from email_analyzer import EmailAnalyzer

import unittest
from unittest.mock import patch


class TestEmailAnalyzer(unittest.TestCase):
    def setUp(self):
        self.subject = " la uncle rummie s hangover pills ! absolutely new ! naeyc"
        self.body = "a recent survey shows that it takes an average of just 3 . 2\ndrinks to cause a hangover . for ten percent of people all\nit takes is one or two . but uncle rummy s hangover helper\nhelps you avoid hangovers and wake up feeling great from head\nto stomach and everywhere else .\nmore information here\n"
        self.clean_subject = [" louise"]  # données pour mocker "return_value" du "clean_text"
        self.clean_body = ["did we retain all the historical data from eol . we met some folks that can help us analyse it \n"]  # données pour mocker "return_value" du "clean_text"
        self.spam_ham_body_prob_true = (
            20,
            0,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.spam_ham_subject_prob_true = (
            20,
            0,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.spam_ham_body_prob_false = (
            0,
            20,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.spam_ham_subject_prob_false = (
            0,
            20,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.vocab = (
            {
                "p_sub_spam": {
                "rummie": 0.5,
                "naeyc": 0.5,
                "pills": 0.5
            },
            "p_sub_ham": {
                "uncle": 0.5,
                "absolutely": 0.5,
                "new": 0.5
            },
            "p_body_spam": {
                "uncle rummy s": 0.5,
                "hangover .": 0.5,
                "survey": 0.5
            },
            "p_body_ham": {
                "recent": 0.1,
                "shows": 0.1,
                "average": 0.1,
            }
            }
        )  # vocabulaire avec les valeurs de la probabilité pour mocker "return_value" du "load_dict"
        self.spam_ham_body_prob_expected = 3.655366451388055e-179, 2.5140284032753285e-179  # valeurs des probabilités attendues
        self.spam_ham_subject_prob_expected = 3.655366451388055e-179, 2.5140284032753285e-179  # valeurs des probabilités attendues

    def tearDown(self):
        pass

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_subject_prob")
    def test_is_spam_Returns_True_if_spam_prob_is_higher(
        self, mock_spam_ham_subject_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être True si probabilité spam > probabilité ham
        """
        mock_spam_ham_body_prob.return_value = self.spam_ham_body_prob_true
        mock_spam_ham_subject_prob.return_value = self.spam_ham_subject_prob_true
        emailAnalyzer = EmailAnalyzer()
        self.assertTrue(emailAnalyzer.is_spam(self.subject, self.body))

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_subject_prob")
    def test_is_spam_Returns_False_if_spam_prob_is_lower(
        self, mock_spam_ham_subject_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être False si probabilité spam < probabilité ham
        """
        mock_spam_ham_body_prob.return_value = self.spam_ham_body_prob_false
        mock_spam_ham_subject_prob.return_value = self.spam_ham_subject_prob_false
        emailAnalyzer = EmailAnalyzer()
        self.assertFalse(emailAnalyzer.is_spam(self.subject, self.body))
        pass

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_spam_ham_body_prob_Returns_expected_probability(self, mock_load_dict):
        """
        Il faut mocker la fonction "load_dict"
        Il faut vérifier que probabilité est calculée correctement en fonction du "body"
        """
        mock_load_dict.return_value = self.vocab
        emailAnalyzer = EmailAnalyzer()
        self.assertEqual(emailAnalyzer.spam_ham_body_prob(self.body), self.spam_ham_body_prob_expected)
        pass

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_subject_spam_ham_prob_Returns_expected_probability(self, mock_load_dict):
        """
        Il faut mocker la fonction "load_dict"
        il faut vérifier que probabilité est calculée correctement en fonction du "sujet"
        """
        mock_load_dict.return_value = self.vocab
        emailAnalyzer = EmailAnalyzer()
        self.assertEqual(emailAnalyzer.spam_ham_subject_prob(self.body), self.spam_ham_subject_prob_expected)
        pass

    ###########################################
    #               CUSTOM TEST               #
    ###########################################
    