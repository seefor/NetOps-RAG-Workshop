import unittest
from netops_rag.filters import build_where_filter
class FilterTests(unittest.TestCase):
    def test_single(self): self.assertEqual(build_where_filter({"status":["active"]}), {"status":"active"})
    def test_or_within_field_and_across_fields(self):
        self.assertEqual(build_where_filter({"status":["active","completed"],"service":["bgp"]}), {"$and":[{"status":{"$in":["active","completed"]}},{"service":"bgp"}]})
if __name__ == "__main__": unittest.main()
