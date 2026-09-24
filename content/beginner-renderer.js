function renderInlineCode(value = '') {
  return escapeHtml(String(value)).replace(/`([^`]+)`/g, '<code>$1</code>');
}

function beginnerChapterTerms(chapter, guide) {
  const seen = new Set();
  const result = [];
  const coreTerms = Array.isArray(guide.coreTerms) ? new Set(guide.coreTerms) : null;
  (chapter.scenes || []).forEach((scene, sceneIndex) => {
    (scene.glossary || []).forEach((item) => {
      if (coreTerms && !coreTerms.has(item.term)) return;
      if (seen.has(item.term)) return;
      seen.add(item.term);
      result.push({ ...item, scene, sceneIndex });
    });
  });
  (guide.terms || []).forEach((item) => {
    if (coreTerms && !coreTerms.has(item.term)) return;
    if (seen.has(item.term)) return;
    seen.add(item.term);
    result.push({ ...item, scene: chapter.scenes?.[0] || {}, sceneIndex: 0 });
  });
  return result;
}

function beginnerTermContext(term, chapter, scene, guide, fallbackGloss, explicitPurpose = '') {
  const needle = String(term).toLowerCase().split(/\s*\/\s*/)[0];
  let matchedScene = scene;
  let stepIndex = -1;
  let step = null;
  for (const candidate of chapter.scenes || []) {
    const candidateIndex = (candidate.steps || []).findIndex((item) => {
      const haystack = `${item.term || ''} ${item.say || ''} ${item.mechanism || ''}`.toLowerCase();
      return haystack.includes(needle);
    });
    if (candidateIndex >= 0) {
      matchedScene = candidate;
      stepIndex = candidateIndex;
      step = candidate.steps[candidateIndex];
      break;
    }
  }
  const base = `${chapter.label} → ${matchedScene.title}`;
  return {
    location: stepIndex >= 0 ? `${base} → bước ${String(stepIndex + 1).padStart(2, '0')}` : base,
    purpose: explicitPurpose || step?.mechanism || `Trong flow “${guide.flow}”, khái niệm này gọi đúng tên một vai trò cần theo dõi. ${fallbackGloss}`
  };
}

function renderBeginnerDictionary(chapter, guide) {
  const terms = beginnerChapterTerms(chapter, guide);
  if (!terms.length) return '';
  const cards = terms.map((item) => {
    const example = termExamples[item.term] || item.scene.command || guide.flow;
    const context = beginnerTermContext(item.term, chapter, item.scene, guide, item.gloss, item.purpose || '');
    return `<article class="term-card"><h4>${escapeHtml(item.term)}</h4><dl><div><dt>Là gì?</dt><dd>${escapeHtml(item.gloss)}</dd></div><div><dt>Tác dụng</dt><dd>${escapeHtml(context.purpose)}</dd></div><div><dt>Ví dụ thật</dt><dd>${escapeHtml(example)}</dd></div><div><dt>Vì sao học?</dt><dd>Để nhận ra chặng “${escapeHtml(context.location)}” đang làm đúng hay là nơi gây lỗi; nếu bỏ qua, bạn dễ sửa nhầm chỗ khi trả lời: ${renderInlineCode(guide.question)}</dd></div><div><dt>Nằm ở đâu?</dt><dd class="term-location">${escapeHtml(context.location)}</dd></div></dl></article>`;
  }).join('');
  return `<details class="concept-dictionary"><summary><div><span>Từ điển tại chỗ</span><strong>${terms.length} thuật ngữ xuất hiện trong chương này</strong><small>Chỉ giữ các từ khóa cần để kể lại cơ chế. Mỗi từ có nghĩa đơn giản, ví dụ và vị trí trong flow.</small></div></summary><div class="term-grid">${cards}</div></details>`;
}

function renderBeginnerSteps(scene) {
  if (!scene.steps?.length) return '';
  return `<div class="mechanism-steps">${scene.steps.map((step, index) => `<article class="mechanism-step"><span>BƯỚC ${String(index + 1).padStart(2, '0')}</span><div><h5>${escapeHtml(step.say || '')}</h5><p>${escapeHtml(step.mechanism || '')}</p>${step.term ? `<code>${escapeHtml(step.term)}</code>` : ''}</div></article>`).join('')}</div>`;
}

function renderBeginnerMechanism(chapter) {
  return (chapter.scenes || []).map((scene, index) => `<article class="mechanism-scene"><p class="studio-kicker">${index === 0 ? 'Đường chính' : `Góc phóng to · ${String(index + 1).padStart(2, '0')}`}</p><h4>${escapeHtml(scene.title || '')}</h4><p class="scene-lead">${escapeHtml(scene.lead || '')}</p><div class="mechanism-copy">${renderReadableText(scene.reading || scene.conclusion || '')}</div>${renderBeginnerSteps(scene)}${scene.conclusion ? `<div class="system-route"><span>Kết luận của cơ chế</span><code>${escapeHtml(scene.conclusion)}</code></div>` : ''}</article>`).join('');
}

function renderGuidedArchifyChapter(topicCode, chapterId, guide) {
  const visuals = archifyVisuals[topicCode]?.[chapterId] || [];
  return visuals.map((visual) => {
    const src = `archify/rendered/${visual.file}.html`;
    return `<figure class="archify-lab"><div class="archify-lab-head"><div><p class="archify-lab-kicker">${escapeHtml(visual.id)} · Visual lab · Archify</p><h3>${escapeHtml(visual.title)}</h3><p class="archify-lab-summary">${escapeHtml(visual.summary)}</p></div><a class="archify-open" href="${src}" target="_blank" rel="noopener">Mở toàn màn hình ↗</a></div><div class="archify-frame-wrap"><iframe class="archify-frame" src="${src}" title="${escapeHtml(visual.title)}" loading="lazy"></iframe></div><div class="archify-understanding"><b>Sau visual · tự kể lại đúng sơ đồ này</b><p><strong>${escapeHtml(visual.title)}:</strong> đi theo tuyến “${escapeHtml(visual.summary)}”. ${renderInlineCode(guide.sayBack)}</p></div><figcaption class="archify-lab-foot"><span class="visual-ratio"><i aria-hidden="true"></i><b>Sơ đồ mang quan hệ · bài viết giải nghĩa và nối thực tế</b></span><span>Phóng to/thu nhỏ, các góc nhìn dẫn đường, giao diện sáng tối và xuất file nằm trong sơ đồ.</span></figcaption></figure>`;
  }).join('');
}

const beginnerPathTargets = {
  F01: ['watch', 'watch', 'place', 'compose', 'automate'],
  F02: ['project', 'boot', 'state', 'state', 'time'],
  F03: ['system', 'model', 'process', 'query', 'transactions', 'storage', 'planner', 'operations']
};

function renderBeginnerHero(topic, lesson, guide) {
  const targets = beginnerPathTargets[topic.code] || lesson.chapters.map((chapter) => chapter.id);
  const path = guide.hero.path.map((item, index) => `<a href="#note-${escapeHtml(targets[index] || lesson.chapters[index]?.id || 'recap')}"><span>${String(index + 1).padStart(2, '0')}</span><b>${escapeHtml(item.label)}</b><small>${escapeHtml(item.plain)}</small></a>`).join('');
  const recap = lesson.chapters.find((chapter) => chapter.id === 'recap');
  const recapLink = recap ? `<a href="#note-recap"><span>${String(guide.hero.path.length + 1).padStart(2, '0')}</span><b>Tổng hợp</b><small>Nối mọi phần thành một mental model.</small></a>` : '';
  return `<section class="beginner-hero"><div class="beginner-hero-main"><p class="studio-kicker">${escapeHtml(guide.hero.kicker)}</p><h2>${renderInlineCode(guide.hero.title)}</h2><p class="beginner-hero-dek">${renderInlineCode(guide.hero.dek)}</p></div><aside class="beginner-scenario"><p class="scenario-label">I · Cơn đau nguyên bản</p><h3>Chuyện gì hỏng nếu vẫn làm thủ công?</h3><p>${renderInlineCode(guide.hero.scenario)}</p><p class="scenario-analogy"><b>Hình dung ban đầu.</b> ${renderInlineCode(guide.hero.analogy)}</p></aside><section class="living-metaphor"><header><div><p class="studio-kicker">II · Bản đồ quy đổi ẩn dụ</p><h3>Một thế giới hữu hình để nhìn thấy cỗ máy vô hình</h3></div><p><b>Thế giới dùng xuyên bài:</b> ${escapeHtml(guide.hero.metaphorWorld)}</p></header><div class="metaphor-table" role="table" aria-label="Bảng quy đổi vật thể đời thường sang khái niệm kỹ thuật"><div class="metaphor-row metaphor-head" role="row"><span>Hình dung trước</span><span>Tên kỹ thuật sau</span><span>Vai trò thật</span></div>${guide.hero.metaphorMap.map((item) => `<div class="metaphor-row" role="row"><strong>${escapeHtml(item.physical)}</strong><b>${escapeHtml(item.technical)}</b><p>${escapeHtml(item.role)}</p></div>`).join('')}</div></section><section class="beginner-outcomes"><p class="scenario-label">Sau khi có hình dung, bạn phải tự giải thích được</p><ul>${guide.hero.outcomes.map((item) => `<li>${renderInlineCode(item)}</li>`).join('')}</ul></section><nav class="beginner-path" aria-label="Mạch học từ tổng thể tới chi tiết">${path}${recapLink}</nav></section>`;
}

function renderBeginnerSection(topicCode, chapter, guide, index) {
  const scene = chapter.scenes[0] || {};
  const visualCount = archifyVisuals[topicCode]?.[chapter.id]?.length || 0;
  const simpleLead = String(guide.plain || scene.lead || '').split(/(?<=[.!?])\s+/)[0];
  return `<section class="beginner-section" id="note-${escapeHtml(chapter.id)}"><header class="beginner-section-head"><div class="beginner-section-index">${String(index + 1).padStart(2, '0')}</div><div class="beginner-section-title"><p class="studio-kicker">III · Cơ chế & thử lửa</p><h2>${escapeHtml(guide.heading || scene.title || chapter.label)}</h2><p>${renderInlineCode(guide.headingLead || simpleLead)}</p></div><aside class="beginner-question"><span>Câu hỏi dẫn đường</span><p>${renderInlineCode(guide.question)}</p></aside></header><div class="beginner-primer"><article class="primer-card"><span class="primer-label">01 · Hình dung trước</span><h3>Giống điều gì mắt thấy được?</h3><p>${renderInlineCode(guide.analogy)}</p><p><b>Giới hạn:</b> ${renderInlineCode(guide.analogyLimit)}</p></article><article class="primer-card"><span class="primer-label">02 · Tên kỹ thuật sau</span><h3>Nói nôm na: nó là gì?</h3><p>${renderInlineCode(guide.plain)}</p></article><article class="primer-card"><span class="primer-label">03 · Tại sao phải biết?</span><h3>Biết để sửa đúng lớp</h3><p>${renderInlineCode(guide.why)}</p></article><article class="primer-card"><span class="primer-label">04 · Nằm ở đâu?</span><h3>Vị trí trong bức tranh lớn</h3><p>${renderInlineCode(guide.place)}</p></article><article class="primer-card"><span class="primer-label">05 · Dùng ở đâu?</span><h3>Trong công việc thực tế</h3><p>${renderInlineCode(guide.job)}</p></article></div><div class="system-route"><span>Đường đi cần giữ trong đầu</span><code>${escapeHtml(guide.flow)}</code></div>${visualCount ? `<section class="visual-brief"><div><span>Sơ đồ này trả lời gì?</span><p>${renderInlineCode(guide.question)}</p><p>${visualCount} sơ đồ bên dưới bóc các góc nhìn khác nhau của cùng câu hỏi.</p></div><div><span>Cách đọc visual</span><p>${renderInlineCode(guide.visualLook)}</p></div></section>${renderGuidedArchifyChapter(topicCode, chapter.id, guide)}` : ''}<div class="mechanism-grid"><div class="mechanism-main"><header><span>Đi từ trực giác tới cơ chế</span><h3>Cơ chế thật sự diễn ra thế nào?</h3><p>Đọc sau visual: mỗi bước phải có chủ thể, việc nó làm và kết quả chuyển sang bước sau.</p></header>${renderBeginnerMechanism(chapter)}</div><aside class="mechanism-side"><article class="mechanism-side-card"><span>Một câu phải giữ</span><p>${escapeHtml(scene.conclusion || guide.plain)}</p></article><article class="mechanism-side-card"><span>Tự kiểm</span><p>${renderInlineCode(guide.sayBack)}</p></article><article class="mechanism-side-card"><span>Nối sang phần sau</span><p>${renderInlineCode(guide.bridge)}</p></article></aside></div><section class="stress-test"><header><p class="studio-kicker">Kịch bản thử lửa</p><h3>Nếu cỗ máy bị ép tới giới hạn thì sao?</h3></header><div><article><span>Sự cố nhìn thấy được</span><p>${renderInlineCode(guide.stress)}</p></article><article><span>Cách hệ thống chống đỡ + dấu vết kiểm tra</span><p>${renderInlineCode(guide.response)}</p></article></div></section>${renderBeginnerDictionary(chapter, guide)}<div class="chapter-bridge"><span>Mạch kiến thức</span><p>${renderInlineCode(guide.bridge)}</p></div></section>`;
}

function renderBeginnerSynthesis(topicCode, guide) {
  const final = guide.final;
  return `<section class="lesson-synthesis"><header class="lesson-synthesis-head"><div><p class="studio-kicker">IV · Bản chất 1 dòng · rồi mới tổng hợp</p><h2>Tóm lại, bạn đã học được gì — và các phần nối nhau ra sao?</h2></div><p class="lesson-synthesis-intro">Bắt đầu từ root của bài, đi theo đường flow, rồi dùng từng thuật ngữ như tên gọi cho một cơ chế đã hiểu — không học thuộc từ trước khi hiểu việc.</p></header><blockquote class="golden-takeaway"><span>Golden takeaway · một câu trẻ 10 tuổi cũng kể lại được</span><strong>${renderInlineCode(final.golden)}</strong></blockquote><ol class="synthesis-learned">${final.learned.map((item) => `<li>${renderInlineCode(item)}</li>`).join('')}</ol><section class="market-grid" aria-label="Ứng dụng trong công việc">${final.market.map((item) => `<article class="market-card"><span>${escapeHtml(item.label)}</span><p>${renderInlineCode(item.text)}</p></article>`).join('')}</section><div class="practice-check"><article class="practice-card"><p class="studio-kicker">Mini-lab để biến đọc thành hiểu</p><h3>Tự làm một vòng hoàn chỉnh</h3><p>${renderInlineCode(final.practice)}</p></article><article class="check-card"><p class="studio-kicker">Không nhìn bài, tự trả lời</p><h3>5 câu kiểm tra mental model</h3><ol>${final.checks.map((item) => `<li>${renderInlineCode(item)}</li>`).join('')}</ol></article></div></section>`;
}

function renderPlainStudyNote(topic) {
  const lesson = lessons[topic.code];
  const guide = beginnerGuides[topic.code];
  if (!lesson || !guide) return renderLegacyPlainStudyNote(topic);
  const sections = lesson.chapters.map((chapter, index) => renderBeginnerSection(topic.code, chapter, guide.chapters[chapter.id], index)).join('');
  const topicIndex = topics.findIndex((item) => item.code === topic.code) + 1;
  const ladders = {
    F01: 'ý định → người hiểu lệnh → chương trình đang chạy → tài nguyên → tự động hóa',
    F02: 'thư mục code → lần chạy → dữ liệu và lỗi → chờ/tính → yêu cầu web',
    F03: 'sự thật chung → luật dữ liệu → đọc/ghi đồng thời → lưu bền → vận hành'
  };
  const ladder = guide.hero.ladder || ladders[topic.code] || '';
  $('#content').innerHTML = `<header class="lesson-head"><div><div class="crumb"><strong>Syllabus</strong><i></i><span>${escapeHtml(topic.group)}</span><i></i><span>${topic.code}</span></div><h1>${escapeHtml(topic.title)}</h1><p>${escapeHtml(guide.hero.dek)}</p><div class="lesson-ladder"><span>Toàn cảnh → chi tiết</span><b>${escapeHtml(ladder)}</b></div></div><div class="head-state"><div class="state-row"><span>Trạng thái</span><b class="state-live">Dành cho người mới</b></div><div class="state-row"><span>Chủ đề</span><b>${String(topicIndex).padStart(2, '0')} / ${topics.length}</b></div><div class="state-row"><span>Cách học</span><b>Việc thật → cơ chế → thuật ngữ</b></div></div></header><article class="beginner-note">${renderBeginnerHero(topic, lesson, guide)}${sections}${renderBeginnerSynthesis(topic.code, guide)}</article>`;
  document.body.classList.remove('is-studio');
}
