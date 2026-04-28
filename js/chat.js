/**
 * chat.js -- Fashion Expert System Frontend Logic
 * Handles chatbot UI interactions, API calls, and rendering
 */

// ─────────────────────────────────────────────────────────────────────────────
// STATE
// ─────────────────────────────────────────────────────────────────────────────
const state = {
  started: false,
  waiting: false,
  currentOptions: [],
  currentStep: 0,   // track which question we are on
};

// ─────────────────────────────────────────────────────────────────────────────
// DOM REFERENCES
// ─────────────────────────────────────────────────────────────────────────────
const chatWindow    = document.getElementById('chat-window');
const welcomeScreen = document.getElementById('welcome-screen');
const mainChat      = document.getElementById('main-chat');
const inputField    = document.getElementById('user-input');
const sendBtn       = document.getElementById('send-btn');
const optionsWrap   = document.getElementById('options-wrap');
const hintText      = document.getElementById('hint-text');
const progressWrap  = document.getElementById('progress-wrap');
const progressFill  = document.getElementById('progress-fill');
const progressLabel = document.getElementById('progress-label');
const btnReset      = document.getElementById('btn-reset');
const btnStart      = document.getElementById('btn-start');

// ─────────────────────────────────────────────────────────────────────────────
// UTILITIES
// ─────────────────────────────────────────────────────────────────────────────

function scrollBottom() {
  chatWindow.scrollTo({ top: chatWindow.scrollHeight, behavior: 'smooth' });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function clearOptions() {
  optionsWrap.innerHTML = '';
  hintText.textContent = '';
}

function setInputDisabled(disabled) {
  inputField.disabled = disabled;
  sendBtn.disabled = disabled;
}

function cap(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(String(str)));
  return div.innerHTML;
}

// ─────────────────────────────────────────────────────────────────────────────
// TYPING INDICATOR
// ─────────────────────────────────────────────────────────────────────────────

function showTyping() {
  const row = document.createElement('div');
  row.id = 'typing-indicator';
  row.className = 'typing-indicator';
  row.innerHTML =
    '<div class="msg-avatar" aria-label="AI Stylist">&#x2728;</div>' +
    '<div class="typing-dots" aria-label="Typing">' +
    '<span></span><span></span><span></span>' +
    '</div>';
  chatWindow.appendChild(row);
  scrollBottom();
}

function hideTyping() {
  const el = document.getElementById('typing-indicator');
  if (el) el.remove();
}

// ─────────────────────────────────────────────────────────────────────────────
// MESSAGE RENDERING
// ─────────────────────────────────────────────────────────────────────────────

function appendBotMessage(html, type) {
  type = type || '';
  const row = document.createElement('div');
  row.className = 'msg-row bot ' + type;

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.setAttribute('aria-label', 'AI Stylist');
  avatar.textContent = '\u2728';

  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';
  bubble.innerHTML = html;

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatWindow.appendChild(row);
  scrollBottom();
}

function appendUserMessage(text) {
  const row = document.createElement('div');
  row.className = 'msg-row user';

  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';
  bubble.textContent = text;

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.setAttribute('aria-label', 'User');
  avatar.textContent = '\u{1F64B}';

  row.appendChild(bubble);
  row.appendChild(avatar);
  chatWindow.appendChild(row);
  scrollBottom();
}

// ─────────────────────────────────────────────────────────────────────────────
// PROGRESS BAR
// ─────────────────────────────────────────────────────────────────────────────

function updateProgress(step, total) {
  var pct = total > 0 ? Math.round((step / total) * 100) : 0;
  progressFill.style.width = pct + '%';
  progressLabel.textContent = 'Step ' + step + ' of ' + total;
  progressWrap.classList.remove('hidden');
}

// ─────────────────────────────────────────────────────────────────────────────
// QUICK REPLY BUTTONS
// ─────────────────────────────────────────────────────────────────────────────

function renderOptions(options, hint) {
  clearOptions();
  if (!options || options.length === 0) return;

  state.currentOptions = options;
  hintText.textContent = hint || 'Choose an option';

  options.forEach(function(opt) {
    var btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.textContent = opt;
    btn.setAttribute('aria-label', 'Select ' + opt);
    btn.addEventListener('click', function() { handleOptionClick(opt, btn); });
    optionsWrap.appendChild(btn);
  });
}

