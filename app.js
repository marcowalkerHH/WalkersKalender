const USERS = {
  noah: {
    name: 'Noah',
    accent: 'var(--noah-accent)',
    themeClass: 'theme-noah',
  },
  johanna: {
    name: 'Johanna',
    accent: 'var(--johanna-accent)',
    themeClass: 'theme-johanna',
  },
  sibylle: {
    name: 'Sibylle',
    accent: 'var(--sibylle-accent)',
    themeClass: 'theme-sibylle',
  }
};

const questionFiles = {
  noah: 'questions/noah_questions.json',
  johanna: 'questions/johanna_questions.json',
  sibylle: 'questions/sibylle_questions.json'
};

const DOOR_ICONS = {
  default: ['❄️', '🎄', '⭐', '🎁', '🕯️', '🎅', '🧝‍♀️', '☃️', '🔔', '🍪'],
  noah: ['🎮', '🛸', '🧬', '⚡', '🛰️', '🕹️', '🧠', '💾', '🎬', '🪐'],
  johanna: ['👗', '💄', '💍', '👜', '👠', '💅', '💐', '✨', '🌸', '🎀'],
  sibylle: ['❤️', '🩺', '💊', '🧬', '🥼', '🌿', '🍎', '🧠', '🫀', '💡'],
};

const PRAISE_MESSAGES = {
  default: [
    'Glückwunsch, das war absolut richtig! +1 Punkt 🎉',
    'Fantastisch beantwortet – weiter so! +1 Punkt ✨',
    'Dein Wissen glänzt heller als jede Lichterkette! +1 Punkt 🌟',
  ],
  noah: [
    'Noah, du bist ein Matrix-Mastermind! +1 Punkt ⚡',
    'Gaming-Instinkt on point – stark gemacht! +1 Punkt 🎮',
    'Mission erfüllt, Captain Noah! +1 Punkt 🚀',
  ],
  johanna: [
    'Johanna, du bist der Inbegriff von Haute-Couture-Wissen! +1 Punkt 👗',
    'Fashion-Queen! Perfekte Antwort. +1 Punkt 👑',
    'Eleganter Volltreffer, Johanna! +1 Punkt ✨',
  ],
  sibylle: [
    'Diagnose top, Doc Sibylle! +1 Punkt 🩺',
    'Herzwissen deluxe – bravo! +1 Punkt ❤️',
    'Sibylle, du behandelst jede Frage meisterhaft! +1 Punkt 🌿',
  ],
};

const LOCAL_KEYS = {
  scores: 'wc_scores',
  mode: 'wc_mode',
  categoryUsage: 'wc_category_usage',
  usedQuestions: 'wc_used_questions',
  music: 'wc_music',
};

const ADMIN_CODE = '687468';

const state = {
  selectedUser: null,
  scores: { noah: 0, johanna: 0, sibylle: 0 },
  mode: 'open',
  questions: {},
  usedQuestions: {},
  categoryUsage: {},
  musicIndex: 0,
  musicEnabled: true,
  musicVolume: 0.35,
};

let calendar;
let calendarTitle;
let calendarSubtitle;
let modeSwitch;
let modeLabel;
let questionModal;
let questionTitle;
let questionText;
let questionCategory;
let answersContainer;
let questionFeedback;
let loginSection;
let calendarView;
let loginMessage;
let securityQuestionLabel;
let securityAnswer;
let loginConfirmButton;
let app;
let intro;
let heartStage;
let matrixCanvas;
let closeQuestion;
let refreshQuestions;
let backToLogin;
let scoreboard;
let levelOverlay;
let crownOverlay;
let adminModal;
let adminOpen;
let adminClose;
let adminCheck;
let adminPanel;
let adminCodeInput;
let adminMessage;
let resetScoresButton;
let toggleModeButton;
let musicToggle;
let volumeControl;
let nextTrackButton;

