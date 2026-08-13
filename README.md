# scholarship.ummanitarian.org

Katalog beasiswa **PhD niche kemanusiaan** — humanitarian studies, conflict health, global health, IHL, disaster management. Sumber otomatis dari 50+ portal pemberi beasiswa, di-ACC via Telegram sebelum tayang.

## Cara kerja

1. **Senin 09:00 WIB** — GitHub Actions menjalankan `scripts/source.py`: crawl 50+ portal → DeepSeek ekstrak data → simpan ke `data/pending.json` → kirim batch ke Telegram via bot (tiap beasiswa: tombol ✅ Approve / ❌ Reject).
2. **Sepanjang hari** — operator klik tombol di Telegram.
3. **Setiap hari 06:00 WIB** — `scripts/poll_approve.py` memproses klik → yang approved masuk `data/scholarships.json` → commit → Cloudflare Pages rebuild otomatis.

## Struktur

```
.github/workflows/        # weekly-source.yml (Senin) + daily-poll.yml (harian)
assets/                   # logo
data/
  scholarships.json       # beasiswa approved — dibaca web
  pending.json            # antrean menunggu ACC
  telegram_offset.json    # state internal bot
scripts/
  source.py               # sourcing + ekstraksi DeepSeek
  notify_telegram.py      # kirim batch ke Telegram
  poll_approve.py         # proses klik Approve/Reject
index.html / style.css / app.js   # frontend statis
_headers                  # config Cloudflare Pages
```

## Setup

Lengkap di `HANDOVER.md` bagian 5 (workflow files, GitHub Secrets, Cloudflare Pages, DNS, Jotform, affiliate). **Credential jangan pernah disimpan di repo ini** — repo publik, semua token diredact.

## Status (2026-08-13)

- [x] Repo + frontend + scripts + logo
- [ ] Workflow files terupload (butuh token scope `workflow`)
- [ ] GitHub Secrets (4)
- [ ] Cloudflare Pages connect
- [ ] DNS `scholarship.ummanitarian.org`
- [ ] Jotform subscriber form
- [ ] Affiliate links
