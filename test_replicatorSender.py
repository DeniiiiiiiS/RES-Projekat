import unittest
import time
import receiverProperty
from sender_functions import konvertuj_u_ReceiverProperty
from sender_functions import Logger

class TestSender(unittest.TestCase):

    def test_Logger(self):
        vreme = time.localtime()
        self.assertEqual(Logger("poruka"),f"{vreme.tm_mday}.{vreme.tm_mon}.{vreme.tm_hour}, {vreme.tm_hour}:{vreme.tm_min}:{vreme.tm_sec}, "+ "poruka"+"\n")
        self.assertEqual(Logger(3),f"{vreme.tm_mday}.{vreme.tm_mon}.{vreme.tm_hour}, {vreme.tm_hour}:{vreme.tm_min}:{vreme.tm_sec}, {3}\n")
        self.assertEqual(Logger(object),f"{vreme.tm_mday}.{vreme.tm_mon}.{vreme.tm_hour}, {vreme.tm_hour}:{vreme.tm_min}:{vreme.tm_sec}, {object}\n")

    def test_konvertuj_u_ReceiverProperty(self):
        self.assertEqual(konvertuj_u_ReceiverProperty(""),"lose")
        self.assertEqual(konvertuj_u_ReceiverProperty(3),"lose")
        self.assertEqual(konvertuj_u_ReceiverProperty(5.77), "lose")
        self.assertEqual(konvertuj_u_ReceiverProperty(object), "lose")
        self.assertEqual(konvertuj_u_ReceiverProperty("3;3;"), "lose")


if __name__ == '__main__':
    unittest.main()