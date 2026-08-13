import os, json, requests
from datetime import datetime

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = int(os.environ['TELEGRAM_CHAT_ID'])
API = f"https://api.telegram.org/bot{TOKEN}"


def get_updates(offset):
    try:
        r = requests.get(f"{API}/getUpdates", params={"offset":offset,"timeout":5}, timeout=15)
        return r.json().get('result', [])
    except:
        return []


def answer_callback(cb_id, text):
    requests.post(f"{API}/answerCallbackQuery", json={"callback_query_id":cb_id,"text":text}, timeout=10)


def send(text):
    requests.post(f"{API}/sendMessage", json={"chat_id":CHAT_ID,"text":text,"parse_mode":"Markdown"}, timeout=10)


def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return default


def save_json(path, data):
    with open(path,'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    offset_data = load_json('data/telegram_offset.json', {"offset":0})
    offset = offset_data.get('offset', 0)
    pending = load_json('data/pending.json', [])
    approved = load_json('data/scholarships.json', [])

    updates = get_updates(offset)
    approved_count = 0
    rejected_count = 0
    new_offset = offset

    for update in updates:
        new_offset = update['update_id'] + 1
        if 'callback_query' not in update:
            continue

        cb = update['callback_query']
        if cb['from']['id'] != CHAT_ID:
            continue

        data = cb.get('data','')

        if data.startswith('approve_'):
            sid = data[8:]
            for s in pending:
                if s['id'] == sid and s.get('review_status') == 'pending':
                    s['review_status'] = 'approved'
                    s['date_approved'] = datetime.now().strftime("%Y-%m-%d")
                    approved.append(s)
                    approved_count += 1
                    answer_callback(cb['id'], "✅ Approved!")
                    break

        elif data.startswith('reject_'):
            sid = data[7:]
            for s in pending:
                if s['id'] == sid and s.get('review_status') == 'pending':
                    s['review_status'] = 'rejected'
                    rejected_count += 1
                    answer_callback(cb['id'], "❌ Rejected")
                    break

    # Save
    pending_remaining = [s for s in pending if s.get('review_status') == 'pending']
    save_json('data/pending.json', pending_remaining)
    save_json('data/scholarships.json', approved)
    save_json('data/telegram_offset.json', {"offset": new_offset})

    if approved_count > 0 or rejected_count > 0:
        send(f"✅ *Update*: {approved_count} approved, {rejected_count} rejected.\nWebsite updated automatically.")
        print(f"Approved: {approved_count} | Rejected: {rejected_count}")
    else:
        print("No new responses")


if __name__ == "__main__":
    main()
