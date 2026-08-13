import os, json, requests, hashlib, time, re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

DEEPSEEK_KEY = os.environ['DEEPSEEK_API_KEY']
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

FIELDS = [
    "humanitarian studies","conflict health","global health",
    "international humanitarian law","disaster management",
    "forced migration","refugee health","humanitarian action",
    "peace and conflict","MHPSS","emergency medicine",
    "humanitarian politics","war and humanitarian response",
    "armed conflict and humanitarian law","humanitarian security",
    "conflict resolution and humanitarian aid","politics of humanitarianism"
]

SOURCES = [
    # Aggregators
    {"url":"https://www.findaphd.com/phds/?Keywords=humanitarian+conflict+health","name":"FindAPhD","fetch":True},
    {"url":"https://scholars4dev.com/category/scholarships-for-development/","name":"Scholars4Dev","fetch":True},
    {"url":"https://opportunitydesk.org/category/scholarships/phd-scholarships/","name":"OpportunityDesk","fetch":True},
    {"url":"https://www.phdportal.eu/search/?d=1&keywords=humanitarian","name":"PhDPortal","fetch":True},
    {"url":"https://reliefweb.int/jobs?type=Scholarship","name":"ReliefWeb","fetch":True},
    {"url":"https://euraxess.ec.europa.eu/jobs/search?query=humanitarian","name":"EURAXESS","fetch":True},
    # Europe West
    {"url":"https://www.daad.de/en/studying-in-germany/scholarships/","name":"DAAD","fetch":True},
    {"url":"https://www.nuffic.nl/en/subjects/scholarships","name":"NUFFIC","fetch":True},
    {"url":"https://si.se/en/apply/scholarships/","name":"Swedish Institute","fetch":True},
    {"url":"https://www.campusfrance.org/en/scholarship","name":"Campus France","fetch":True},
    {"url":"https://www.norad.no/en/front/funding/scholarships/","name":"NORAD","fetch":True},
    {"url":"https://www.eur-lex.europa.eu","name":"Erasmus Mundus","fetch":False},
    {"url":"https://www.boell.de/en/foundation/scholarships","name":"Heinrich Böll","fetch":True},
    {"url":"https://www.fes.de/en/","name":"Friedrich Ebert","fetch":True},
    # Nordic
    {"url":"https://www.edufi.fi/en/scholarships/","name":"EDUFI Finland","fetch":True},
    {"url":"https://www.sida.se/en/for-partners/resources-for-partners/scholarships","name":"SIDA Sweden","fetch":True},
    {"url":"https://www.uio.no/english/research/phd/","name":"Univ Oslo","fetch":True},
    {"url":"https://www.ku.dk/english/research/phd/","name":"Univ Copenhagen","fetch":True},
    # East/Central Europe
    {"url":"https://stipendiumhungaricum.hu/apply/","name":"Stipendium Hungaricum","fetch":True},
    {"url":"https://nawa.gov.pl/en/students/scholarship-programmes","name":"NAWA Poland","fetch":True},
    {"url":"https://www.dzs.hr/en/find-scholarship/scholarships-of-the-republic-of-croatia/","name":"Croatia Gov","fetch":True},
    {"url":"https://www.scholarshipdb.net/scholarships-in/Humanitarian-Studies","name":"ScholarshipDB","fetch":True},
    # Conflict/IHL specific
    {"url":"https://www.graduateinstitute.ch/admissions/financial-aid","name":"Graduate Institute Geneva","fetch":True},
    {"url":"https://www.geneva-academy.ch/study-programmes","name":"Geneva Academy IHL","fetch":True},
    {"url":"https://www.berghof-foundation.org/en/","name":"Berghof Foundation","fetch":True},
    {"url":"https://www.ceu.edu/admissions/financial-aid","name":"CEU Vienna","fetch":True},
    # Islamic / Middle East
    {"url":"https://www.isdb.org/scholarship-programs","name":"IsDB","fetch":True},
    {"url":"https://turkiyeburslari.gov.tr/en","name":"Türkiye Bursları","fetch":True},
    {"url":"https://www.qf.org.qa/education","name":"Qatar Foundation","fetch":False},
    {"url":"https://kfas.org.kw/en-us/scholarships","name":"Kuwait Foundation","fetch":True},
    # Global Health specific
    {"url":"https://wellcome.org/grant-funding/schemes","name":"Wellcome Trust","fetch":True},
    {"url":"https://www.fic.nih.gov/Programs/Pages/scholars-fellows-international.aspx","name":"NIH Fogarty","fetch":True},
    {"url":"https://www.who.int/scholarships","name":"WHO-TDR","fetch":True},
    {"url":"https://gcgh.grandchallenges.org/about/grants","name":"Gates Grand Challenges","fetch":True},
    {"url":"https://www.akdn.org/our-agencies/aga-khan-foundation/social-development/scholarships","name":"Aga Khan","fetch":True},
    {"url":"https://www.icrc.org/en/career-types/internship-or-fellowship","name":"ICRC Fellowship","fetch":True},
    # Asia Pacific
    {"url":"https://www.mext.go.jp/en/policy/education/highered/title02/detail02/1373897.htm","name":"MEXT Japan","fetch":True},
    {"url":"https://www.niied.go.kr/eng/contents.do?contentsNo=105","name":"KGSP Korea","fetch":True},
    {"url":"https://www.csc.edu.cn/studyinchina/","name":"CSC China","fetch":True},
    {"url":"https://www.adb.org/work-with-us/careers/japan-scholarship-program","name":"ADB Japan","fetch":True},
    {"url":"https://www.icdf.org.tw/ct.asp?xItem=12505&CtNode=30316&mp=2","name":"Taiwan ICDF","fetch":True},
    {"url":"https://www.iccr.gov.in/scholarships","name":"ICCR India","fetch":True},
    # Indonesia-relevant
    {"url":"https://www.australiaawardsindonesia.org/","name":"Australia Awards","fetch":True},
    {"url":"https://www.chevening.org/scholarships/","name":"Chevening UK","fetch":True},
    {"url":"https://foreign.fulbrightonline.org/","name":"Fulbright US","fetch":True},
    # Africa / LatAm
    {"url":"https://www.mastercardfdn.org/all/scholars-program/","name":"Mastercard Foundation","fetch":True},
    {"url":"https://www.twas.org/opportunity","name":"TWAS","fetch":True},
    {"url":"https://www.oas.org/en/scholarships/","name":"OAS","fetch":True},
    # Target universities (dari Prinsipal)
    {"url":"https://www.fhs.se/en/","name":"Swedish Defence University","fetch":True},
    {"url":"https://www.uu.se/en/admissions/scholarships","name":"Uppsala University","fetch":True},
    {"url":"https://www.unimi.it/en/education/scholarships-and-exemptions","name":"University of Milan","fetch":True},
    {"url":"https://www.unipi.it/index.php/english-version","name":"University of Pisa","fetch":True},
    {"url":"https://www.universiteitleiden.nl/en/scholarships","name":"Leiden University","fetch":True},
    {"url":"https://www.uu.nl/en/education/scholarships","name":"Utrecht University","fetch":True},
    {"url":"https://www.uva.nl/en/education/fees-and-funding/funding-and-scholarships/funding-and-scholarships.html","name":"University of Amsterdam","fetch":True},
    {"url":"https://vu.nl/en/education/more-about/scholarships","name":"VU Amsterdam","fetch":True},
    {"url":"https://www.wur.nl/en/education-programmes/phd-programme/phd-scholarships.htm","name":"Wageningen University","fetch":True},
    {"url":"https://www.tudelft.nl/en/education/practical-matters/scholarships","name":"TU Delft","fetch":True},
    {"url":"https://www.eur.nl/en/education/practical-matters/scholarships","name":"Erasmus University Rotterdam","fetch":True},
    {"url":"https://www.rug.nl/scholarships","name":"University of Groningen","fetch":True},
    {"url":"https://scholarships.uq.edu.au/","name":"University of Queensland","fetch":True},
    {"url":"https://www.sydney.edu.au/study/fees-and-costs/scholarships.html","name":"University of Sydney","fetch":True},
    {"url":"https://scholarships.unimelb.edu.au/","name":"University of Melbourne","fetch":True},
    {"url":"https://www.anu.edu.au/study/scholarships","name":"ANU","fetch":True},
    {"url":"https://www.monash.edu/study/fees-scholarships/scholarships","name":"Monash University","fetch":True},
    {"url":"https://www.unsw.edu.au/study/scholarships","name":"UNSW","fetch":True},
    {"url":"https://www.otago.ac.nz/scholarships","name":"University of Otago","fetch":True},
    {"url":"https://www.wgtn.ac.nz/scholarships","name":"Victoria University of Wellington","fetch":True},
    {"url":"https://www.auckland.ac.nz/en/study/scholarships-and-awards.html","name":"University of Auckland","fetch":True},
    {"url":"https://www.canterbury.ac.nz/study/scholarships/","name":"University of Canterbury","fetch":True},
    {"url":"https://www.manchester.ac.uk/study/postgraduate-research/funding/","name":"University of Manchester","fetch":True},
    {"url":"https://www.kcl.ac.uk/study/funding","name":"King's College London","fetch":True},
    {"url":"https://www.lse.ac.uk/study-at-lse/Graduate/funding-and-scholarships","name":"LSE","fetch":True},
]


