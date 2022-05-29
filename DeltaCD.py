# DeltaCD.py

import CollectionDescription


class DeltaCD:
    def __init__(self, add, update):
        self.add = add
        self.update = update


DeltaCD.add = list(CollectionDescription)
DeltaCD.update = list(CollectionDescription)
