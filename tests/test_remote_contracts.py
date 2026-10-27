"""No network/provider calls: verify auth, limit and MCP safety contracts."""
import os, unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
import remote_api
from mcp_adapter import mcp

class RemoteContracts(unittest.TestCase):
    def setUp(self):
        self.env=patch.dict(os.environ,{'SERVICE_API_KEY':'test-only-not-a-real-key','SERVICE_AUTH_REQUIRED':'true','RATE_LIMIT_REQUESTS_PER_MINUTE':'2','RENDER_GIT_COMMIT':'release-under-test'})
        self.env.start(); remote_api.hits.clear()
        self.client=TestClient(remote_api.app)
    def tearDown(self): self.client.close(); self.env.stop(); remote_api.hits.clear()
    def test_bearer_required_for_http_and_mcp(self):
        for path in ['/v1/providers','/mcp/']:
            for header in [None,'Bearer wrong','test-only-not-a-real-key','Basic test-only-not-a-real-key']:
                headers={'Authorization':header} if header else {}
                self.assertEqual(self.client.get(path,headers=headers).status_code,401)
        self.assertEqual(self.client.get('/v1/providers',headers={'Authorization':'bearer test-only-not-a-real-key'}).status_code,200)
    def test_limiter_rejects_metadata_without_provider_cost(self):
        auth={'Authorization':'Bearer test-only-not-a-real-key'}
        self.assertEqual(self.client.get('/v1/providers',headers=auth).status_code,200)
        self.assertEqual(self.client.get('/v1/providers',headers={'Authorization':'bearer test-only-not-a-real-key'}).status_code,200)
        r=self.client.get('/v1/providers',headers=auth)
        self.assertEqual(r.status_code,429); self.assertEqual(r.headers['Retry-After'],'60')
    def test_health_reports_deployed_commit(self):
        for path in ['/health','/ready']:
            self.assertEqual(self.client.get(path).json()['release'],'release-under-test')

class McpAnnotations(unittest.IsolatedAsyncioTestCase):
    async def test_tools_are_read_only(self):
        tools=await mcp.list_tools()
        self.assertEqual({t.name for t in tools},{'multi_platform_search','search_platform'})
        for tool in tools:
            self.assertTrue(tool.annotations.readOnlyHint)
            self.assertFalse(tool.annotations.destructiveHint)
