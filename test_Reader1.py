# test_Reader1-unittest/mock.py
import random
import unittest
from time import localtime
from unittest.mock import patch, Mock
from Reader1_functions import logger, check_deadband
from Reader1_functions import insert_process


class TestLogger(unittest.TestCase):
    def test_logger_characters(self):
        time_now = localtime()
        message = "Just trying"
        self.assertEqual(logger(message), f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, "
                                          f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}"
                                          f" -> {message}\n")

    def test_logger_numbers(self):
        time_now = localtime()
        message = random.random()
        self.assertEqual(logger(message), f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, "
                                          f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}"
                                          f" -> {message}\n")

    def test_logger_null(self):
        time_now = localtime()
        message = None
        self.assertEqual(logger(message), f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, "
                                          f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}"
                                          f" -> {message}\n")

    def test_logger_empty_string(self):
        time_now = localtime()
        message = ""
        self.assertEqual(logger(message), f"{time_now.tm_mday}.{time_now.tm_mon}.{time_now.tm_year}, "
                                          f"{time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}"
                                          f" -> {message}\n")


# test za insert_process
class TestInsertProcess(unittest.TestCase):
    @patch('Reader1_functions.insert')
    def test_process__good__code_digital(self, mock_insert):
        mock_insert.return_value = "Ulazi dalje u insert"
        self.assertEqual(insert_process(1, 1, 2, 100), mock_insert.return_value)

    @patch('Reader1_functions.check_deadband')
    def test_process__good__code_analog(self, mock_check_deadband):
        mock_check_deadband.return_value = "Ulazi dalje u check_deadband"
        self.assertEqual(insert_process(1, 1, 1, 100), mock_check_deadband.return_value)

    def test_process_bad_id(self):
        self.assertEqual(insert_process("not int", 1, 1, 100), "ID is not valid!")

    def test_process_bad_id2(self):
        self.assertEqual(insert_process(None, 1, 1, 100), "ID is not valid!")

    def test_process_bad_id3(self):
        self.assertEqual(insert_process(1.33, 1, 1, 100), "ID is not valid!")

    def test_process_bad_value(self):
        self.assertEqual(insert_process(1, 1, 1, 214748364799), "Value is not valid!")

    def test_process_bad_value2(self):
        self.assertEqual(insert_process(1, 1, 1, -214748364799), "Value is not valid!")

    def test_process_bad_dataset(self):
        self.assertEqual(insert_process(1, 2, 1, 100), "Dataset is not valid!")

    def test_process_bad_dataset2(self):
        self.assertEqual(insert_process(1, None, 1, 100), "Dataset is not valid!")

    def test_process_bad_code(self):
        self.assertEqual(insert_process(1, 1, 3, 100), "Code is not in range 1:2")

    def test_process_bad_code2(self):
        self.assertEqual(insert_process(1, 1, None, 100), "Code is not integer!")


# test za check_deadband
class TestCheckDeadband(unittest.TestCase):
    @patch('Reader1_functions.get_fetchall')
    @patch('Reader1_functions.insert')
    def test_check_doesnt_exist(self, mock_insert, mock_get_fetchall):
        mock_insert.return_value = "INSERT"
        mock_get_fetchall.return_value = None
        self.assertEqual(check_deadband(1, 1, 'CODE_DIGITAL', 100), "INSERT")


#class TestCheckDeadband2(unittest.TestCase):
#    @patch('Reader1_functions.get_fetchall')
#    @patch('Reader1_functions.insert')
#    def test_check_does_exist(self, mock_insert, mock_get_fetchall):
#        mock_insert.return_value = "INSERT"
#        mock_get_fetchall.return_value = None
#        self.assertEqual(check_deadband(1, 1, 'CODE_DIGITAL', 100), "INSERT")


if __name__ == '__main__':
    unittest.main()
