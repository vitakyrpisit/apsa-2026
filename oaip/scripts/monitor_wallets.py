#!/usr/bin/env python3
"""Read-only wallet monitor; never signs or sends transactions."""
import argparse,json,os,sys,time
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
def now(): return datetime.now(timezone.utc).isoformat()
def req(url,timeout=15,payload=None,headers=None):
 h={"User-Agent":"OAIP-ReadOnly-Monitor/1.0","Accept":"application/json"}
 if headers:h.update(headers)
 data=json.dumps(payload).encode() if payload is not None else None
 if data is not None:h["Content-Type"]="application/json"
 with urlopen(Request(url,data=data,headers=h),timeout=timeout) as r:return json.loads(r.read().decode())
def rec(w,txid,ts,amount,direction,status,sender=None,recipient=None):
 return {"observed_at_utc":now(),"network":w["network"],"wallet":w["address"],"txid":txid,"timestamp":ts,"amount_base_units":str(amount),"asset":w["asset"],"direction":direction,"status":status,"sender":sender,"recipient":recipient,"explorer":w["explorer"]}
def blockscout(w,t):
 j=req(w["api_base"].rstrip("/")+"/addresses/"+w["address"]+"/transactions",t); out=[]
 for x in j.get("items",[]) if isinstance(j,dict) else []:
  f=(x.get("from") or {}).get("hash"); to=(x.get("to") or {}).get("hash")
  if (to or "").lower()==w["address"].lower():out.append(rec(w,x.get("hash"),x.get("timestamp"),x.get("value","0"),"incoming",x.get("status") or x.get("result") or "observed",f,to))
 return out
def bitcoin(w,t):
 j=req(w["api_base"].rstrip("/")+"/address/"+w["address"]+"/txs",t);out=[]
 for x in j if isinstance(j,list) else []:
  st=x.get("status",{})
  for v in x.get("vout",[]):
   if v.get("scriptpubkey_address")==w["address"]:out.append(rec(w,x.get("txid"),st.get("block_time"),v.get("value",0),"incoming","confirmed" if st.get("confirmed") else "unconfirmed",None,w["address"]))
 return out
def solana(w,t):
 j=req(w["rpc_url"],t,{"jsonrpc":"2.0","id":1,"method":"getSignaturesForAddress","params":[w["address"],{"limit":25}]})
 # Signatures alone do not establish amount: mark candidates only.
 return [rec(w,x.get("signature"),x.get("blockTime"),"unknown","candidate",x.get("confirmationStatus","observed")) for x in (j.get("result") or [])]
def tron(w,t):
 key=os.environ.get("TRONGRID_API_KEY");h={"TRON-PRO-API-KEY":key} if key else {}
 u=w["api_base"].rstrip("/")+"/v1/accounts/"+w["address"]+"/transactions?only_to=true&limit=20&order_by=block_timestamp,desc"
 j=req(u,t,headers=h)
 return [rec(w,x.get("txID"),x.get("block_timestamp"),"unknown","candidate","observed",None,w["address"]) for x in (j.get("data") or [])]
FUN={"ethereum":blockscout,"arbitrum":blockscout,"bitcoin":bitcoin,"solana":solana,"tron":tron}
def poll(cfg,out,timeout):
 out.parent.mkdir(parents=True,exist_ok=True);seen=set()
 if out.exists():
  for line in out.read_text(errors="ignore").splitlines():
   try:
    x=json.loads(line);seen.add((x.get("network"),x.get("txid"),x.get("wallet"),x.get("amount_base_units")))
   except Exception:pass
 n=0
 for w in cfg.get("wallets",[]):
  try:
   for x in FUN[w["network"]](w,timeout):
    k=(x["network"],x.get("txid"),x["wallet"],x.get("amount_base_units"))
    if k in seen:continue
    with out.open("a",encoding="utf-8") as f:f.write(json.dumps(x,ensure_ascii=False)+"\n")
    seen.add(k);n+=1;print(json.dumps(x,ensure_ascii=False))
  except (HTTPError,URLError,TimeoutError,OSError,ValueError,KeyError) as e:print(f'ERROR {w.get("network")}: {type(e).__name__}: {e}',file=sys.stderr)
  except Exception as e:print(f'ERROR {w.get("network")}: unexpected {type(e).__name__}: {e}',file=sys.stderr)
 print(f'[{now()}] new_records={n}; journal={out}',file=sys.stderr)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--config",default="config/wallets.json");p.add_argument("--once",action="store_true");p.add_argument("--interval",type=int);p.add_argument("--timeout",type=int);p.add_argument("--output");a=p.parse_args()
 cfg=json.loads(Path(a.config).read_text(encoding="utf-8"));interval=a.interval or cfg.get("poll_interval_seconds",60);timeout=a.timeout or cfg.get("timeout_seconds",15);out=Path(a.output or cfg.get("data_file","data/observed_transactions.jsonl"))
 while True:
  poll(cfg,out,timeout)
  if a.once:break
  time.sleep(max(15,interval))
if __name__=="__main__":main()
