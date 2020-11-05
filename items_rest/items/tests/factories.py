from factory import DictFactory, Sequence
from factory.fuzzy import FuzzyInteger


class ItemDictFactory(DictFactory):

    key = Sequence(lambda n: f"key_{n}")
    value = FuzzyInteger(0, 1000)