def call_deepseek(messages, max_tokens=2000):
    try:
        r = requests.post(DEEPSEEK_URL, headers={
            "Authorization": f"Bearer {DEEPSEEK_KEY}",
            "Content-Type": "application/json"
        }, json={
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": max_tokens
        }, timeout=90)
        return r.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"  DeepSeek error: {e}")
        return None


def parse_json_result(text):
    if not text:
        return []
    try:
        cleaned = re.sub(r'```json|```', '', text).strip()
        result = json.loads(cleaned)
        return result if isinstance(result, list) else []
    except:
        return []


def fetch_page(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        for tag in soup(['script','style','nav','footer','header']):
            tag.decompose()
        text = soup.get_text(separator=' ', strip=True)
        return ' '.join(text.split())[:8000]
    except:
        return None


def extract_from_content(content, source_name):
    prompt = f"""Extract PhD scholarships from this page content. Source: {source_name}.

Focus ONLY on scholarships relevant to:
{', '.join(FIELDS)}

Content:
{content[:5000]}

Return JSON array. Each item:
{{
  "title": "scholarship name",
  "university": "host university",
  "country": "host country ISO name",
  "field_tags": ["tag1","tag2"],
  "funding_type": "fully_funded|partial|unknown",
  "deadline": "YYYY-MM-DD or null",
  "official_link": "direct URL or null",
  "language_of_instruction": "English",
  "source_language": "en",
  "summary": "2-3 sentences what this scholarship offers"
}}

PhD level only. Return [] if none found. JSON only."""
    result = call_deepseek([
        {"role":"system","content":"Scholarship data extractor. Return only valid JSON arrays."},
        {"role":"user","content":prompt}
    ])
    return parse_json_result(result)


def extract_from_knowledge(source_name):
    prompt = f"""List 3-5 real PhD scholarships or fellowships offered by or listed on: {source_name}.

Focus on fields: {', '.join(FIELDS[:6])}

Return JSON array:
{{
  "title": "exact scholarship name",
  "university": "host university",
  "country": "host country",
  "field_tags": ["tag1","tag2"],
  "funding_type": "fully_funded|partial|unknown",
  "deadline": null,
  "official_link": "most likely URL",
  "language_of_instruction": "English",
  "source_language": "en",
  "summary": "2-3 sentences"
}}

Only include scholarships you are confident exist. Return [] if unsure. JSON only."""
    result = call_deepseek([
        {"role":"system","content":"Scholarship data assistant. Return only valid JSON arrays."},
        {"role":"user","content":prompt}
    ])
    return parse_json_result(result)


def find_key_figures(university, field_tags):
    if not university or university.lower() in ['various','multiple','n/a','unknown']:
        return []
    prompt = f"""Find 2-3 influential researchers at {university} working on: {', '.join(field_tags[:3])}.

Return JSON array:
[{{
  "name": "Full Name",
  "title": "Academic title",
  "research_focus": "1-2 sentences",
  "profile_url": "Google Scholar or faculty page URL",
  "source": "google_scholar|faculty_page"
}}]

Only include researchers with verifiable public profiles. Return [] if unsure. JSON only."""
    result = call_deepseek([
        {"role":"system","content":"Research mapping assistant. Return only valid JSON arrays."},
        {"role":"user","content":prompt}
    ])
    figures = parse_json_result(result)
    return figures[:3]


def make_id(title, university):
    raw = f"{title.lower().strip()}{university.lower().strip()}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def compute_status(deadline_str):
    if not deadline_str:
        return "Unknown"
    try:
        d = datetime.strptime(deadline_str, "%Y-%m-%d")
        now = datetime.now()
        if d < now:
            return "Expired"
        if (d - now).days <= 30:
            return "Closing Soon"
        return "Open"
    except:
        return "Unknown"


def load_existing_ids():
    ids = set()
    try:
        with open('data/scholarships.json') as f:
            for item in json.load(f):
                ids.add(item.get('id'))
    except:
        pass
    return ids


def main():
    existing_ids = load_existing_ids()
    new_items = []

    for source in SOURCES:
        print(f"Processing: {source['name']}...")
        items = []

        if source.get('fetch'):
            content = fetch_page(source['url'])
            if content and len(content) > 200:
                items = extract_from_content(content, source['name'])
                print(f"  Fetched + extracted: {len(items)}")
            else:
                items = extract_from_knowledge(source['name'])
                print(f"  Knowledge fallback: {len(items)}")
        else:
            items = extract_from_knowledge(source['name'])
            print(f"  Knowledge only: {len(items)}")

        for item in items:
            title = (item.get('title') or '').strip()
            university = (item.get('university') or '').strip()
            if not title:
                continue

            item_id = make_id(title, university)
            if item_id in existing_ids:
                continue

            status = compute_status(item.get('deadline'))
            if status == 'Expired':
                continue

            print(f"  New: {title[:60]}")
            time.sleep(2)
            key_figures = find_key_figures(university, item.get('field_tags', []))

            full_item = {
                "id": item_id,
                "title": title,
                "university": university,
                "country": item.get('country','Unknown'),
                "field_tags": item.get('field_tags',[]),
                "funding_type": item.get('funding_type','unknown'),
                "deadline": item.get('deadline'),
                "status": status,
                "official_link": item.get('official_link'),
                "language_of_instruction": item.get('language_of_instruction','English'),
                "source_language": item.get('source_language','en'),
                "summary": item.get('summary',''),
                "key_figures": key_figures,
                "supervisor_page_url": f"https://scholar.google.com/search?q={requests.utils.quote(university)}+phd+supervisor+{requests.utils.quote(' '.join(item.get('field_tags',[])[:2]))}",
                "review_status": "approved",
                "date_sourced": datetime.now().strftime("%Y-%m-%d"),
                "source_name": source['name'],
                "sponsored": False
            }
            new_items.append(full_item)
            existing_ids.add(item_id)

        time.sleep(3)

    if new_items:
        try:
            with open('data/scholarships.json') as f:
                scholarships = json.load(f)
        except:
            scholarships = []
        scholarships.extend(new_items)
        with open('data/scholarships.json','w') as f:
            json.dump(scholarships, f, indent=2, ensure_ascii=False)
        print(f"\nTotal new: {len(new_items)} (langsung tayang, tanpa approval)")
    else:
        print("No new scholarships found")


if __name__ == "__main__":
    main()
