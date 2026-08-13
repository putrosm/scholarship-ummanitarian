import os, json, requests
from datetime import datetime

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
API = f"https://api.telegram.org/bot{TOKEN}"


def send(text, keyboard=None):
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        payload["reply_markup"] = {"inline_keyboard": keyboard}
    requests.post(f"{API}/sendMessage", json=payload, timeout=15)


def main():
    try:
        with open('data/pending.json') as f:
            pending = json.load(f)
    except:
        pending = []

    unsent = [s for s in pending if not s.get('sent_to_telegram')]

    if not unsent:
        send("🎓 *Weekly Scholarship Scan*\n\nNo new scholarships this week.")
        return

    send(f"🎓 *Weekly Scholarship Scan*\n\n*{len(unsent)} new scholarships* pending your review.\nApprove or reject each below:")

    for s in unsent:
        emoji = {"Open":"🟢","Closing Soon":"🟡","Expired":"🔴","Unknown":"⚪"}.get(s.get('status',''),"⚪")
        funding = {'fully_funded':'Fully Funded','partial':'Partial','unknown':'Check page'}.get(s.get('funding_type',''),'—')
        deadline = s.get('deadline') or 'No deadline'
        tags = ', '.join(s.get('field_tags',[])[:3]) or '—'

        text = (
            f"*{s.get('title','—')}*\n"
            f"🏛 {s.get('university','—')} | 🌍 {s.get('country','—')}\n"
            f"{emoji} {s.get('status','—')} | 📅 {deadline}\n"
            f"💰 {funding} | 🏷 {tags}\n\n"
            f"{s.get('summary','')[:300]}"
        )
        keyboard = [[
            {"text":"✅ Approve","callback_data":f"approve_{s['id']}"},
            {"text":"❌ Reject","callback_data":f"reject_{s['id']}"}
        ]]
        send(text, keyboard)
        s['sent_to_telegram'] = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open('data/pending.json','w') as f:
        json.dump(pending, f, indent=2, ensure_ascii=False)

    print(f"Sent {len(unsent)} scholarships to Telegram")


if __name__ == "__main__":
    main()
