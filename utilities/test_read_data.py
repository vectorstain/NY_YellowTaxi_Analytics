import sys

from io import StringIO
from unittest import TestCase
from unittest import mock

from .read_data import readUserInput

class TestReadData(TestCase):

    @mock.patch('builtins.input', side_effect=['2022','1',"Bronx"])
    def test_readUserInput_1(self,mock_input):
        '''
        Test if given three correct input return their transformation
        '''
        result = readUserInput()
        self.assertEqual(result, [2022,1,"Bronx"])

    
    @mock.patch('builtins.input', side_effect=['20','2022','1',"Bronx"])
    def test_readUserInput_2(self,mock_input):
        '''
        Test if given a wrong year return the correct message.
        '''
        capturedOutput = StringIO()                   # Create StringIO object
        sys.stdout = capturedOutput                   #  and redirect stdout.
        result = readUserInput()                      # Call unchanged function.
        sys.stdout = sys.__stdout__                   # Reset redirect.
        capt_out = capturedOutput.getvalue()
        self.assertEqual(capt_out, "The typed year '20' is invalid, should be in the range between 2010 and 2022\n")

    @mock.patch('builtins.input', side_effect=['2022','13','1',"Bronx"])
    def test_readUserInput_3(self,mock_input):
        '''
        Test if given a wrong month return the correct message.
        '''
        capturedOutput = StringIO()                   # Create StringIO object
        sys.stdout = capturedOutput                   #  and redirect stdout.
        result = readUserInput()                      # Call unchanged function.
        sys.stdout = sys.__stdout__                   # Reset redirect.
        capt_out = capturedOutput.getvalue()
        self.assertEqual(capt_out, "The typed month '13' is invalid, should be in the range between 1 and 12\n")

    @mock.patch('builtins.input', side_effect=['2022','1',"Bronxx", "Bronx"])
    def test_readUserInput_4(self,mock_input):
        '''
        Test if given a wrong borough return the correct message.
        '''
        capturedOutput = StringIO()                   # Create StringIO object
        sys.stdout = capturedOutput                   #  and redirect stdout.
        result = readUserInput()                      # Call unchanged function.
        sys.stdout = sys.__stdout__                   # Reset redirect.
        capt_out = capturedOutput.getvalue()
        self.assertEqual(capt_out, "The typed borough 'Bronxx' is invalid, should be one of ['EWR', 'Queens', 'Bronx', 'Manhattan', 'Staten Island', 'Brooklyn']\n")