// ─────────────────────────────────────────────────────────────────────────────
// GENDER THEME SWITCHER  (defined early so handleOptionClick can call it)
// ─────────────────────────────────────────────────────────────────────────────

function applyGenderTheme(gender) {
  document.body.classList.remove('theme-male', 'theme-female');
  if (gender === 'male') {
    document.body.classList.add('theme-male');
  } else {
    document.body.classList.add('theme-female');
  }
}

function handleOptionClick(value, btn) {
  if (state.waiting) return;
  document.querySelectorAll('.option-btn').forEach(function(b) { b.classList.remove('selected'); });
  btn.classList.add('selected');

  // Apply gender theme immediately when user answers the FIRST question (gender)
  if (state.currentStep === 0) {
    applyGenderTheme(value.toLowerCase());
  }

  setTimeout(function() { sendMessage(value); }, 200);
}

// ─────────────────────────────────────────────────────────────────────────────
// RECOMMENDATION -- rendered as staggered chat bubbles
// ─────────────────────────────────────────────────────────────────────────────

function renderRecommendation(data) {
  try {
    clearOptions();
    progressWrap.classList.add('hidden');
    setInputDisabled(true);

    var facts  = data.facts  || {};
    var accs   = Array.isArray(data.accessories)  ? data.accessories  : [];
    var rules  = Array.isArray(data.fired_rules)  ? data.fired_rules  : [];
    var outfit = data.outfit  || 'Smart casual outfit';
    var ruleId = data.rule_id || '--';
    var explanation = data.explanation || 'This recommendation is based on your answers.';

    // Icons for each profile key
    var profileIcons = { gender:'&#128100;', occasion:'&#127917;', weather:'&#127782;', style:'&#10024;', color:'&#127912;' };

    // ── Bubble 1: Profile Summary ──────────────────────────────────────────
    var profileRows = '';
    Object.keys(facts).forEach(function(k) {
      var icon = profileIcons[k] || '';
      profileRows +=
        '<div class="rec-row">' +
          '<span class="rec-key">' + icon + ' ' + cap(k) + '</span>' +
          '<span class="rec-val">' + cap(facts[k]) + '</span>' +
        '</div>';
    });

    appendBotMessage(
      '<div class="rec-section">' +
        '<div class="rec-section-title">&#128203; Your Style Profile</div>' +
        profileRows +
      '</div>'
    );

    // ── Bubble 2: Outfit ───────────────────────────────────────────────────
    setTimeout(function() {
      appendBotMessage(
        '<div class="rec-section rec-outfit-section">' +
          '<div class="rec-section-title">&#128247; Recommended Outfit</div>' +
          '<div class="rec-outfit-big">' + escapeHtml(outfit) + '</div>' +
        '</div>'
      );
    }, 500);

    // ── Bubble 3: Accessories ──────────────────────────────────────────────
    setTimeout(function() {
      var accBadges = accs.map(function(a) {
        return '<span class="acc-badge">' + escapeHtml(a) + '</span>';
      }).join('');

      appendBotMessage(
        '<div class="rec-section">' +
          '<div class="rec-section-title">&#128141; Accessories &amp; Extras</div>' +
          '<div class="acc-list">' + (accBadges || '<em>None listed</em>') + '</div>' +
        '</div>'
      );
    }, 1100);

    // ── Bubble 4: Why this outfit (Explanation) ────────────────────────────
    setTimeout(function() {
      var rulesHtml = rules.map(function(r) {
        return '<span class="rule-chip">' + escapeHtml(r) + '</span>';
      }).join(' ');

      appendBotMessage(
        '<div class="rec-section rec-explain-section">' +
          '<div class="rec-section-title">&#129504; Why This Outfit?</div>' +
          '<div class="rec-explain-body">' + escapeHtml(explanation) + '</div>' +
        '</div>'
      );
    }, 1800);

    // ── Bubble 5: Restart button ───────────────────────────────────────────
    setTimeout(function() {
      var row = document.createElement('div');
      row.className = 'msg-row bot';

      var avatar = document.createElement('div');
      avatar.className = 'msg-avatar';
      avatar.textContent = '\u2728';

      var bubble = document.createElement('div');
      bubble.className = 'msg-bubble';

      var msgText = document.createElement('div');
      msgText.style.marginBottom = '12px';
      msgText.textContent = 'Hope you love your new look! Want to explore another style?';

      var restartBtn = document.createElement('button');
      restartBtn.className = 'btn-try-again';
      restartBtn.id = 'btn-try-again';
      restartBtn.textContent = 'Try Another Outfit';
      restartBtn.addEventListener('click', restartConversation);

      bubble.appendChild(msgText);
      bubble.appendChild(restartBtn);
      row.appendChild(avatar);
      row.appendChild(bubble);
      chatWindow.appendChild(row);
      scrollBottom();
    }, 2600);

  } catch (err) {
    console.error('Recommendation render error:', err);
    appendBotMessage('Something went wrong: ' + err.message, 'error');
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// API CALLS
// ─────────────────────────────────────────────────────────────────────────────

async function startConversation() {
  try {
    var res  = await fetch('/start', { method: 'POST' });
    var data = await res.json();
    handleServerResponse(data);
  } catch (err) {
    appendBotMessage('Could not connect to the server. Please refresh.', 'error');
  }
}

async function sendMessage(text) {
  if (state.waiting || !text.trim()) return;

  state.waiting = true;
  clearOptions();
  setInputDisabled(true);

  appendUserMessage(text);
  inputField.value = '';

  await sleep(350);
  showTyping();
  await sleep(800 + Math.random() * 400);

  try {
    var res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    });
    var data = await res.json();
    hideTyping();
    handleServerResponse(data);
  } catch (err) {
    hideTyping();
    appendBotMessage('Network error. Please try again.', 'error');
  } finally {
    state.waiting = false;
    if (!inputField.disabled) inputField.focus();
  }
}


