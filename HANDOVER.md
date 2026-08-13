# HANDOVER — scholarship.ummanitarian.org

> ⚠️ CREDENTIALS DIREDACT — repo publik. Credential asli hanya di GitHub Secrets repo ini + penyimpanan aman operator.
> JANGAN pernah menulis token/credential di file repo. JANGAN paste token ke chat mana pun.
> *Last updated: 2026-08-13*
> *Operator: Putro S. Muhammad (putrosm.darsono@gmail.com)*

---

## 1. GAMBARAN PROYEK

Website pencarian beasiswa PhD niche: humanitarian studies, conflict health, global health, IHL, disaster management.

- **URL production:** `scholarship-ummanitarian.pages.dev` (LIVE ✅)
- **URL target (subdomain):** `scholarship.ummanitarian.org` — belum aktif, tinggal CNAME (bagian 5D)
- **Repo:** `github.com/putrosm/scholarship-ummanitarian` (PUBLIC, branch `main`) — *sebelumnya ummanitarian/scholarship-ummanitarian, sudah ditransfer ke putrosm 2026-08-13*
- **Hosting:** Cloudflare Pages (project `scholarship-ummanitarian`, akun putrosm.darsono@gmail.com)
- **Stack:** frontend statis (HTML/CSS/JS vanilla, no build step) + GitHub Actions + DeepSeek (sourcing) + Telegram bot (ACC manusia) + Cloudflare Pages (deploy)
- **AI asisten aktif:** Claude (Anthropic) — Hermes/Nous sudah tidak aktif (WSL2 decommission)

## 2. STATUS SETUP (2026-08-13 — hampir semua beres)

| Item | Status |
|---|---|
| Repo + frontend + scripts + logo | ✅ |
| Workflow files (`weekly-source.yml`, `daily-poll.yml`) | ✅ terupload |
| GitHub Secrets (6): `DEEPSEEK_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `GH_TOKEN`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | ✅ terisi |
| Auto-deploy workflow → Cloudflare Pages | ✅ (step wrangler di kedua workflow) |
| Cloudflare Pages project + deploy | ✅ LIVE di `scholarship-ummanitarian.pages.dev` |
| Trial end-to-end (sourcing → TG → approve → deploy) | ✅ 8 beasiswa approved tampil |
| CNAME subdomain `scholarship.ummanitarian.org` | ⬜ BELUM — di panel idwebhost (5D) |
| Jotform subscriber form | ⬜ BELUM — form belum dibuat (5E) |
| Affiliate links (Grammarly/Magoosh) | ⬜ opsional (5F) |

## 3. CREDENTIALS — LOKASI PENYIMPANAN

| Item | Lokasi | Catatan |
|---|---|---|
| GitHub token (putrosm) | GitHub Secrets `GH_TOKEN` | scope repo + workflow |
| DeepSeek API key | GitHub Secrets `DEEPSEEK_API_KEY` | platform.deepseek.com |
| Telegram bot token @ummanitarian_bot | GitHub Secrets `TELEGRAM_BOT_TOKEN` | **diganti 2026-08-13** (token lama 401 mati); token baru TIDAK boleh tulis di repo/chat |
| Telegram chat ID | `446614920` (bukan rahasia) | |
| Cloudflare API token | GitHub Secrets `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` | scoped Pages; akun CF = putrosm.darsono@gmail.com |

**PENTING:** Token yang pernah tampil di chat history / repo = dianggap bocor → regenerate. Jangan pernah paste token asli ke chat Claude/Telegram/WebUI. Isi langsung di GitHub Secrets (Settings → Secrets and variables → Actions).

## 4. STRUKTUR REPO

```
.github/workflows/
├── weekly-source.yml     ← Senin 09:00 WIB: sourcing → pending.json → TG → deploy
└── daily-poll.yml        ← Harian 06:00 WIB: proses klik TG → scholarships.json → deploy
assets/logo-dark.png      ← logo hitam (header terang) — U merah #CC0000
assets/logo-white.png     ← logo putih (footer gelap)
data/scholarships.json    ← beasiswa APPROVED — dibaca web
data/pending.json         ← antrean menunggu ACC
data/telegram_offset.json ← state internal bot
scripts/source.py         ← sourcing 50+ portal + ekstraksi DeepSeek
scripts/notify_telegram.py← kirim batch ke TG + tombol ✅/❌
scripts/poll_approve.py   ← proses klik → approved → scholarships.json
index.html / style.css / app.js  ← frontend (EN default + toggle ID)
_headers                  ← config keamanan Cloudflare Pages
```

## 5. ALUR KERJA NORMAL (sudah jalan otomatis)

```
SENIN 09.00 WIB → weekly-source: source.py (50+ portal → DeepSeek) → pending.json → notify TG (tombol ACC) → auto-deploy CF Pages
SEPANJANG HARI  → operator klik ✅/❌ di Telegram
HARIAN 06.00 WIB → daily-poll: poll_approve.py → approved masuk scholarships.json → auto-deploy → website live
```

**Trigger manual** (tanpa tunggu jadwal): Repo → Actions → workflow → Run workflow. Atau via API dispatch (pakai `GH_TOKEN`).

## 6. SISA TUGAS (untuk Claude)

### 5D. CNAME subdomain (butuh panel idwebhost — DNS ummanitarian.org di idwebhost, BUKAN Cloudflare)
Tambah record DNS di panel idwebhost/cPanel untuk `ummanitarian.org`:
- Type: `CNAME`, Name: `scholarship`, Target: `scholarship-ummanitarian.pages.dev`
- Contoh yang sudah jalan: `insight.ummanitarian.org` → CNAME → `ummanitarian-insight.pages.dev`
- Setelah propagate (~5-15 menit), di Cloudflare Pages → project → Custom domains → pastikan `scholarship.ummanitarian.org` terverifikasi (sudah ditambahkan 2026-08-13, status menunggu DNS)

### 5E. Jotform subscriber form
1. Buat form di Jotform (akun `liqihuang03@...` — KONFIRMASI pemiliknya dengan Prinsipal; kalau bukan milik Prinsipal, buat akun Jotform baru gratis)
2. Field: Nama lengkap, Email, Nomor WhatsApp, Field of interest (checkbox: Humanitarian Studies, Conflict Health, Global Health, IHL, Disaster Management, Forced Migration, MHPSS)
3. Ambil embed code → ganti placeholder di `index.html` (cari `FORM_ID_HERE` / `data-src`) → commit → push → auto-deploy
4. Jangan lupa: `#jotform-placeholder` di-hide saat iframe loaded (lihat app.js)

