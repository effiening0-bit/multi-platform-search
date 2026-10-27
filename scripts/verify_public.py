"""Public HTTPS acceptance with the official MCP client. Outputs no credentials."""
import argparse, asyncio, importlib.metadata, json, os, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def verify(args):
    base=args.base_url.rstrip('/')
    if not base.startswith('https://'): raise SystemExit('HTTPS required')
    token=os.getenv('SERVICE_API_KEY')
    if not token:
        for line in (Path(__file__).resolve().parents[1]/'.env').read_text(encoding='utf-8').splitlines():
            if line.startswith('SERVICE_API_KEY='): token=line.split('=',1)[1].strip()
    if not token: raise SystemExit('SERVICE_API_KEY is missing')
    auth={'Authorization':'Bearer '+token}
    evidence={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'base_url':base,'sdk':importlib.metadata.version('mcp'),'checks':[]}
    def record(name,passed,**details):
        item={'name':name,'passed':bool(passed),**details}; evidence['checks'].append(item)
        print(json.dumps(item),flush=True)
    def summary(data):
        return {'status':data.get('status'),'result_count':len(data.get('results',[])),
                'platforms':sorted({r.get('platform','unknown') for r in data.get('results',[])}),
                'provider_status':[{'provider':p.get('provider'),'status':p.get('status')} for p in data.get('providers',[])],
                'warning_count':len(data.get('warnings',[]))}
    async with httpx.AsyncClient(timeout=120,follow_redirects=True) as client:
        for path in ['/health','/ready']:
            r=await client.get(base+path); body=r.json() if r.status_code==200 else {}
            record(path,r.status_code==200 and body.get('status')=='ok',http_status=r.status_code,release=body.get('release'))
        for label,headers in [('missing',{}),('wrong',{'Authorization':'Bearer invalid-acceptance-token'}),('missing_scheme',{'Authorization':token})]:
            for path in ['/v1/search','/mcp/']:
                r=await client.post(base+path,headers=headers,json={'query':'acceptance'})
                record('auth_'+label+path,r.status_code==401,http_status=r.status_code)
        async with client.stream('GET',base+'/mcp/',headers={**auth,'Accept':'application/json, text/event-stream'}) as r:
            record('mcp_endpoint_no_421',r.status_code not in [401,404,421,500,502,503],http_status=r.status_code)
        r=await client.post(base+'/v1/search',headers=auth,json={'query':'Zotero reference manager official','mode':'quick','platforms':['web'],'max_results':3})
        body=r.json() if r.status_code==200 else {}
        record('http_search',r.status_code==200 and bool(body.get('results')),http_status=r.status_code,**summary(body))
    try:
        async with streamablehttp_client(base+'/mcp/',headers=auth,timeout=120,sse_read_timeout=120) as streams:
            async with ClientSession(streams[0],streams[1],read_timeout_seconds=timedelta(seconds=120)) as session:
                init=await session.initialize()
                record('mcp_initialize',True,protocol=init.protocolVersion,server=init.serverInfo.name,server_version=init.serverInfo.version)
                tools=await session.list_tools(); names=sorted(t.name for t in tools.tools)
                record('mcp_tools_list',{'multi_platform_search','search_platform'}.issubset(names),tools=names)
                record('mcp_read_only_annotations',all(t.annotations and t.annotations.readOnlyHint and not t.annotations.destructiveHint for t in tools.tools))
                for name,arguments in [('multi_platform_search',{'query':'Zotero reference manager tutorial','mode':'quick','platforms':['web','exa','youtube','bilibili','zhihu','xiaohongshu'],'max_results':12}),('search_platform',{'query':'Zotero tutorial','platform':'youtube','mode':'quick'})]:
                    result=await session.call_tool(name,arguments=arguments)
                    body=result.structuredContent or next((json.loads(c.text) for c in result.content if getattr(c,'type',None)=='text'),{})
                    record(name,not result.isError and bool(body.get('results')),**summary(body))
    except Exception as exc: record('mcp_protocol',False,error_type=type(exc).__name__)
    if args.rate_limit:
        async with httpx.AsyncClient(timeout=30) as client:
            for n in range(65):
                r=await client.get(base+'/v1/providers',headers=auth)
                if r.status_code==429: break
            record('rate_limit',r.status_code==429 and bool(r.headers.get('Retry-After')),requests=n+1,http_status=r.status_code,retry_after=r.headers.get('Retry-After'))
    evidence['passed']=all(c['passed'] for c in evidence['checks'])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
    return evidence['passed']

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--base-url',required=True); p.add_argument('--output',type=Path,required=True); p.add_argument('--rate-limit',action='store_true')
    raise SystemExit(0 if asyncio.run(verify(p.parse_args())) else 1)
