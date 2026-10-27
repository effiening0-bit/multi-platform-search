import json, os, unittest
from unittest.mock import patch
from multi_platform_search.models import SearchResult
from multi_platform_search.providers import BilibiliProvider, TavilyProvider

class Response:
    def __init__(self, payload): self.payload=payload
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def read(self): return json.dumps(self.payload).encode()

def candidate():
    return SearchResult('fallback-1','bilibili','Zotero tutorial','https://www.bilibili.com/video/BVdemo')

class BilibiliFallbackTests(unittest.TestCase):
    def setUp(self):
        self.env=patch.dict(os.environ,{'TAVILY_API_KEY':'test-key-for-unit-tests'}); self.env.start()
    def tearDown(self): self.env.stop()

    def test_http_failure_uses_domain_scoped_tavily(self):
        with patch('multi_platform_search.providers.urlopen',side_effect=OSError('blocked')), patch.object(TavilyProvider,'search',return_value=[candidate()]) as index:
            result=BilibiliProvider().search('Zotero tutorial',3)
        index.assert_called_once_with('Zotero tutorial',3)
        self.assertEqual(result[0].metadata['fallback_reason'],'public_api_failure')

    def test_api_rejection_and_empty_success_both_fall_back(self):
        for payload,reason in [({'code':-412},'public_api_rejected'),({'code':0,'data':{'result':[]}},'public_api_empty')]:
            with self.subTest(reason=reason), patch('multi_platform_search.providers.urlopen',return_value=Response(payload)), patch.object(TavilyProvider,'search',return_value=[candidate()]) as index:
                result=BilibiliProvider().search('Zotero tutorial',3)
                index.assert_called_once()
                self.assertEqual(result[0].metadata['fallback_reason'],reason)

    def test_direct_results_do_not_spend_tavily_quota(self):
        payload={'code':0,'data':{'result':[{'bvid':'BVdemo','title':'Zotero','play':12}]}}
        with patch('multi_platform_search.providers.urlopen',return_value=Response(payload)), patch.object(TavilyProvider,'search') as index:
            result=BilibiliProvider().search('Zotero tutorial',3)
        index.assert_not_called(); self.assertEqual(len(result),1)

    def test_tavily_failure_or_zero_results_uses_rss_once(self):
        for behavior in [{'side_effect':TimeoutError('timeout')},{'return_value':[]}]:
            with patch('multi_platform_search.providers.urlopen',side_effect=OSError('blocked')), patch.object(TavilyProvider,'search',**behavior), patch('multi_platform_search.providers.BingRssProvider.search',return_value=[candidate()]) as rss:
                self.assertEqual(len(BilibiliProvider().search('Zotero',3)),1)
                rss.assert_called_once_with('Zotero',3)

    def test_no_tavily_key_keeps_free_rss_fallback(self):
        with patch.dict(os.environ,{'TAVILY_API_KEY':''}), patch('multi_platform_search.providers.urlopen',side_effect=OSError('blocked')), patch.object(TavilyProvider,'search') as index, patch('multi_platform_search.providers.BingRssProvider.search',return_value=[]) as rss:
            self.assertEqual(BilibiliProvider().search('Zotero',3),[])
        index.assert_not_called(); rss.assert_called_once()

    def test_domain_filter_metadata_and_basic_cost_are_explicit(self):
        response={'results':[{'title':'wrong domain','url':'https://bilibili.com.evil.example/video/a'}, {'title':'valid','url':'https://www.bilibili.com/video/BVdemo'}, {'title':'wrong scheme','url':'javascript:alert(1)'}]}
        with patch('multi_platform_search.providers.urlopen',return_value=Response(response)) as opened:
            result=TavilyProvider(site='bilibili.com',name='bilibili').search('Zotero',3)
        sent=json.loads(opened.call_args.args[0].data)
        self.assertEqual(sent['include_domains'],['bilibili.com'])
        self.assertEqual(sent['search_depth'],'basic'); self.assertFalse(sent['auto_parameters'])
        self.assertFalse(sent['include_raw_content']); self.assertEqual(len(result),1)
        self.assertEqual(result[0].platform,'bilibili'); self.assertEqual(result[0].content_type,'video')
        self.assertEqual(result[0].metadata,{'source_type':'public_index_fallback','provider':'tavily'})
