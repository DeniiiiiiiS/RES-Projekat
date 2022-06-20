# test_Reader1-unittest/mock.py
import random
import unittest
from time import localtime

from Reader1 import logger


# test za logger
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


if __name__ == '__main__':
    unittest.main()
