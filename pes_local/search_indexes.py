# -*- coding:utf-8 -*-
from haystack import indexes
from pes.search_indexes import WordIndex as BaseWordIndex


# If you dont want to use the default index, please comment the following
# lines and write your own indexes




class WordIndex(BaseWordIndex, indexes.Indexable):
    pass
