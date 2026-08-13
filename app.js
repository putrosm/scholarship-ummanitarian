// State
let allScholarships = [];
let currentLang = 'en';

// ── LANG TOGGLE ──
function toggleLang() {
  currentLang = currentLang === 'en' ? 'id' : 'en';
  applyLang();
  document.getElementById('lang-btn').textContent = currentLang === 'en' ? '🇮🇩 ID' : '🇬🇧 EN';
}

function applyLang() {
  const key = currentLang === 'en' ? 'en' : 'id';
  document.querySelectorAll('[data-en]').forEach(el => {
    const val = el.dataset[key];
    if (val) el.textContent = val;
  });
  document.querySelectorAll('[data-placeholder-en]').forEach(el => {
    el.placeholder = currentLang === 'en' ? el.dataset.placeholderEn : el.dataset.placeholderId;
  });
  // Re-render to update card labels
  if (allScholarships.length) renderCards(filterData());
  updateResultsCount(filterData().length);
}

// ── FETCH DATA ──
async function loadScholarships() {
  try {
    const r = await fetch('/data/scholarships.json');
    allScholarships = await r.json();
    populateFilters();
    updateStats();
    renderCards(allScholarships);
    document.getElementById('loading').style.display = 'none';
    document.getElementById('cards-grid').style.display = 'grid';
    if (allScholarships.length === 0) {
      document.getElementById('empty-state').style.display = 'block';
      document.getElementById('cards-grid').style.display = 'none';
    }
    updateResultsCount(allScholarships.length);
  } catch (e) {
    console.error(e);
    document.getElementById('loading').innerHTML = '<p>Failed to load scholarships.</p>';
  }
}

// ── STATS ──
function updateStats() {
  const open = allScholarships.filter(s => s.status === 'Open' || s.status === 'Closing Soon').length;
  const countries = new Set(allScholarships.map(s => s.country).filter(Boolean)).size;
  document.getElementById('stat-open').textContent = open;
  document.getElementById('stat-countries').textContent = countries;
}

// ── POPULATE FILTERS ──
function populateFilters() {
  // Fields
  const fields = new Set();
  allScholarships.forEach(s => (s.field_tags || []).forEach(t => fields.add(t)));
  const fieldSel = document.getElementById('filter-field');
  [...fields].sort().forEach(f => {
    const o = document.createElement('option');
    o.value = f;
    o.textContent = f.charAt(0).toUpperCase() + f.slice(1);
    fieldSel.appendChild(o);
  });

  // Countries
  const countries = new Set(allScholarships.map(s => s.country).filter(Boolean));
  const countrySel = document.getElementById('filter-country');
  [...countries].sort().forEach(c => {
    const o = document.createElement('option');
    o.value = c;
    o.textContent = c;
    countrySel.appendChild(o);
  });
}

// ── FILTER ──
function filterData() {
  const q = document.getElementById('search-input').value.toLowerCase().trim();
  const status = document.getElementById('filter-status').value;
  const funding = document.getElementById('filter-funding').value;
  const field = document.getElementById('filter-field').value;
  const country = document.getElementById('filter-country').value;
  const sortBy = document.getElementById('sort-by').value;

  let data = allScholarships.filter(s => {
    if (status && s.status !== status) return false;
    if (funding && s.funding_type !== funding) return false;
    if (field && !(s.field_tags || []).includes(field)) return false;
    if (country && s.country !== country) return false;
    if (q) {
      const searchable = [s.title, s.university, s.country, s.summary, ...(s.field_tags || [])].join(' ').toLowerCase();
      if (!searchable.includes(q)) return false;
    }
    return true;
  });

  // Sort
  data.sort((a, b) => {
    if (a.sponsored && !b.sponsored) return -1;
    if (!a.sponsored && b.sponsored) return 1;
    if (sortBy === 'deadline') {
      if (!a.deadline) return 1;
      if (!b.deadline) return -1;
      return new Date(a.deadline) - new Date(b.deadline);
    }
    return new Date(b.date_sourced || 0) - new Date(a.date_sourced || 0);
  });

  return data;
}

function updateResultsCount(n) {
  const el = document.getElementById('results-count');
  el.textContent = currentLang === 'en'
    ? `${n} scholarship${n !== 1 ? 's' : ''} found`
    : `${n} beasiswa ditemukan`;
}

function clearFilters() {
  document.getElementById('search-input').value = '';
  ['filter-status','filter-funding','filter-field','filter-country','sort-by'].forEach(id => {
    document.getElementById(id).selectedIndex = 0;
  });
  applyFilters();
}

function applyFilters() {
  const data = filterData();
  renderCards(data);
  updateResultsCount(data.length);
  const noRes = document.getElementById('no-results');
  const grid = document.getElementById('cards-grid');
  if (data.length === 0 && allScholarships.length > 0) {
    noRes.style.display = 'block';
    grid.style.display = 'none';
  } else {
    noRes.style.display = 'none';
    grid.style.display = 'grid';
  }
}

