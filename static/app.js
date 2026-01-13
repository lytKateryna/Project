console.log('JS LOADED');
let currentPage = 0;
const limit = 10;

let currentSearchType = null;
let currentSearchParams = {};
// Tab switching
function showTab(tabName) {
  // Hide all tabs
  document.querySelectorAll('.tab-content').forEach((tab) => tab.classList.remove('active'));
  document.querySelectorAll('.tab-button').forEach((btn) => btn.classList.remove('active'));

  // Show selected tab
  document.getElementById(tabName + '-tab').classList.add('active');
  event.target.classList.add('active');

  // Load statistics if switching to statistics tab
  if (tabName === 'statistics') {
    loadStatistics();
  }
}

// Statistics functions
async function loadStatistics() {
  const statsType = document.getElementById('statsType').value;
  const resultsDiv = document.getElementById('statsResults');

  resultsDiv.innerHTML = '<p>Loading...</p>';

  try {
    const endpoint = statsType === 'popular' ? '/meta/popular' : '/meta/recent';
    const response = await fetch(endpoint);
    if (!response.ok) throw new Error('Server error: ' + response.status);
    const data = await response.json();
    const items = data?.items || [];

    const html = `
            <ul>
                ${items.map((query) => `<li>${query}</li>`).join('')}
            </ul>
        `;
    resultsDiv.innerHTML = html || '<p>No data available</p>';
  } catch (e) {
    resultsDiv.innerHTML = '<p>Error loading statistics</p>';
    console.error('loadStatistics error:', e);
  }
}

function search() {
  const query = document.getElementById('searchInput')?.value?.trim();
  if (!query) {
    document.getElementById('results').innerHTML = '<p>Please enter a keyword or year</p>';
    return;
  }

  // Check if query is a 4-digit year
  const yearRegex = /^\d{4}$/;
  if (yearRegex.test(query)) {
    searchByYear(query);
  } else {
    searchByKeyword();
  }
}

async function searchByKeyword(keyword = null, resetPage = true) {
  if (resetPage) resetPagination();
  if (!keyword) keyword = document.getElementById('searchInput')?.value?.trim();
  const resultsDiv = document.getElementById('results');
  const safePage = Number.isFinite(currentPage) ? currentPage : 0;
  const safeLimit = Number.isFinite(limit) ? limit : 10;
  const offset = safePage * safeLimit;
  if (!resultsDiv) return;

  if (!keyword) {
    resultsDiv.innerHTML = '<p>Please enter a keyword</p>';
    return;
  }

  currentSearchType = 'keyword';
  currentSearchParams = { keyword };

  resultsDiv.innerHTML = '<p>Loading...</p>';

  try {
    const response = await fetch(
      `/films/search/keyword?query=${encodeURIComponent(keyword)}&offset=${offset}&limit=${safeLimit}`,
    );
    if (!response.ok) throw new Error('Server error: ' + response.status);
    const data = await response.json();
    const items = data?.items || [];
    const total = data?.total || 0;

    const html = items
      .map((item) => {
        const poster = item.poster_url || item.poster || '/static/no-poster.png';
        const year = item.release_year || item.year || '';
        const title = item.title || 'Untitled';
        return `
                <div class="card">
                    <img src="${poster}" alt="${title}">
                    <h3>${title}</h3>
                    <span>${year}</span>
                </div>
            `;
      })
      .join('');

    resultsDiv.innerHTML = html || '<p>No results found</p>';
    updatePaginationDisplay(total);
  } catch (e) {
    resultsDiv.innerHTML = '<p>Error loading data</p>';
    console.error('searchByKeyword error:', e);
  }
}

