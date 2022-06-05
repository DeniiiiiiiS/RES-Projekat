# DeltaCD.py

import collectionDescription


class DeltaCD:
    def __init__(self):
        self.add_list = []   # Lista u kojoj se nalaze objeki CD koje trebaju da se dodaju u bazu
        self.update_list = []    # Lista u kojoj se nalaze objeki CD koje trebaju da se azuiraju u bazi

    def dodajNovi(self,cd):
        self.add_list.append(cd)
    
    def azuirajPostojeci(self,cd):
        self.update_list.append(cd)

