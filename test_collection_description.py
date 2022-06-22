import unittest
import CollectionDescription

class TsetColl(unittest.TestCase):
    def test_getId(self):
        cd = CollectionDescription.CollectionDescription(1,1)
        self.assertEqual(CollectionDescription.CollectionDescription.getId(cd), 1)
        cd = CollectionDescription.CollectionDescription("string",1)
        self.assertEqual(CollectionDescription.CollectionDescription.getId(cd), "string")
        cd = CollectionDescription.CollectionDescription(None,1)
        self.assertEqual(CollectionDescription.CollectionDescription.getId(cd), None)
        cd = CollectionDescription.CollectionDescription(object,1)
        self.assertEqual(CollectionDescription.CollectionDescription.getId(cd), object)
    def test_getdataset(self):
        cd = CollectionDescription.CollectionDescription(1,1)
        self.assertEqual(CollectionDescription.CollectionDescription.getDataset(cd), 1)
        cd = CollectionDescription.CollectionDescription(1,"string")
        self.assertEqual(CollectionDescription.CollectionDescription.getDataset(cd), "string")
        cd = CollectionDescription.CollectionDescription(1,None)
        self.assertEqual(CollectionDescription.CollectionDescription.getDataset(cd), None)
        cd = CollectionDescription.CollectionDescription(1, object)
        self.assertEqual(CollectionDescription.CollectionDescription.getDataset(cd), object)



if __name__ == '__main__':
        unittest.main()