const audioPlaylist = Array.isArray(window.WALKERS_AUDIO_TRACKS)
  ? window.WALKERS_AUDIO_TRACKS
  : [];

let audioPlayer = new Audio();
audioPlayer.loop = false;
audioPlayer.addEventListener('ended', () => {
  nextTrack();
});
audioPlayer.addEventListener('error', () => {
  if (!audioPlaylist.length) return;
  console.warn('Audiotrack konnte nicht geladen werden, nächster Track.');
  nextTrack();
});

let hasInitialized = false;
let introFailsafeTimer = null;
let loginChallengeAnswer = null;

function cacheDom() {
  calendar = document.getElementById('calendar');
  calendarTitle = document.getElementById('calendarTitle');
  calendarSubtitle = document.getElementById('calendarSubtitle');
  modeSwitch = document.getElementById('modeSwitch');
  modeLabel = document.getElementById('modeLabel');
  questionModal = document.getElementById('questionModal');
  questionTitle = document.getElementById('questionTitle');
  questionText = document.getElementById('questionText');
  questionCategory = document.getElementById('questionCategory');
  answersContainer = document.getElementById('answers');
  questionFeedback = document.getElementById('questionFeedback');
  loginSection = document.getElementById('login');
  calendarView = document.getElementById('calendarView');
  loginMessage = document.getElementById('loginMessage');
  securityQuestionLabel = document.getElementById('securityQuestionLabel');
  securityAnswer = document.getElementById('securityAnswer');
  loginConfirmButton = document.getElementById('loginConfirm');
  app = document.getElementById('app');
  intro = document.getElementById('intro');
  heartStage = document.getElementById('heartStage');
  matrixCanvas = document.getElementById('matrixCanvas');
  closeQuestion = document.getElementById('closeQuestion');
  refreshQuestions = document.getElementById('refreshQuestions');
  backToLogin = document.getElementById('backToLogin');
  scoreboard = document.getElementById('scoreboard');
  levelOverlay = document.getElementById('levelOverlay');
  crownOverlay = document.getElementById('crownOverlay');
  adminModal = document.getElementById('adminModal');
  adminOpen = document.getElementById('adminOpen');
  adminClose = document.getElementById('adminClose');
  adminCheck = document.getElementById('adminCheck');
  adminPanel = document.getElementById('adminPanel');
  adminCodeInput = document.getElementById('adminCode');
  adminMessage = document.getElementById('adminMessage');
  resetScoresButton = document.getElementById('resetScores');
  toggleModeButton = document.getElementById('toggleMode');
  musicToggle = document.getElementById('musicToggle');
  volumeControl = document.getElementById('volumeControl');
  nextTrackButton = document.getElementById('nextTrack');
}

function ensureDomReferences() {
  const required = {
    calendar,
    calendarTitle,
    calendarSubtitle,
    modeSwitch,
    modeLabel,
    questionModal,
    questionTitle,
    questionText,
    questionCategory,
    answersContainer,
    questionFeedback,
    loginSection,
    calendarView,
    loginMessage,
    securityQuestionLabel,
    securityAnswer,
    loginConfirmButton,
    app,
    intro,
    heartStage,
    matrixCanvas,
    closeQuestion,
    refreshQuestions,
    backToLogin,
    scoreboard,
    levelOverlay,
    crownOverlay,
    adminModal,
    adminOpen,
    adminClose,
    adminCheck,
    adminPanel,
    adminCodeInput,
    adminMessage,
    resetScoresButton,
    toggleModeButton,
    musicToggle,
    volumeControl,
    nextTrackButton,
  };

  const missing = Object.entries(required)
    .filter(([, el]) => !el)
    .map(([name]) => name);

  if (missing.length) {
    throw new Error(`Fehlende DOM-Elemente: ${missing.join(', ')}`);
  }
}

