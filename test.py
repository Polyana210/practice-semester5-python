import unittest
from search import search_phrase

class TestStringMethods(unittest.TestCase):

    def test_1(self):
        search_res = search_phrase("книга")
        self.assertEqual(search_res["Count"], 4)
    
    def test_2(self):
        search_res = search_phrase("папа")
        self.assertEqual(search_res["Count"], 0)
    
    def test_3(self):
        search_res = search_phrase("Книга")
        self.assertEqual(search_res["Count"], 4)
    
    def test_4(self):
        search_res = search_phrase("123")
        self.assertEqual(search_res["Count"], 2)
  

if __name__ == '__main__':
    unittest.main()