// ── RENDER CARDS ──
function renderCards(data) {
  const grid = document.getElementById('cards-grid');
  grid.innerHTML = data.map(s => cardHTML(s)).join('');
}

function cardHTML(s) {
  const statusMap = {
    'Open': ['status-open', currentLang === 'en' ? 'Open' : 'Buka'],
    'Closing Soon': ['status-closing', currentLang === 'en' ? 'Closing Soon' : 'Segera Tutup'],
    'Expired': ['status-expired', currentLang === 'en' ? 'Expired' : 'Berakhir'],
    'Unknown': ['status-unknown', currentLang === 'en' ? 'Unknown' : 'Tidak Diketahui']
  };
  const [statusCls, statusLabel] = statusMap[s.status] || statusMap['Unknown'];

  const fundingMap = {
    'fully_funded': currentLang === 'en' ? 'Fully Funded' : 'Beasiswa Penuh',
    'partial': currentLang === 'en' ? 'Partial' : 'Sebagian',
    'unknown': currentLang === 'en' ? 'Check page' : 'Cek halaman'
  };
  const fundingLabel = fundingMap[s.funding_type] || s.funding_type;

  const deadline = s.deadline
    ? new Date(s.deadline).toLocaleDateString('en-GB', {day:'numeric', month:'short', year:'numeric'})
    : (currentLang === 'en' ? 'No deadline' : 'Tanpa tenggat');

  const tagsHTML = (s.field_tags || []).slice(0, 4).map(t =>
    `<span class="tag">${t}</span>`
  ).join('');

  const keyFigsHTML = s.key_figures && s.key_figures.length ? `
    <details class="key-figures">
      <summary>${currentLang === 'en' ? 'Key Researchers' : 'Peneliti Kunci'}</summary>
      <ul>
        ${s.key_figures.map(f => `
          <li>
            <strong>${escHTML(f.name)}</strong> &mdash; ${escHTML(f.title || '')}<br>
            <small>${escHTML(f.research_focus || '')}</small><br>
            ${f.profile_url ? `<a href="${escHTML(f.profile_url)}" target="_blank" rel="noopener">
              ${currentLang === 'en' ? 'View Profile →' : 'Lihat Profil →'}
            </a>` : ''}
          </li>
        `).join('')}
      </ul>
      <p class="ai-disclaimer">${currentLang === 'en'
        ? '⚠ AI-suggested — verify independently before contact.'
        : '⚠ Saran AI — verifikasi secara mandiri sebelum menghubungi.'}</p>
    </details>
  ` : '';

  const supervisorBtn = s.supervisor_page_url ? `
    <a href="${escHTML(s.supervisor_page_url)}" target="_blank" rel="noopener" class="btn-supervisor">
      ${currentLang === 'en' ? 'Find Supervisors' : 'Cari Pembimbing'}
    </a>
  ` : '';

  const applyBtn = s.official_link ? `
    <a href="${escHTML(s.official_link)}" target="_blank" rel="noopener" class="btn-apply">
      ${currentLang === 'en' ? 'View Scholarship →' : 'Lihat Beasiswa →'}
    </a>
  ` : '';

  return `
    <div class="scholarship-card${s.sponsored ? ' sponsored' : ''}">
      ${s.sponsored ? '<span class="badge-featured">FEATURED</span>' : ''}
      <div class="card-header">
        <h3 class="card-title">${escHTML(s.title)}</h3>
        <span class="status-badge ${statusCls}">${statusLabel}</span>
      </div>
      <div class="card-meta">
        <span>🏛 ${escHTML(s.university || '—')}</span>
        <span>🌍 ${escHTML(s.country || '—')}</span>
      </div>
      <div class="card-meta">
        <span>📅 ${deadline}</span>
        <span>💰 ${fundingLabel}</span>
        <span>🗣 ${escHTML(s.language_of_instruction || 'English')}</span>
      </div>
      <div class="card-tags">${tagsHTML}</div>
      <p class="card-summary">${escHTML(s.summary || '')}</p>
      ${keyFigsHTML}
      <div class="card-actions">
        ${applyBtn}
        ${supervisorBtn}
      </div>
    </div>
  `;
}

function escHTML(str) {
  return String(str)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}

// ── EVENT LISTENERS ──
document.addEventListener('DOMContentLoaded', () => {
  loadScholarships();

  let searchTimer;
  document.getElementById('search-input').addEventListener('input', () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(applyFilters, 300);
  });

  ['filter-status','filter-funding','filter-field','filter-country','sort-by'].forEach(id => {
    document.getElementById(id).addEventListener('change', applyFilters);
  });
});