function handleFatalError(error) {
  console.error('Initialisierung fehlgeschlagen', error);
  revealAppImmediately();
  showFatalMessage('Ups! Bitte lade die Seite neu oder leere den Browser-Cache.');
}

function revealAppImmediately() {
  if (intro) {
    intro.classList.add('hidden');
  }
  if (app) {
    app.classList.remove('hidden');
  }
}

function showFatalMessage(text) {
  if (loginMessage) {
    loginMessage.textContent = text;
    loginMessage.classList.add('error');
    return;
  }
  const fallback = document.createElement('p');
  fallback.className = 'message error';
  fallback.textContent = text;
  (app || document.body).prepend(fallback);
}

function safeReadJSON(key, fallback) {
  const raw = localStorage.getItem(key);
  if (!raw) return fallback;
  try {
    const parsed = JSON.parse(raw);
    if (parsed === null || typeof parsed !== 'object') {
      return fallback;
    }
    return parsed;
  } catch (error) {
    console.warn(`Konnte localStorage-Eintrag ${key} nicht lesen, wird zurückgesetzt.`, error);
    localStorage.removeItem(key);
    return fallback;
  }
}

function init() {
  if (hasInitialized) return;
  hasInitialized = true;
  try {
    cacheDom();
    // Start the intro immediately so it always fades out even if later
    // initialization (like DOM assertions) fails on mismatched files.
    setupIntro();
    ensureDomReferences();
    restoreState();
    setupLogin();
    createCalendar();
    bindEvents();
    loadQuestions();
    initSnow();
    initMusic();
  } catch (error) {
    handleFatalError(error);
  }
}

function setupIntro() {
  if (!intro) {
    revealAppImmediately();
    return;
  }

  if (introFailsafeTimer) {
    clearTimeout(introFailsafeTimer);
  }

  introFailsafeTimer = setTimeout(() => {
    console.warn('Intro-Failsafe aktiv, Anwendung wird direkt angezeigt.');
    revealAppImmediately();
  }, 12000);

  setTimeout(() => {
    if (heartStage) {
      heartStage.classList.add('hidden');
    }
    if (matrixCanvas) {
      matrixCanvas.classList.remove('hidden');
      startMatrixAnimation();
    }
  }, 3500);

  setTimeout(() => {
    intro.classList.add('hidden');
    if (app) {
      app.classList.remove('hidden');
    }
    if (introFailsafeTimer) {
      clearTimeout(introFailsafeTimer);
      introFailsafeTimer = null;
    }
  }, 8500);
}

function startMatrixAnimation() {
  if (!matrixCanvas) return;
  const ctx = matrixCanvas.getContext('2d');
  const w = matrixCanvas.width = window.innerWidth;
  const h = matrixCanvas.height = window.innerHeight;
  const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789★❄︎☃︎';
  const fontSize = 18;
  const columns = Math.floor(w / fontSize);
  const drops = Array(columns).fill(1);

  function draw() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#00ffa0';
    ctx.font = fontSize + 'px monospace';
    drops.forEach((y, idx) => {
      const text = letters.charAt(Math.floor(Math.random() * letters.length));
      ctx.fillText(text, idx * fontSize, y * fontSize);
      if (y * fontSize > h && Math.random() > 0.975) {
        drops[idx] = 0;
      }
      drops[idx] = y + 1;
    });
  }
  const matrixInterval = setInterval(draw, 50);
  setTimeout(() => clearInterval(matrixInterval), 5000);
}

function getRandomInt(min, max) {
  const minCeil = Math.ceil(min);
  const maxFloor = Math.floor(max);
  return Math.floor(Math.random() * (maxFloor - minCeil + 1)) + minCeil;
}

function refreshSecurityQuestion() {
  if (!securityQuestionLabel || !securityAnswer) return;
  const first = getRandomInt(3, 12);
  const second = getRandomInt(2, 11);
  loginChallengeAnswer = first + second;
  securityQuestionLabel.textContent = `Sicherheitsfrage: Wieviel ist ${first} + ${second}?`;
  securityAnswer.value = '';
}

