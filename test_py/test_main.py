# import unittest
# from main import *
#
#
# # Test print_hi()
# class TestPrintHi(unittest.TestCase):
#     def test_print_hi(self, name='World'):
#         self.assertEqual(print_hi(name), "Hi, World")
#
#
# # if __name__ == '__main__':
# #
# #     x = TestPrintHi()
# #     x.test_print_hi()
#

import unittest
import subprocess
from unittest.mock import patch
from main import give_answer

# import hello_world from main.py
from main import *
import os


class Test1(unittest.TestCase):
    # test call to help expecting success
    def test_help_statement(self):
        x = subprocess.call(['python3', '../main.py', '-h', '&>', '/dev/null'], stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        self.assertEqual(x, 0)

    # test non existent directory expecting error
    def test_non_existent_output(self):
        x = subprocess.call(['python3', '../main.py', 'https://giphy.com/gifs/whatever', '-o', 'bad_o'],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        self.assertEqual(x, 1)

    # test no input expecting error
    def test_non_existent_input(self):
        x = subprocess.call(['python3', '../main.py', ''], stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        self.assertEqual(x, 1)

    # test existing file call sending '' expecting "Overwriting..."
    @patch('main.get_response',
           return_value='')  # TODO - this isn't actually being called... see https://stackoverflow.com/questions/21046717/python-mocking-raw-input-in-unittests
    def test_existing_file_yes(self, input):
        x = subprocess.run(['python3', '../main.py', 'https://giphy.com/gifs/whatever', '-n', 'test.gif'],
                           capture_output=True)
        self.assertEqual(give_answer('y'), 'Overwriting...')  # TODO - replace give_answer with patch

    # grabber = GiphyGrabber(url='https://giphy.com/gifs/rNgT8P8pL3dn2', config_path='../config.json')
    #
    # def test_GiphyGrabber_get_gif_url(self):
    #     self.assertEqual("https://media1.giphy.com/media/rNgT8P8pL3dn2/giphy.gif", Test1.grabber.clean_gif_url)
    #
    # def test_save_gif(self):
    #     gif_title = 'testing'
    #     Test1.grabber.save_gif(gif_title)
    #     self.assertTrue(os.path.exists(f"/Users/matt/Desktop/gifs/{gif_title}.gif"))


if __name__ == '__main__':
    unittest.main()
