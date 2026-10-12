#!/usr/bin/env python3
"""Generate a static Receive page. This does not deploy the page or monitor transactions."""
import argparse,html,json
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument("--config",default="config/wallets.json");p.add_argument("--output",default="receive.html");a=p.parse_args()
 cfg=json.loads(Path(a.config).read_text(encoding="utf-8"));cards=[]
 for w in cfg["wallets"]:
  net=html.escape(w["network"].upper());asset=html.escape(w["asset"]);addr=html.escape(w["address"]);exp=html.escape(w["explorer"],quote=True)
  prefix={"bitcoin":"bitcoin:","ethereum":"ethereum:","arbitrum":"ethereum:","solana":"solana:","tron":"tron:"}.get(w["network"],"")
  uri=html.escape(prefix+w["address"],quote=True)
  cards.append(f'<article><h2>{asset} · {net}</h2><div class="qr" data-uri="{uri}"></div><p class="address">{addr}</p><button data-copy="{addr}">Копировать адрес</button><a href="{exp}" target="_blank" rel="noopener noreferrer">Обозреватель</a><p class="warning">Проверьте сеть и актив. Никогда не передавайте seed phrase или приватный ключ.</p></article>')
 page = """<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Receive</title>
<style>body{font:16px system-ui;max-width:1100px;margin:2rem auto;padding:0 1rem;background:#f7f7f7}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem}article{background:white;border:1px solid #ddd;border-radius:12px;padding:1rem;overflow-wrap:anywhere}.qr{width:180px;height:180px;margin:1rem auto}.address{font:.9rem monospace}.warning{color:#754b00}</style>
<h1>Приём активов</h1><p>Статическая страница. QR требует загрузки qrcodejs с CDN. Перед публикацией декодируйте QR и сверьте адрес.</p><div class="grid">""" + "".join(cards) + """</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script><script>
document.querySelectorAll('.qr').forEach(e=>{if(window.QRCode)new QRCode(e,{text:e.dataset.uri,width:180,height:180});else e.textContent='QR библиотека недоступна';});
document.querySelectorAll('button[data-copy]').forEach(b=>b.onclick=async()=>{try{await navigator.clipboard.writeText(b.dataset.copy);b.textContent='Скопировано'}catch(e){b.textContent='Копирование недоступно'}});
</script></html>"""
 Path(a.output).write_text(page,encoding="utf-8");print("Created",a.output,"— static file only; not deployed.")
if __name__=="__main__":main()
