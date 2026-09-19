import unittest
from multi_platform_search.dedup import deduplicate
from multi_platform_search.models import SearchResult
from multi_platform_search.normalize import normalize_url
from multi_platform_search.routing import classify_intent, rewrite, route
from multi_platform_search.service import SearchService

def item(title, url, score=.5): return SearchResult("x", "web", title, url, search_score=score)
class Failing:
    def search(self, query, limit): raise TimeoutError("test timeout")
class Working:
    def search(self, query, limit): return [item("Result", "https://example.org")]
class CoreTests(unittest.TestCase):
    def test_url_normalize_removes_tracking(self): self.assertEqual(normalize_url("https://www.youtube.com/watch?v=x&utm_source=a"), "https://youtube.com/watch?v=x")
    def test_router_and_rewriter(self):
        self.assertEqual(classify_intent("医学生怎么做文献管理"), "medical_research")
        self.assertEqual(route("iPhone 17 Pro 使用体验")[1][0], "bilibili")
        self.assertIn("教程", rewrite("Zotero", "bilibili", "software_tutorial"))
    def test_deduplication_preserves_group(self):
        results = deduplicate([item("Same title", "https://example.com/a?utm_source=x", .4), item("same title", "https://example.com/a", .8)])
        self.assertEqual((len(results), results[0].duplicate_group_id, results[0].search_score), (1, "dup-001", .8))
    def test_provider_failure_does_not_break_chain(self):
        response = SearchService({"web": Working(), "youtube": Failing()}).search("query", platforms=["web", "youtube"])
        self.assertEqual(len(response.results), 1)
        self.assertEqual([x.status for x in response.provider_status], ["success", "unavailable"])
