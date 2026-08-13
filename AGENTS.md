# AGENTS.md — scholarship.ummanitarian.org

> File ini dibaca otomatis oleh agent AI (Claude Code, Hermes, dll.) saat membuka repo.
> Baca SELURUH file ini sebelum mengubah apa pun.

## Identitas proyek

- **Katalog beasiswa PhD niche kemanusiaan** (humanitarian studies, conflict health, global health, IHL, disaster management), sumber otomatis 50+ portal.
- **URL target:** scholarship.ummanitarian.org (Cloudflare Pages — LIVE di scholarship-ummanitarian.pages.dev; subdomain menunggu CNAME, lihat HANDOVER.md)
- **Repo:** github.com/putrosm/scholarship-ummanitarian — branch `main` satu-satunya. **Repo publik — jangan pernah commit credential.**
- **Stack:** frontend statis (HTML/CSS/JS vanilla) + GitHub Actions + DeepSeek (ekstraksi) + Telegram bot (ACC manusia).

## Siapa "Hermes" — baca kalau Prinsipal menyebutnya

- **Hermes** = asisten AI CLI (Nous Research) yang jalan di WSL2 Ubuntu, dipakai Prinsipal untuk otomasi portal lain (HIFDI, IHSC, dll.). Bukan Claude, bukan bagian dari proyek ini.
- WSL2 sedang di-decommission → Hermes akan berhenti. Repo ini tetap hidup, dikerjakan penuh oleh Claude.
- Kalau Prinsipal menyebut "Hermes": kerjakan langsung, jangan menunggu Hermes.

## DEPLOY & CREDENTIALS — sangat penting

- **Jangan pernah menaruh token/credential di repo ini.** Semua sudah diredact di HANDOVER.md. Credential asli hanya di: GitHub Secrets repo ini + penyimpanan aman operator.
- Workflow memakai `secrets.GH_TOKEN`, `DEEPSEEK_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` — jangan hardcode nilai apa pun di file.
- `.github/workflows/` butuh token dengan scope `workflow` — kalau push workflow ditolak, itu masalah scope token, bukan isi file.
- Jangan `git add -A` sembarangan — stage path spesifik. Jangan push data internal (log, backup) yang tidak perlu.

## Alur kerja (jangan diubah tanpa ACC Prinsipal)

```
SENIN 09.00 WIB  → weekly-source.yml: source.py → pending.json → notify_telegram.py (tombol ✅/❌)
SEPANJANG HARI   → operator klik di Telegram
HARIAN 06.00 WIB → daily-poll.yml: poll_approve.py → approved → scholarships.json → commit → deploy
```

## Aturan kerja

- Bahasa laporan: **Indonesia**.
- Artikel/data beasiswa: sumber harus nyata (jangan mengarang beasiswa). `extract_from_knowledge` hanya fallback untuk sumber yang gagal di-fetch.
- Jangan ubah alur kerja (jadwal, format data, struktur JSON) tanpa konfirmasi.
- `data/scholarships.json` dibaca web — pastikan selalu valid JSON.
- Jangan hapus `_headers` — itu config keamanan Cloudflare Pages.

## Setup yang belum selesai (detail di HANDOVER.md bagian 5)

A. Workflow files (token scope `workflow`) → B. GitHub Secrets (4) → C. Cloudflare Pages → D. DNS CNAME → E. Jotform form → F. Affiliate links.

## Verifikasi sebelum push

- JSON valid (`data/*.json`).
- Tidak ada string credential (cari `ghp_`, `sk-`, `AAH` di file yang di-stage).
- Workflow YAML valid (kalau menyentuh `.github/workflows/`).
