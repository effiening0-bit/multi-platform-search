"""Scan tracked worktree and Git history without printing secret values."""
import json, os, re, subprocess
from pathlib import Path

def git(*args): return subprocess.check_output(['git',*args])

names=['TAVILY_API_KEY','EXA_API_KEY','YOUTUBE_API_KEY','SERVICE_API_KEY']
known=[os.environ[n].encode() for n in names if len(os.environ.get(n,''))>=12]
env=Path('.env')
if env.exists():
    for line in env.read_text(encoding='utf-8').splitlines():
        if '=' in line:
            name,value=line.split('=',1)
            if name in names and len(value.strip())>=12: known.append(value.strip().encode())
pattern=re.compile(rb'(?:tvly-|AIza|ghp_|github_pat_|sk_live_)[A-Za-z0-9_-]{16,}')
findings=[]
files=git('ls-files','-z').decode().rstrip('\0').split('\0')
for f in files:
    p=Path(f)
    if p.is_file() and (pattern.search(p.read_bytes()) or any(k in p.read_bytes() for k in known)):
        findings.append({'scope':'worktree','path':f})
blobs=0
for line in git('rev-list','--objects','--all').decode().splitlines():
    oid,_,name=line.partition(' ')
    if git('cat-file','-t',oid).strip()!=b'blob': continue
    blobs+=1; data=git('cat-file','blob',oid)
    if pattern.search(data) or any(k in data for k in known): findings.append({'scope':'history','path':name,'object':oid})
report={'tracked_files':len(files),'history_blobs':blobs,'env_tracked':'.env' in files,'findings':findings,'passed':not findings and '.env' not in files}
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['passed'] else 1)
