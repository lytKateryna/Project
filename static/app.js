console.log('JS LOADED');

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

async function searchByKeyword() {
  const keyword = document.getElementById('searchInput')?.value?.trim();
  const resultsDiv = document.getElementById('results');

  if (!resultsDiv) return;

  if (!keyword) {
    resultsDiv.innerHTML = '<p>Please enter a keyword</p>';
    return;
  }

  resultsDiv.innerHTML = '<p>Loading...</p>';

  try {
    const response = await fetch(`/films/search/keyword?query=${encodeURIComponent(keyword)}`);
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
                    <img src="${poster}" alt="${title}">
                    <h3>${title}</h3>
                    <span>${year}</span>
                </div>
            `;
      })
      .join('');

    resultsDiv.innerHTML = html || '<p>No results found</p>';
  } catch (e) {
    resultsDiv.innerHTML = '<p>Error loading data</p>';
    console.error('searchByKeyword error:', e);
  }
}

function searchByYear(year) {
  if (!year) return;

  const y = parseInt(String(year).trim(), 10);
  if (Number.isNaN(y)) {
    document.getElementById('results').innerHTML = '<p>Invalid year</p>';
    return;
  }

  const resultsDiv = document.getElementById('results');
  if (!resultsDiv) return;

  resultsDiv.innerHTML = '<p>Loading...</p>';

  fetch(`/films/search/year?year=${y}`)
    .then((res) => {
      if (!res.ok) throw new Error('Server error: ' + res.status);
      return res.json();
    })
    .then((data) => {
      const items = data?.items || [];

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
    })
    .catch((e) => {
      console.error('searchByYear error:', e);
      resultsDiv.innerHTML = '<p>Error searching by year</p>';
    });
}

function searchByYearRange() {
  const resultsDiv = document.getElementById('results');
  if (!resultsDiv) return;

  const yearFromInput = document.getElementById('yearFrom');
  const yearToInput = document.getElementById('yearTo');
  const from = yearFromInput?.valueAsNumber;
  const to = yearToInput?.valueAsNumber;

  if (!Number.isInteger(from) || !Number.isInteger(to)) {
    resultsDiv.innerHTML = '<p>Please enter both from and to years</p>';
    return;
  }

  if (from > to) {
    resultsDiv.innerHTML = '<p>From year cannot be greater than to year</p>';
    return;
  }

  resultsDiv.innerHTML = '<p>Loading...</p>';

  fetch(
    `/films/search/year_range?year_from=${encodeURIComponent(from)}&year_to=${encodeURIComponent(to)}`
)
    .then((res) => {
      if (!res.ok) throw new Error('Server error: ' + res.status);
      return res.json();
    })
    .then((data) => {
      const items = data?.items || [];

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

  const yearFromInput = document.getElementById('yearFrom');
  const yearToInput = document.getElementById('yearTo');
  const yearRangeBtn = document.querySelector('.year-range-box button');

  const onYearRangeEnter = (e) => {
    if (e.key === 'Enter') searchByYearRange();
  };

  if (yearFromInput) yearFromInput.addEventListener('keyup', onYearRangeEnter);
  if (yearToInput) yearToInput.addEventListener('keyup', onYearRangeEnter);
  if (yearRangeBtn) yearRangeBtn.addEventListener('click', searchByYearRange);
})();