function setupLogin() {
  document.querySelectorAll('.user-select button').forEach((button) => {
    button.addEventListener('click', () => {
      state.selectedUser = button.dataset.user;
      document.querySelectorAll('.user-select button').forEach((btn) => btn.classList.remove('active'));
      button.classList.add('active');
      loginMessage.textContent = '';
    });
  });

  if (loginConfirmButton) {
    loginConfirmButton.addEventListener('click', () => {
      if (!state.selectedUser) {
        loginMessage.textContent = 'Bitte wähle eine Person.';
        return;
      }
      if (loginChallengeAnswer === null) {
        refreshSecurityQuestion();
      }
      if (Number(securityAnswer.value) !== loginChallengeAnswer) {
        loginMessage.textContent = 'Die Antwort ist leider falsch.';
        refreshSecurityQuestion();
        return;
      }
      loginMessage.textContent = '';
      refreshSecurityQuestion();
      showCalendar();
    });
  }

  refreshSecurityQuestion();
}

function showCalendar() {
  loginSection.classList.add('hidden');
  calendarView.classList.remove('hidden');
  updateTheme();
  updateDoors();
}

function updateTheme() {
  const user = USERS[state.selectedUser];
  calendarTitle.textContent = `${user.name} – Christmas Calendar`;
  calendarSubtitle.textContent = state.mode === 'open' ? 'Alle Türchen frei wählbar' : 'Advent-Modus aktiv';
  document.body.dataset.theme = user.themeClass;
  document.querySelectorAll('.calendar button').forEach((door) => {
    door.style.boxShadow = `inset 0 0 0 2px ${user.accent}`;
  });
  updateDoorIcons();
}

function updateDoors() {
  const limit = state.mode === 'advent' ? getCurrentAdventDay() : 24;
  document.querySelectorAll('.calendar button').forEach((door) => {
    const day = Number(door.dataset.day);
    const locked = day > limit;
    door.classList.toggle('locked', locked);
  });
}

function createCalendar() {
  const fragment = document.createDocumentFragment();
  for (let i = 1; i <= 24; i += 1) {
    const button = document.createElement('button');
    button.innerHTML = `<span>${i}</span>`;
    button.dataset.day = i;
    button.dataset.iconIndex = i - 1;
    button.addEventListener('click', () => handleDoorClick(i));
    fragment.appendChild(button);
  }
  calendar.appendChild(fragment);
  updateDoorIcons();
  updateDoors();
}

function updateDoorIcons() {
  const icons = getDoorIcons();
  document.querySelectorAll('.calendar button').forEach((door) => {
    const index = Number(door.dataset.iconIndex) || 0;
    door.dataset.icon = icons[index % icons.length];
  });
}

function getDoorIcons() {
  if (!state.selectedUser) return DOOR_ICONS.default;
  return DOOR_ICONS[state.selectedUser] || DOOR_ICONS.default;
}

function handleDoorClick(day) {
  if (!state.selectedUser) {
    loginMessage.textContent = 'Bitte erst einloggen.';
    return;
  }
  if (state.mode === 'advent') {
    const currentDay = getCurrentAdventDay();
    if (day > currentDay) {
      return;
    }
  }
  openQuestion();
}

function getCurrentAdventDay() {
  const now = new Date();
  if (now.getMonth() === 11) {
    return Math.min(now.getDate(), 24);
  }
  return 24;
}

function loadQuestions() {
  const entries = Object.entries(questionFiles).map(([user, path]) => fetch(path)
    .then((res) => {
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      return res.json();
    })
    .then((data) => {
      state.questions[user] = Array.isArray(data) ? data : [];
    })
    .catch((error) => {
      console.error(`Fehler beim Laden der Fragen für ${user}`, error);
      state.questions[user] = [];
    }));
  return Promise.all(entries);
}

