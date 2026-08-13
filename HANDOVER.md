> ⚠️ CREDENTIALS DIREDACT dari file ini karena repo publik.
> Simpan credentials asli di tempat aman (password manager / catatan pribadi terenkripsi).
> Onboard Claude baru: paste isi file ini + tambahkan credentials dari catatan Anda.

# HANDOVER — scholarship.ummanitarian.org
*Last updated: 2026-08-13*
*Operator: Putro S. Muhammad (putrosm.darsono@gmail.com)*

---

## 1. GAMBARAN PROYEK

Website pencarian beasiswa PhD niche: humanitarian studies, conflict health, global health, IHL, disaster management.

- **URL target:** scholarship.ummanitarian.org
- **Repo:** github.com/ummanitarian/scholarship-ummanitarian
- **Hosting:** Cloudflare Pages (belum disambung — lihat bagian SETUP BELUM SELESAI)
- **AI asisten aktif:** Claude (Anthropic) — bukan Hermes/Nous

---

## 2. CREDENTIALS

| Item | Value | Reset di |
|---|---|---|
| GitHub token | `ghp_XXXX_REDACTED — lihat penyimpanan aman Anda` | github.com/settings/tokens |
| DeepSeek API key | `sk-XXXX_REDACTED — lihat penyimpanan aman Anda` | platform.deepseek.com |
| Telegram bot token | `XXXX_REDACTED — lihat penyimpanan aman Anda` | t.me/BotFather → /mybots |
| Telegram bot | @ummanitarian_bot | — |
| Telegram chat ID Anda | `XXXX_REDACTED` | kirim pesan ke @userinfobot |
| Jotform akun | liqihuang03@... | jotform.com |
| GitHub akun | ummanitarian (email: putrosm.darsono@gmail.com) | github.com/settings |

**PENTING:** Credentials di atas ada di chat history Claude. Setelah setup selesai, generate ulang semua token untuk keamanan.

---

## 3. STRUKTUR REPO

```
scholarship-ummanitarian/
├── .github/workflows/
│   ├── weekly-source.yml     ← jalan tiap Senin 09.00 WIB
│   └── daily-poll.yml        ← jalan tiap hari 06.00 WIB
├── assets/
│   ├── logo-dark.jpg         ← logo hitam (untuk header terang)
│   └── logo-white.png        ← logo putih (untuk footer gelap)
├── data/
│   ├── scholarships.json     ← beasiswa APPROVED — dibaca web
│   ├── pending.json          ← beasiswa pending approval Anda
│   └── telegram_offset.json  ← state internal bot Telegram
├── scripts/
│   ├── source.py             ← sourcing 50+ portal → pending.json
│   ├── notify_telegram.py    ← kirim batch ke Telegram
│   ├── poll_approve.py       ← proses klik Approve/Reject Anda
│   └── requirements.txt      ← requests, beautifulsoup4
├── index.html                ← halaman utama web
├── style.css                 ← styling (brand UMMANITARIAN)
├── app.js                    ← filter/search/render kartu
└── _headers                  ← Cloudflare Pages config
```

---

## 4. ALUR KERJA NORMAL

```
SENIN 09.00 WIB
GitHub Actions jalankan weekly-source.yml
→ source.py fetch 50+ portal beasiswa
→ DeepSeek ekstrak data terstruktur
→ hasil masuk data/pending.json
→ notify_telegram.py kirim batch ke Telegram Anda
   (tiap beasiswa = 1 pesan + tombol ✅ Approve / ❌ Reject)

SEPANJANG HARI
Anda buka Telegram → klik ✅ atau ❌ per beasiswa

SETIAP HARI 06.00 WIB
GitHub Actions jalankan daily-poll.yml
→ poll_approve.py cek klik Anda di Telegram
→ yang di-approve → masuk data/scholarships.json
→ git commit → Cloudflare Pages rebuild otomatis
→ web live terupdate
→ Bot kirim konfirmasi: "X approved, Y rejected. Website updated."
```

---

## 5. SETUP YANG BELUM SELESAI

### A. Workflow files — PRIORITAS PERTAMA
Token GitHub belum punya scope `workflow`. Lakukan:
1. github.com/settings/tokens → edit token → centang `workflow` → Save
2. Repo → Add file → Create new file
3. Buat `.github/workflows/weekly-source.yml` (isi ada di bawah)
4. Buat `.github/workflows/daily-poll.yml` (isi ada di bawah)

**Isi weekly-source.yml:**
```yaml
name: Weekly Scholarship Sourcing
on:
  schedule:
    - cron: '0 2 * * 1'
  workflow_dispatch:
jobs:
  source:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GH_TOKEN }}
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r scripts/requirements.txt
      - run: python scripts/source.py
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
      - run: python scripts/notify_telegram.py
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      - run: |
          git config user.name "scholarship-bot"
          git config user.email "bot@ummanitarian.org"
          git add data/pending.json
          git diff --staged --quiet || git commit -m "chore: pending scholarships $(date +%Y-%m-%d)"
          git push
```

**Isi daily-poll.yml:**
```yaml
name: Daily Approval Poll
on:
  schedule:
    - cron: '0 23 * * *'
  workflow_dispatch:
jobs:
  poll:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GH_TOKEN }}
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r scripts/requirements.txt
      - run: python scripts/poll_approve.py
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      - run: |
          git config user.name "scholarship-bot"
          git config user.email "bot@ummanitarian.org"
          git add data/scholarships.json data/pending.json data/telegram_offset.json
          git diff --staged --quiet || git commit -m "chore: approved scholarships $(date +%Y-%m-%d)"
          git push
```

