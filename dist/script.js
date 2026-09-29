const select = document.querySelector('#case-select');
const view = document.querySelector('#case-view');

function el(tag, className, content) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (content !== undefined) node.textContent = content;
  return node;
}

function renderCase(item) {
  view.replaceChildren();
  const top = el('div', 'case-meta');
  top.append(el('span', '', `${item.case_id} · first turn · ${item.category}`),
             el('span', '', `Decision: ${item.preferred}`));
  view.append(top, el('p', 'case-prompt', item.prompt_summary));

  const pair = el('div', 'response-pair');
  for (const letter of ['A', 'B']) {
    const key = `candidate_${letter.toLowerCase()}`;
    const preferred = item.preferred === letter;
    const card = el('div', `response-card ${preferred ? 'preferred' : ''}`);
    const heading = el('div', 'response-heading');
    heading.append(el('strong', '', `${letter} · ${item[`${key}_model_id`]}`));
    if (preferred) heading.append(el('span', 'preferred-badge', 'PREFERRED'));
    card.append(heading, el('p', '', item[`${key}_summary`]));
    const score = el('div', 'score-line',
      `Correctness ${item[`${letter.toLowerCase()}_correctness`]}/2 · Instructions ${item[`${letter.toLowerCase()}_instruction`]}/2 · Relevance ${item[`${letter.toLowerCase()}_relevance`]}/2 · Clarity ${item[`${letter.toLowerCase()}_clarity`]}/2`);
    const source = el('a', 'source-link', `Read original answer ↗`);
    source.href = item[`${key}_source_url`];
    source.target = '_blank';
    source.rel = 'noopener noreferrer';
    source.title = `Find answer ID ${item[`${key}_answer_id`]} in the source file`;
    card.append(score, el('span', 'answer-id', `Answer ID: ${item[`${key}_answer_id`]}`), source);
    pair.append(card);
  }
  view.append(pair);
  const rationale = el('div', 'rationale');
  rationale.append(el('span', 'mini-label', item.primary_error.replaceAll('_', ' ')),
                   el('p', '', item.rationale));
  const prompt = el('a', 'source-link', 'Read original prompt ↗');
  prompt.href = item.prompt_source_url;
  prompt.target = '_blank';
  prompt.rel = 'noopener noreferrer';
  prompt.title = `Find question ID ${item.question_id} in the source file`;
  rationale.append(prompt, el('span', 'answer-id', `Question ID: ${item.question_id} · Source period: ${item.source_period}`));
  view.append(rationale);
}

fetch('data/real_model_evaluations.json')
  .then(response => { if (!response.ok) throw new Error('Cases unavailable'); return response.json(); })
  .then(items => {
    select.replaceChildren();
    items.forEach(item => {
      const option = document.createElement('option');
      option.value = item.case_id;
      option.textContent = `${item.case_id} · ${item.category}`;
      select.append(option);
    });
    select.addEventListener('change', () => renderCase(items.find(item => item.case_id === select.value)));
    renderCase(items[0]);
  })
  .catch(() => {
    select.replaceChildren(el('option', '', 'Cases unavailable'));
    view.replaceChildren(el('p', '', 'The interactive sample could not load. The CSV and source files are linked below.'));
  });

const annotationList = document.querySelector('#annotation-list');
const annotationCount = document.querySelector('#annotation-count');
const intentCounts = document.querySelector('#intent-counts');
const languageFilter = document.querySelector('#language-filter');
const intentFilter = document.querySelector('#intent-filter');
const intentOrder = ['DELIVERY_ISSUE', 'BILLING_ISSUE', 'REFUND_REQUEST',
                     'ACCOUNT_ACCESS', 'TECHNICAL_SUPPORT', 'OTHER'];

function renderAnnotations(items) {
  const filtered = items.filter(item =>
    (languageFilter.value === 'all' || item.language === languageFilter.value) &&
    (intentFilter.value === 'all' || item.primary_intent === intentFilter.value));
  annotationCount.textContent = `Showing ${filtered.length} of ${items.length} messages`;
  annotationList.replaceChildren();
  if (!filtered.length) {
    annotationList.append(el('p', 'empty-annotations', 'No messages match these filters.'));
    return;
  }
  for (const item of filtered) {
    const row = el('div', 'annotation-row');
    row.setAttribute('role', 'listitem');
    const identity = el('div', 'annotation-identity');
    identity.append(el('strong', '', item.item_id),
                    el('span', '', item.language === 'pt-BR' ? 'Brazilian Portuguese' : 'English'));
    const message = el('p', 'annotation-text', item.text);
    message.lang = item.language;
    const labels = el('div', 'annotation-labels');
    labels.append(el('span', 'tag', item.primary_intent),
                  el('span', `urgency urgency-${item.urgency.toLowerCase()}`, `${item.urgency} urgency`));
    row.append(identity, message, labels);
    annotationList.append(row);
  }
}

fetch('data/intent_annotations.json')
  .then(response => { if (!response.ok) throw new Error('Annotations unavailable'); return response.json(); })
  .then(items => {
    const counts = new Map(intentOrder.map(intent => [intent, 0]));
    items.forEach(item => counts.set(item.primary_intent, (counts.get(item.primary_intent) || 0) + 1));
    for (const intent of intentOrder) {
      const option = document.createElement('option');
      option.value = intent;
      option.textContent = `${intent} (${counts.get(intent)})`;
      intentFilter.append(option);
      const chip = el('div', 'intent-count');
      chip.append(el('strong', '', String(counts.get(intent))), el('span', '', intent));
      intentCounts.append(chip);
    }
    languageFilter.addEventListener('change', () => renderAnnotations(items));
    intentFilter.addEventListener('change', () => renderAnnotations(items));
    renderAnnotations(items);
  })
  .catch(() => {
    annotationCount.textContent = 'Annotations unavailable';
    annotationList.replaceChildren(el('p', 'empty-annotations', 'The interactive list could not load. Download the full CSV below.'));
  });