function searchByYear(year, resetPage = true) {
  if (resetPage) resetPagination();
  if (!year) return;

  const y = parseInt(String(year).trim(), 10);
  if (Number.isNaN(y)) {
    document.getElementById('results').innerHTML = '<p>Invalid year</p>';
    return;
  }

  currentSearchType = 'year';
  currentSearchParams = { year: y };

  const resultsDiv = document.getElementById('results');
  if (!resultsDiv) return;

  resultsDiv.innerHTML = '<p>Loading...</p>';

  const offset = currentPage * limit;
  fetch(`/films/search/year?year=${y}&offset=${offset}&limit=${limit}`)
    .then((res) => {
      if (!res.ok) throw new Error('Server error: ' + res.status);
      return res.json();
    })
    .then((data) => {
      const items = data?.items || [];
      const total = data?.total || 0;

      const html = items
        .map((item) => {
          const poster = item.poster_url || item.poster || '/static/no-poster.png';
          const year = item.release_year || item.year || '';
          const title = item.title || 'Untitled';
          return `
                    <div class="card">
                        <img src="${poster}" alt="${title}">
                        <h3>${title}</h3>
                        <span>${year}</span>
                    </div>
                `;
        })
        .join('');

      resultsDiv.innerHTML = html || '<p>No results found</p>';
      updatePaginationDisplay(total);
    })
    .catch((e) => {
      console.error('searchByYear error:', e);
      resultsDiv.innerHTML = '<p>Error searching by year</p>';
    });
}

function searchByYearRange(resetPage = true) {
  if (resetPage) resetPagination();
  const yearFrom = document.getElementById('yearFrom')?.value?.trim();
  const yearTo = document.getElementById('yearTo')?.value?.trim();
  const genreId = document.getElementById('yearRangeGenre')?.value?.trim();

  if (!yearFrom || !yearTo) {
    document.getElementById('results').innerHTML = '<p>Please enter both from and to years</p>';
    return;
  }

  const from = parseInt(yearFrom);
  const to = parseInt(yearTo);

  if (from > to) {
    document.getElementById('results').innerHTML =
      '<p>From year cannot be greater than to year</p>';
    return;
  }

  currentSearchType = 'year_range';
  currentSearchParams = { year_from: from, year_to: to, category_id: genreId || null };

  const resultsDiv = document.getElementById('results');
  if (!resultsDiv) return;

  resultsDiv.innerHTML = '<p>Loading...</p>';

  const offset = currentPage * limit;
  let url = `/films/search/year_range?year_from=${encodeURIComponent(
    from,
  )}&year_to=${encodeURIComponent(to)}&offset=${offset}&limit=${limit}`;
  if (genreId) {
    url += `&category_id=${encodeURIComponent(genreId)}`;
  }

  fetch(url)
    .then((res) => {
      if (!res.ok) throw new Error('Server error: ' + res.status);
      return res.json();
    })
    .then((data) => {
      const items = data?.items || [];
      const total = data?.total || 0;

      const html = items
        .map((item) => {
          const poster = item.poster_url || item.poster || '/static/no-poster.png';
          const year = item.release_year || item.year || '';
          const title = item.title || 'Untitled';
          return `
                    <div class="card">
                        <img src="${poster}" alt="${title}">
                        <h3>${title}</h3>
                        <span>${year}</span>
                    </div>
                `;
        })
        .join('');

      resultsDiv.innerHTML = html || '<p>No results found</p>';
      updatePaginationDisplay(total);
    })
    .catch((e) => {
      console.error('searchByYearRange error:', e);
      resultsDiv.innerHTML = '<p>Error searching by year range</p>';
    });
}

function renderResults(films) {
  const results = document.getElementById('results');
  results.innerHTML = '';

  if (films.length === 0) {
    results.innerHTML = '<p>No films found</p>';
    return;
  }

  films.forEach((film) => {
    const div = document.createElement('div');
    div.className = 'film-card';

    div.innerHTML = `
            <img src="${film.poster_url}" alt="">
            <h3>${film.title}</h3>
            <p>${film.release_year}</p>
            <p>⭐ ${film.rating}</p>
        `;

    results.appendChild(div);
  });
}