function handleServerResponse(data) {
  switch (data.type) {

    case 'question':
      state.currentStep = data.step;   // track current step
      appendBotMessage(data.message);
      renderOptions(data.options, data.hint);
      updateProgress(data.step, data.total);
      setInputDisabled(false);
      break;

    case 'error':
      appendBotMessage(data.message, 'error');
      renderOptions(data.options, '');
      setInputDisabled(false);
      break;

    case 'recommendation':
      // Apply theme from facts if available
      if (data.facts && data.facts.gender) {
        applyGenderTheme(data.facts.gender);
      }
      appendBotMessage('Great, I have everything I need! Let me put together your perfect outfit...');
      updateProgress(5, 5);
      setTimeout(function() { renderRecommendation(data); }, 600);
      break;

    case 'done':
      appendBotMessage(data.message);
      break;

    default:
      break;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// START / RESTART
// ─────────────────────────────────────────────────────────────────────────────

async function showChatUI() {
  welcomeScreen.classList.add('hidden');
  mainChat.style.display = 'flex';
  mainChat.classList.remove('hidden');
  state.started = true;
  await startConversation();
}

async function restartConversation() {
  chatWindow.innerHTML = '';
  clearOptions();
  progressWrap.classList.add('hidden');
  setInputDisabled(false);
  state.waiting = false;
  state.currentStep = 0;
  document.body.classList.remove('theme-male', 'theme-female');
  try { await fetch('/reset', { method: 'POST' }); } catch(e) {}
  await startConversation();
}

// ─────────────────────────────────────────────────────────────────────────────
// EVENT LISTENERS
// ─────────────────────────────────────────────────────────────────────────────

btnStart.addEventListener('click', showChatUI);

btnReset.addEventListener('click', async function() {
  if (!state.started) return;
  await restartConversation();
});

sendBtn.addEventListener('click', function() {
  sendMessage(inputField.value.trim());
});

inputField.addEventListener('keydown', function(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage(inputField.value.trim());
  }
});

// ─────────────────────────────────────────────────────────────────────────────
// INIT
// ─────────────────────────────────────────────────────────────────────────────
setInputDisabled(true);
