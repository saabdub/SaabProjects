from collections import Counter

class Bag:

    def __init__(self):
        """Create a new empty bag."""
        self.items = Counter()
        self.count = 0

    def size(self) -> int:
        """Return the total number of copies of all items in the bag."""
        return self.count

    def add(self, item: object) -> None:
        """Add one copy of item to the bag.
           Multiple copies are allowed."""
        self.items[item] = self.items[item] + 1
        self.count = self.count + 1

    def discard(self, item: object) -> None:
        """ Remove at most one copy of item from the bag.
            No effect if item is not in the bag.
        """
        if self.items[item] > 0:
            self.items[item] = self.items[item] - 1
            self.count = self.count - 1

    def is_contains(self, item: object) -> bool:
        """ Return True if there is at least
            one copy of item in the bag.
        """
        if self.items[item] > 0:
            return True
        else:
            return False

    def multiplicity(self, item: object) -> int:
        """Return the number of copies of item in the bag.
        Return zero if the item doesn't occur in the bag.
        """
        return Counter(self.items)[item]

    def ordered(self):
        """Return the items ordered by decreasing multiplicity.
        Return a list of (count, item) pairs.
        """
        def value(item):
            return item[0]

        store = []
        # iterate through all the words in the bag
        for item in self.items:
            templist = [self.multiplicity(item), item]
            store.append(templist)

        # sorting the list by the value of the sublist which is the first element in the sublist
        counted_words = sorted(store, key=value, reverse=True)
        return counted_words