function openQuestion() {
  const question = drawQuestion();
  if (!question) {
    questionText.textContent = 'Keine Fragen verfügbar.';
    questionCategory.textContent = '';
    answersContainer.innerHTML = '';
  } else {
    questionTitle.textContent = `${USERS[state.selectedUser].name} – Quiz`;
    questionText.textContent = question.question;
    questionCategory.textContent = question.category;
    answersContainer.innerHTML = '';
    question.answers.forEach((answer, index) => {
      const button = document.createElement('button');
      button.textContent = answer;
      button.addEventListener('click', () => handleAnswer(button, index === question.correctIndex, question));
      answersContainer.appendChild(button);
    });
  }
  questionFeedback.textContent = '';
  questionFeedback.classList.remove('celebrate', 'oops');
  questionModal.classList.remove('hidden');
}

function drawQuestion() {
  const user = state.selectedUser;
  const userQuestions = state.questions[user];
  if (!userQuestions) return null;

  const usage = state.categoryUsage[user] || {};
  const categories = [...new Set(userQuestions.map((q) => q.category))];
  const minUsage = Math.min(...categories.map((cat) => usage[cat] || 0));
  const leastUsedCategories = categories.filter((cat) => (usage[cat] || 0) === minUsage);
  const category = leastUsedCategories[Math.floor(Math.random() * leastUsedCategories.length)];

  const difficulty = shouldUseHardQuestions(user) ? 'hard' : 'normal';

  const preferredOrder = difficulty === 'hard' ? ['hard', 'normal'] : ['normal', 'hard'];
  let question = null;
  preferredOrder.some((level) => {
    question = pullQuestion(user, category, level);
    return Boolean(question);
  });

  if (question) {
    state.categoryUsage[user] = state.categoryUsage[user] || {};
    state.categoryUsage[user][category] = (state.categoryUsage[user][category] || 0) + 1;
    saveState();
  }

  return question;
}

function pullQuestion(user, category, difficulty) {
  state.usedQuestions[user] = state.usedQuestions[user] || {};
  const usedList = state.usedQuestions[user][difficulty] || [];
  const usedSet = new Set(usedList);
  let pool = state.questions[user].filter((q) => q.category === category && q.difficulty === difficulty && !usedSet.has(q.id));
  if (!pool.length) {
    state.usedQuestions[user][difficulty] = [];
    pool = state.questions[user].filter((q) => q.category === category && q.difficulty === difficulty);
  }
  if (!pool.length) return null;
  const question = pool[Math.floor(Math.random() * pool.length)];
  state.usedQuestions[user][difficulty] = [...(state.usedQuestions[user][difficulty] || []), question.id];
  return question;
}

function handleAnswer(button, isCorrect, question) {
  document.querySelectorAll('#answers button').forEach((btn) => {
    btn.disabled = true;
  });
  questionFeedback.classList.remove('celebrate', 'oops');
  if (isCorrect) {
    button.classList.add('correct');
    questionFeedback.textContent = getPraiseMessage();
    questionFeedback.classList.add('celebrate');
    updateScore(1);
  } else {
    button.classList.add('wrong');
    questionFeedback.textContent = `Leider falsch. Richtige Antwort: ${question.answers[question.correctIndex]}. -1 Punkt`;
    questionFeedback.classList.add('oops');
    updateScore(-1);
  }
}

function getPraiseMessage() {
  const user = state.selectedUser;
  const pool = (user && PRAISE_MESSAGES[user]) || PRAISE_MESSAGES.default;
  const index = Math.floor(Math.random() * pool.length);
  return pool[index];
}

function updateScore(delta) {
  const user = state.selectedUser;
  state.scores[user] = (state.scores[user] || 0) + delta;
  saveState();
  updateScoreboard();
  checkLevelUp(user);
}

