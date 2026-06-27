import {
  DECK,
  enrichCard,
  findDeckById,
  findDeckByName,
  matchCardId,
} from './deck.js';

const state = {
  query: '',
  loading: false,
  showDeck: false,
  drawn: null,
};

const els = {};

function $(id) {
  return document.getElementById(id);
}

function initEls() {
  els.queryInput = $('query-input');
  els.revealModal = $('reveal-modal');
  els.deckModal = $('deck-modal');
  els.loadingPanel = $('loading-panel');
  els.cardPanel = $('card-panel');
  els.cardRoman = $('card-roman');
  els.cardImg = $('card-img');
  els.cardArchetype = $('card-archetype');
  els.sourceBadge = $('source-badge');
  els.queryEcho = $('query-echo');
  els.cardReading = $('card-reading');
  els.cardTactical = $('card-tactical');
  els.cardCultural = $('card-cultural');
  els.cardEmotional = $('card-emotional');
  els.deckGrid = $('deck-grid');
}

function mapArcanaResponse(data, echo) {
  const base = findDeckById(data.card.card_id) || findDeckByName(data.card.card_name) || findDeckById(matchCardId(echo));
  return {
    card: enrichCard({
      ...base,
      name: data.card.card_name || base.name,
      reading: data.explanation.metaphor,
      tactical: data.explanation.tactical_explanation,
      cultural: data.explanation.cultural_context,
      emotional: data.explanation.emotional_impact,
    }),
    source: 'ai',
    echo,
  };
}

async function runArcana(query) {
  const res = await fetch('/arcana', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ moment_description: query }),
  });
  const data = await res.json();
  if (data.error) throw new Error(data.message || 'Arcana pipeline failed');
  return mapArcanaResponse(data, query);
}

function curatedReading(query, echo) {
  const base = findDeckById(matchCardId(query));
  return { card: enrichCard({ ...base }), source: 'curated', echo };
}

async function consult(rawQuery) {
  if (state.loading) return;

  let query = (rawQuery == null ? state.query : rawQuery).trim();
  let echo = query;
  if (!query) {
    const rnd = DECK[Math.floor(Math.random() * DECK.length)];
    query = rnd.moment;
    echo = rnd.moment;
  }

  state.loading = true;
  state.drawn = { card: {}, source: 'ai', echo };
  render();

  try {
    state.drawn = await runArcana(query);
  } catch (err) {
    console.warn('Granite consult failed, using curated deck:', err.message);
    state.drawn = curatedReading(query, echo);
  } finally {
    state.loading = false;
    render();
  }
}

function closeReveal() {
  state.drawn = null;
  state.loading = false;
  render();
}

function openDeck() {
  state.showDeck = true;
  renderDeck();
  render();
}

function closeDeck() {
  state.showDeck = false;
  render();
}

function pickDeckCard(card) {
  state.showDeck = false;
  state.drawn = { card: enrichCard({ ...card }), source: 'curated', echo: card.moment };
  render();
}

function renderCardPanel() {
  const { drawn, loading } = state;
  const showReveal = !!drawn || loading;

  els.revealModal.classList.toggle('open', showReveal);
  els.loadingPanel.classList.toggle('hidden', !loading);
  els.cardPanel.classList.toggle('hidden', loading || !drawn?.card?.id);

  if (!drawn || loading || !drawn.card?.id) return;

  const c = drawn.card;
  els.cardRoman.textContent = c.roman;
  els.cardImg.src = c.img;
  els.cardImg.alt = c.name;
  els.cardArchetype.textContent = c.archetype;
  els.sourceBadge.textContent = drawn.source === 'ai' ? '✦ DRAWN BY GRANITE' : '◆ FROM THE DECK';
  els.queryEcho.textContent = `THE OMEN — ${drawn.echo}`;
  els.cardReading.textContent = `"${c.reading}"`;
  els.cardTactical.textContent = c.tactical;
  els.cardCultural.textContent = c.cultural;
  els.cardEmotional.textContent = c.emotional;
}

function renderDeck() {
  els.deckGrid.innerHTML = DECK.map((d, i) => `
    <button class="deck-item" data-id="${d.id}" style="animation-delay:${(i * 0.045).toFixed(3)}s">
      <div style="position:relative;width:100%;border-radius:7px;overflow:hidden;border:1px solid #2C2718;box-shadow:0 14px 30px -18px rgba(0,0,0,0.9);">
        <img src="/static/cards/${d.id}.png" alt="${d.name}" style="width:100%;display:block;">
        <div style="position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,transparent 62%,rgba(8,7,5,0.5));"></div>
        <div style="position:absolute;top:8px;left:8px;font-family:'Cinzel',serif;font-size:11px;letter-spacing:0.1em;color:#E0B24A;background:rgba(8,7,5,0.6);border:1px solid rgba(224,178,74,0.35);border-radius:3px;padding:2px 7px;">${d.roman}</div>
      </div>
      <div style="font-family:'Cinzel',serif;font-weight:600;font-size:14px;letter-spacing:0.05em;color:#EFE6CD;margin-top:13px;text-transform:uppercase;">${d.name}</div>
      <div style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:0.07em;color:#857C68;margin-top:5px;text-align:center;line-height:1.5;">${d.archetype}</div>
    </button>
  `).join('');

  els.deckGrid.querySelectorAll('.deck-item').forEach((btn) => {
    btn.addEventListener('click', () => {
      const card = findDeckById(btn.dataset.id);
      if (card) pickDeckCard(card);
    });
  });
}

function render() {
  els.queryInput.value = state.query;
  els.deckModal.classList.toggle('open', state.showDeck);
  renderCardPanel();
}

function setupRevealObserver() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        en.target.classList.add('visible');
        observer.unobserve(en.target);
      }
    });
  }, { threshold: 0.16 });
  document.querySelectorAll('[data-reveal]').forEach((el) => observer.observe(el));
}

function bindEvents() {
  els.queryInput.addEventListener('input', (e) => {
    state.query = e.target.value;
  });
  els.queryInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') consult(state.query);
  });

  $('draw-btn').addEventListener('click', () => consult(state.query));
  $('nav-deck-btn').addEventListener('click', () => consult(''));
  $('view-deck-btn').addEventListener('click', openDeck);
  $('cta-deck-btn').addEventListener('click', () => consult(''));
  $('close-reveal-btn').addEventListener('click', closeReveal);
  $('draw-another-btn').addEventListener('click', () => consult(''));
  $('close-deck-btn').addEventListener('click', closeDeck);

  els.revealModal.addEventListener('click', closeReveal);
  els.deckModal.addEventListener('click', closeDeck);
  els.revealModal.querySelector('.modal').addEventListener('click', (e) => e.stopPropagation());
  els.deckModal.querySelector('.deck-inner').addEventListener('click', (e) => e.stopPropagation());
}

initEls();
renderDeck();
bindEvents();
setupRevealObserver();
render();