### B. GitHub Secrets
Repo → Settings → Secrets and variables → Actions → New repository secret:

| Name | Value |
|---|---|
| `DEEPSEEK_API_KEY` | `sk-XXXX_REDACTED — lihat penyimpanan aman Anda` |
| `TELEGRAM_BOT_TOKEN` | `XXXX_REDACTED — lihat penyimpanan aman Anda` |
| `TELEGRAM_CHAT_ID` | `XXXX_REDACTED` |
| `GH_TOKEN` | `ghp_XXXX_REDACTED — lihat penyimpanan aman Anda` |

### C. Cloudflare Pages
1. Cloudflare dashboard → Pages → Create project
2. Connect GitHub → pilih repo `ummanitarian/scholarship-ummanitarian`
3. Build settings:
   - Build command: *(kosong)*
   - Build output directory: `/` *(root)*
4. Deploy → dapat URL `scholarship-ummanitarian.pages.dev`

### D. DNS Subdomain
Cloudflare dashboard → DNS → ummanitarian.org:
- Type: `CNAME`
- Name: `scholarship`
- Target: `scholarship-ummanitarian.pages.dev`
- Proxy: ON (orange cloud)

Lalu di Cloudflare Pages → Custom domains → Add → `scholarship.ummanitarian.org`

### E. Jotform Subscriber Form
Buat form baru di Jotform (akun liqihuang03) dengan field:
- Nama lengkap
- Email
- Nomor WhatsApp
- Field of interest (checkbox: Humanitarian Studies, Conflict Health, Global Health, IHL, Disaster Management, Forced Migration, MHPSS)

Setelah dibuat → ambil embed code → paste ke `index.html` ganti bagian:
```
src="https://form.jotform.com/FORM_ID_HERE"
```

### F. Affiliate Links
Di `index.html`, ganti placeholder:
- Grammarly: daftar di grammarly.com/affiliates → dapat link → ganti `https://grammarly.go2cloud.org/SH8a`
- Magoosh: daftar di magoosh.com/affiliates → dapat link → ganti URL Magoosh

---

## 6. OPERASIONAL MANUAL

### Trigger sourcing sekarang (tanpa tunggu Senin)
Repo → Actions → Weekly Scholarship Sourcing → Run workflow

### Trigger approval sekarang
Repo → Actions → Daily Approval Poll → Run workflow

### Tambah beasiswa manual
Edit `data/scholarships.json` di GitHub web UI — tambah objek baru dengan struktur:
```json
{
  "id": "buat-unik-12char",
  "title": "Nama Beasiswa",
  "university": "Nama Universitas",
  "country": "Negara",
  "field_tags": ["humanitarian studies"],
  "funding_type": "fully_funded",
  "deadline": "2026-12-31",
  "status": "Open",
  "official_link": "https://...",
  "language_of_instruction": "English",
  "summary": "Deskripsi singkat.",
  "key_figures": [],
  "sponsored": false,
  "date_sourced": "2026-08-13"
}
```

### Tandai beasiswa sebagai sponsored
Edit `scholarships.json` → cari beasiswa → ubah `"sponsored": false` → `"sponsored": true` → commit.

---

## 7. TROUBLESHOOT

| Masalah | Cek |
|---|---|
| Bot tidak kirim ke Telegram | Actions → weekly-source → lihat log. Cek TELEGRAM_BOT_TOKEN di Secrets. |
| Approve tidak diproses | Actions → daily-poll → lihat log. Cek TELEGRAM_CHAT_ID = XXXX_REDACTED. |
| Web tidak update setelah approve | Cloudflare Pages → Deployments → apakah ada deployment baru? Kalau tidak, cek apakah git push di workflow berhasil. |
| Sourcing tidak temukan beasiswa | Actions → weekly-source → log source.py. Cek DEEPSEEK_API_KEY. Cek saldo DeepSeek di platform.deepseek.com. |
| pending.json kosong terus | Kemungkinan semua beasiswa sudah ada (duplicate). Reset: kosongkan `data/pending.json` → `[]` → commit → trigger manual. |

---

## 8. ONBOARD CLAUDE BARU

Paste ini di awal sesi baru:

```
Lanjutkan proyek scholarship.ummanitarian.org.

Repo: github.com/ummanitarian/scholarship-ummanitarian
HANDOVER lengkap: lihat file HANDOVER.md di repo.

Proyek: website beasiswa PhD niche humanitarian/conflict/global health.
Stack: static HTML + GitHub Actions + DeepSeek sourcing + Telegram approval.
PRD sudah acc. Build sudah selesai kecuali bagian SETUP BELUM SELESAI di HANDOVER.md.
Operator: Putro S. Muhammad (putrosm.darsono@gmail.com / @BinDarsono Telegram).
Lanjut dari mana kita berhenti.
```

---

## 9. KONTAK & REFERENSI

- Repo: github.com/ummanitarian/scholarship-ummanitarian
- DeepSeek dashboard: platform.deepseek.com
- Cloudflare dashboard: dash.cloudflare.com
- Jotform: jotform.com (akun liqihuang03)
- Telegram bot: t.me/ummanitarian_bot