function updateScoreboard() {
  Object.entries(state.scores).forEach(([user, score]) => {
    const span = scoreboard.querySelector(`[data-user="${user}"] strong`);
    if (span) span.textContent = score;
  });
}

function checkLevelUp(user) {
  const score = state.scores[user];
  if (score > 0 && score % 10 === 0 && state.mode === 'open') {
    levelOverlay.classList.remove('hidden');
    setTimeout(() => levelOverlay.classList.add('hidden'), 3000);
  }
  if (score >= 50 && score % 50 === 0) {
    crownOverlay.classList.remove('hidden');
    setTimeout(() => crownOverlay.classList.add('hidden'), 4000);
  }
}

function shouldUseHardQuestions(user) {
  return state.scores[user] >= 10 && state.mode === 'open';
}

function bindEvents() {
  closeQuestion.addEventListener('click', () => questionModal.classList.add('hidden'));
  refreshQuestions.addEventListener('click', () => {
    if (!state.selectedUser) return;
    state.usedQuestions[state.selectedUser] = {};
    state.categoryUsage[state.selectedUser] = {};
    saveState();
    alert('Fragen für ' + USERS[state.selectedUser].name + ' wurden neu gemischt.');
  });
  backToLogin.addEventListener('click', () => {
    calendarView.classList.add('hidden');
    loginSection.classList.remove('hidden');
    state.selectedUser = null;
    document.querySelectorAll('.user-select button').forEach((btn) => btn.classList.remove('active'));
    loginMessage.textContent = '';
    refreshSecurityQuestion();
  });
  modeSwitch.addEventListener('change', () => {
    modeSwitch.checked = state.mode === 'advent';
    requestAdminCode(() => {
      state.mode = state.mode === 'open' ? 'advent' : 'open';
      saveState();
      modeSwitch.checked = state.mode === 'advent';
      updateModeLabel();
    });
  });
  adminOpen.addEventListener('click', () => adminModal.classList.remove('hidden'));
  adminClose.addEventListener('click', closeAdminModal);
  adminCheck.addEventListener('click', () => {
    if (adminCodeInput.value === ADMIN_CODE) {
      adminMessage.textContent = 'Zugang gewährt.';
      adminPanel.classList.remove('hidden');
    } else {
      adminMessage.textContent = 'Code falsch.';
    }
  });
  resetScoresButton.addEventListener('click', () => {
    if (!validateAdmin()) return;
    Object.keys(state.scores).forEach((user) => { state.scores[user] = 0; });
    saveState();
    updateScoreboard();
  });
  toggleModeButton.addEventListener('click', () => {
    if (!validateAdmin()) return;
    state.mode = state.mode === 'open' ? 'advent' : 'open';
    saveState();
    modeSwitch.checked = state.mode === 'advent';
    updateModeLabel();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      questionModal.classList.add('hidden');
      adminModal.classList.add('hidden');
    }
  });
  musicToggle.addEventListener('click', toggleMusic);
  volumeControl.addEventListener('input', (event) => {
    state.musicVolume = Number(event.target.value);
    audioPlayer.volume = state.musicVolume;
    saveState();
  });
  nextTrackButton.addEventListener('click', nextTrack);
}

function updateModeLabel() {
  modeLabel.textContent = state.mode === 'open' ? 'Offener Modus' : 'Advent-Modus';
  calendarSubtitle.textContent = state.mode === 'open' ? 'Alle Türchen frei wählbar' : 'Tägliche Türchen bis heute aktiv';
  updateDoors();
}

function requestAdminCode(callback) {
  const code = prompt('Admin-Code eingeben');
  if (code === ADMIN_CODE) {
    callback();
  }
}

function closeAdminModal() {
  adminModal.classList.add('hidden');
  adminPanel.classList.add('hidden');
  adminMessage.textContent = '';
  adminCodeInput.value = '';
}

function validateAdmin() {
  if (adminCodeInput.value !== ADMIN_CODE) {
    adminMessage.textContent = 'Bitte Admin-Code eingeben.';
    return false;
  }
  return true;
}