async function loadGenres() {
  console.log('loadGenres called');

  const container = document.getElementById('genres');
  const yearRangeSelect = document.getElementById('yearRangeGenre');
  if (!container) {
    console.error('NO #genres ELEMENT');
    return;
  }

  try {
    const response = await fetch('/films/genres');
    const data = await response.json();

    container.innerHTML = '';
    (data?.items || []).forEach((genre) => {
      const btn = document.createElement('button');
      btn.textContent = genre.name;
      btn.onclick = () => searchByGenre(genre.category_id);
      container.appendChild(btn);

      // Also populate the year range genre select
      if (yearRangeSelect) {
        const option = document.createElement('option');
        option.value = genre.category_id;
        option.textContent = genre.name;
        yearRangeSelect.appendChild(option);
      }
    });
  } catch (e) {
    console.error('loadGenres error:', e);
    container.innerHTML = '<p>Could not load genres</p>';
  }
}
const genreCache = new Map();

async function searchByGenre(categoryId) {
  console.log('searchByGenre:', categoryId);

  const resultsDiv = document.getElementById('results');
  if (!resultsDiv) return;
  if (genreCache.has(categoryId)) {
    resultsDiv.innerHTML = genreCache.get(categoryId);
    return;
  }
  resultsDiv.innerHTML = '<p>Loading...</p>';

  try {
    const response = await fetch(
      `/films/search/genres?category_id=${categoryId}&year_from=1900&year_to=2100`,
    );
    if (!response.ok) throw new Error('Server error: ' + response.status);
    const data = await response.json();
    const items = data?.items || [];

    const html = items
      .map((item) => {
        const poster = item.poster_url || item.poster || '/static/no-poster.png';
        const year = item.release_year || item.year || '';
        const title = item.title || 'Untitled';
        return `
                <div class="card">
                <img 
  src="${poster}" 
  alt="${title}" 
  loading="lazy"
  decoding="async"
>

<!--                    <img src="${poster}" alt="${title}">-->
                    <h3>${title}</h3>
                    <span>${year}</span>
                </div>
            `;
      })
      .join('');
    genreCache.set(categoryId, html);
    resultsDiv.innerHTML = html || '<p>No results found</p>';
  } catch (e) {
    resultsDiv.innerHTML = '<p>Error loading data</p>';
    console.error('searchByGenre error:', e);
  }
}

loadGenres(); // initialize genre buttons

// Pagination functions
function resetPagination() {
  currentPage = 0;
  currentSearchType = null;
  currentSearchParams = {};
  document.getElementById('pagination').style.display = 'none';
}

function updatePaginationDisplay(total) {
  const paginationDiv = document.getElementById('pagination');
  const pageInfo = document.getElementById('pageInfo');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');

  if (total <= limit) {
    paginationDiv.style.display = 'none';
    return;
  }

  paginationDiv.style.display = 'flex';
  pageInfo.textContent = `Page ${currentPage + 1}`;

  prevBtn.disabled = currentPage === 0;
  nextBtn.disabled = (currentPage + 1) * limit >= total;
}

function prevPage() {
  if (currentPage > 0) {
    currentPage--;
    if (currentSearchType === 'keyword') {
      searchByKeyword(currentSearchParams.keyword, false);
    } else if (currentSearchType === 'year') {
      searchByYear(currentSearchParams.year, false);
    } else if (currentSearchType === 'year_range') {
      searchByYearRange(false);
    }
  }
}

function nextPage() {
  currentPage++;
  if (currentSearchType === 'keyword') {
    searchByKeyword(currentSearchParams.keyword, false);
  } else if (currentSearchType === 'year') {
    searchByYear(currentSearchParams.year, false);
  } else if (currentSearchType === 'year_range') {
    searchByYearRange(false);
  }
}

// Attach Enter key handler and ensure search button triggers search
(() => {
  const input = document.getElementById('searchInput');
  if (input) {
    input.addEventListener('keyup', (e) => {
      if (e.key === 'Enter') search();
    });

    // try to find the button sibling in the same .search-box
    const parent = input.parentElement;
    if (parent) {
      const btn = parent.querySelector('button');
      if (btn) btn.addEventListener('click', search);
    }
  }
})();