### 5F. Affiliate links (opsional)
- Grammarly: `https://grammarly.go2cloud.org/SH8a` — ganti dengan link affiliate sendiri kalau ada
- Magoosh: `https://magoosh.com/?utm_source=ummanitarian`

## 7. TROUBLESHOOT

| Masalah | Cek |
|---|---|
| Bot tidak kirim TG | Actions → weekly-source log. Cek `TELEGRAM_BOT_TOKEN` di Secrets (token lama 401 mati). Cek script tidak menandai `sent_to_telegram` palsu: kalau token mati saat kirim, script TETAP lulus (requests tidak raise) — reset `sent_to_telegram` di pending.json lalu jalankan ulang |
| Approve tidak diproses | Actions → daily-poll log. Cek `TELEGRAM_CHAT_ID` = 446614920 |
| Web tidak update setelah approve | Cek auto-deploy step wrangler di workflow (CLOUDFLARE_API_TOKEN/ACCOUNT_ID di Secrets) |
| Sourcing kosong terus | Cek `DEEPSEEK_API_KEY`, saldo DeepSeek (platform.deepseek.com). Reset pending.json → `[]` → trigger manual |
| Push workflow ditolak | `GH_TOKEN` di Secrets harus token putrosm dengan scope `workflow` (bukan token ummanitarian) |

## 8. ONBOARD CLAUDE BARU

Paste ini di awal sesi baru:

```
Lanjutkan proyek scholarship.ummanitarian.org.

Repo: github.com/putrosm/scholarship-ummanitarian (PUBLIC, main)
HANDOVER lengkap: file HANDOVER.md di repo.

Proyek: website beasiswa PhD niche humanitarian/conflict/global health.
Stack: static HTML + GitHub Actions + DeepSeek sourcing + Telegram approval + Cloudflare Pages.
Status: SEMUA JALAN. Live di scholarship-ummanitarian.pages.dev. Trial selesai, 8 beasiswa approved.
Sisa tugas: (1) CNAME scholarship.ummanitarian.org di panel idwebhost — pandu Prinsipal, (2) Jotform form — konfirmasi pemilik akun liqihuang03 dulu, (3) affiliate links opsional.
Credential: JANGAN tulis di repo/chat. Semua di GitHub Secrets. Token Telegram diganti 2026-08-13 — jangan pakai token lama.
Operator: Putro S. Muhammad (putrosm.darsono@gmail.com / @BinDarsono Telegram).
Lanjut dari bagian SETUP di HANDOVER.md.
```

## 9. KONTAK & REFERENSI

- Repo: github.com/putrosm/scholarship-ummanitarian
- DeepSeek: platform.deepseek.com
- Cloudflare: dash.cloudflare.com (akun putrosm.darsono@gmail.com)
- Jotform: jotform.com (akun liqihuang03@... — konfirmasi pemilik)
- Telegram bot: t.me/ummanitarian_bot
- Panel DNS: idwebhost (hosting ummanitarian.org)