function initSnow() {
  const snowLayer = document.getElementById('snowLayer');
  if (!snowLayer) return;

  const spawnFlake = () => {
    const flake = document.createElement('div');
    flake.className = 'flake';
    flake.style.left = `${Math.random() * 100}%`;
    const delay = Math.random() * 4;
    const duration = 4 + Math.random() * 6;
    flake.style.animationDelay = `${delay}s`;
    flake.style.animationDuration = `${duration}s`;
    snowLayer.appendChild(flake);
    setTimeout(() => {
      if (flake.parentNode) {
        flake.parentNode.removeChild(flake);
      }
    }, (delay + duration + 1) * 1000);
  };

  for (let i = 0; i < 80; i += 1) {
    spawnFlake();
  }

  setInterval(spawnFlake, 700);
}

function restoreState() {
  state.scores = safeReadJSON(LOCAL_KEYS.scores, state.scores);
  state.mode = localStorage.getItem(LOCAL_KEYS.mode) || 'open';
  state.categoryUsage = safeReadJSON(LOCAL_KEYS.categoryUsage, {});
  state.usedQuestions = safeReadJSON(LOCAL_KEYS.usedQuestions, {});
  const musicSettings = safeReadJSON(LOCAL_KEYS.music, {});
  state.musicEnabled = typeof musicSettings.enabled === 'boolean'
    ? musicSettings.enabled
    : true;
  state.musicVolume = typeof musicSettings.volume === 'number'
    ? musicSettings.volume
    : 0.35;
  state.musicIndex = typeof musicSettings.index === 'number'
    ? musicSettings.index
    : 0;
  if (!audioPlaylist.length) {
    state.musicIndex = 0;
  } else {
    state.musicIndex = state.musicIndex % audioPlaylist.length;
  }
  modeSwitch.checked = state.mode === 'advent';
  updateModeLabel();
  updateScoreboard();
}

function saveState() {
  localStorage.setItem(LOCAL_KEYS.scores, JSON.stringify(state.scores));
  localStorage.setItem(LOCAL_KEYS.mode, state.mode);
  localStorage.setItem(LOCAL_KEYS.categoryUsage, JSON.stringify(state.categoryUsage));
  localStorage.setItem(LOCAL_KEYS.usedQuestions, JSON.stringify(state.usedQuestions));
  localStorage.setItem(LOCAL_KEYS.music, JSON.stringify({
    enabled: state.musicEnabled,
    volume: state.musicVolume,
    index: state.musicIndex,
  }));
}

function initMusic() {
  if (!audioPlaylist.length) {
    musicToggle.disabled = true;
    volumeControl.disabled = true;
    nextTrackButton.disabled = true;
    musicToggle.title = 'Keine Audiodateien eingebunden';
    return;
  }
  volumeControl.value = state.musicVolume;
  audioPlayer.src = audioPlaylist[state.musicIndex];
  audioPlayer.volume = state.musicVolume;
  if (state.musicEnabled) {
    audioPlayer.play().catch(() => {});
  } else {
    musicToggle.textContent = '🔇';
  }
}

function toggleMusic() {
  if (!audioPlaylist.length) return;
  state.musicEnabled = !state.musicEnabled;
  if (state.musicEnabled) {
    musicToggle.textContent = '🎵';
    audioPlayer.play().catch(() => {});
  } else {
    musicToggle.textContent = '🔇';
    audioPlayer.pause();
  }
  saveState();
}

function nextTrack() {
  if (!audioPlaylist.length) return;
  state.musicIndex = (state.musicIndex + 1) % audioPlaylist.length;
  audioPlayer.src = audioPlaylist[state.musicIndex];
  audioPlayer.currentTime = 0;
  if (state.musicEnabled) {
    audioPlayer.play().catch(() => {});
  }
  saveState();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

