import unittest
from multi_platform_search.models import SearchResult
from multi_platform_search.service import SearchService

class ResultProvider:
    def __init__(self, platform): self.platform = platform
    def search(self, query, limit): return [SearchResult(self.platform + "-1", self.platform, "Shared tutorial", f"https://{self.platform}.example/video", content_type="video", search_score=.6, extraction_available=True)]
class FailingProvider:
    def search(self, query, limit): raise TimeoutError("timeout")

class IntegrationContracts(unittest.TestCase):
    def test_web_bilibili_youtube_zhihu_and_xhs_contract(self):
        providers = {name: ResultProvider(name) for name in ("web", "bilibili", "youtube", "zhihu", "xiaohongshu")}
        response = SearchService(providers).search("query", platforms=list(providers))
        self.assertEqual(len(response.provider_status), 5)
        self.assertEqual(len(response.results), 1)  # cross-platform title duplicate group
        self.assertTrue(response.results[0].duplicate_group_id)
    def test_web_survives_all_other_provider_failures(self):
        providers = {"web": ResultProvider("web"), "bilibili": FailingProvider(), "youtube": FailingProvider(), "zhihu": FailingProvider(), "xiaohongshu": FailingProvider()}
        response = SearchService(providers).search("query", platforms=list(providers))
        self.assertEqual(response.provider_status[0].status, "success")
        self.assertEqual(len(response.results), 1)
