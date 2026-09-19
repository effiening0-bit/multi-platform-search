import os,time,hmac,uuid,hashlib
from contextlib import asynccontextmanager
from collections import defaultdict,deque
from fastapi import FastAPI,Header,HTTPException,Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from multi_platform_search import SearchService
from multi_platform_search.config import load_local_env
from mcp_adapter import app as mcp_app, mcp
load_local_env()
@asynccontextmanager
async def lifespan(_app):
    async with mcp.session_manager.run():
        yield
app=FastAPI(lifespan=lifespan); service=SearchService(); hits=defaultdict(deque)
app.mount('/mcp', mcp_app())
@app.middleware('http')
async def mcp_auth(request: Request, call_next):
    if request.url.path.startswith('/mcp'):
        try:
            # Reuse the HTTP guard so MCP has identical bearer-auth and
            # sliding-window rate-limit semantics.
            guard(request.headers.get('authorization'))
        except HTTPException as exc:
            return JSONResponse({'error':exc.detail},status_code=exc.status_code,headers=exc.headers or {})
    return await call_next(request)
class RequestModel(BaseModel): query:str=Field(min_length=1,max_length=500); mode:str='normal'; platforms:list[str]|None=None; max_results:int|None=Field(None,ge=1,le=30)
def guard(header):
    expected=os.getenv('SERVICE_API_KEY',''); auth=os.getenv('SERVICE_AUTH_REQUIRED','true').lower()=='true'
    if auth and (not expected or not header or not hmac.compare_digest(header.removeprefix('Bearer '),expected)): raise HTTPException(401,'unauthorized')
    key=hashlib.sha256((header or 'local').encode()).hexdigest(); now=time.monotonic(); q=hits[key]
    while q and now-q[0]>60:q.popleft()
    if len(q)>=int(os.getenv('RATE_LIMIT_REQUESTS_PER_MINUTE','30')): raise HTTPException(429,'rate_limited',headers={'Retry-After':'60'})
    q.append(now)
@app.get('/health')
def health(): return {'status':'ok'}
@app.get('/ready')
def ready(): return {'status':'ok','initialized':True}
@app.get('/v1/providers')
def providers(authorization:str|None=Header(None)):
    guard(authorization); return [{'provider':n,'configured':bool(os.getenv({'web':'TAVILY_API_KEY','youtube':'YOUTUBE_API_KEY','exa':'EXA_API_KEY'}.get(n,''))),'enabled':True,'source_type':'third_party_api'} for n in service.providers]
@app.post('/v1/search')
def search(body:RequestModel,authorization:str|None=Header(None)):
    guard(authorization); start=time.perf_counter(); x=service.search(body.query,body.mode,body.platforms); results=x.results[:body.max_results] if body.max_results else x.results
    return {'request_id':str(uuid.uuid4()),'status':'success','query':body.query,'mode':body.mode,'results':[r.to_dict() for r in results],'providers':[s.__dict__ for s in x.provider_status],'warnings':x.warnings,'meta':{'latency_ms':round((time.perf_counter()-start)*1000),'candidate_count':len(x.results),'deduped_count':len(x.results)}}
@app.post('/v1/search/platform')
def platform(body:RequestModel,authorization:str|None=Header(None)):
    if not body.platforms or len(body.platforms)!=1: raise HTTPException(422,'one platform required')
    return search(body,authorization)
