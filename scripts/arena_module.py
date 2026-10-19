#!/usr/bin/env python3
"""
FSDS · EDAI · DSAI — AI Adaptive Practice & Career Mastery Arena Module
Provides ARENA_CSS (Minimalist Anthropic Editorial UI) and ARENA_JS:
- 3-Tier Ultra-Fast Cognitive Memory DB (In-Memory Hot Digest <0.2ms + IndexedDB + Supabase Sync)
- Anti-Grind Breadth x Depth Matrix & Bilingual AI Warden ("Quản Giáo AI" / "The AI Warden")
- Universal BYOK Multi-Provider AI Gateway (Gemini, OpenAI/Codex, Claude, Grok, DeepSeek, Qwen, GLM, Kimi, OpenRouter, Custom) + Fetch Models
- Polymorphic Question Generator (Zero exact repeat + Global Adaptive Tier Shift across 7 Ranks: Student -> Senior+)
- Level 1 & 2 Instant Grader + Level 3 Hybrid AI First-Principles Semantic Grader
- Contextual In-Arena Study Chatbox (2-Phase Anti-Spoiler Pre-Submit Socratic vs Post-Submit Deep Dive)
- Multi-Account Virtual Sandbox & Automated Dev Test Harness API
"""

ARENA_CSS = r"""
  /* ==========================================================================
     ARENA PRACTICE LAB (#/practice) — AUTHENTIC ANTHROPIC ACADEMY CDS
     ========================================================================== */
  .arena-shell {
    display: flex;
    flex-direction: column;
    gap: 22px;
    max-width: var(--article-max, 1120px);
    margin: 0 auto;
    padding: 0 0 56px;
  }

  /* Login Gate Two-Column Editorial Layout */
  .arena-gate-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 20px;
    align-items: stretch;
  }

  @media (min-width: 860px) {
    .arena-gate-grid {
      grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
    }
  }

  .arena-gate-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 16px;
    padding: 24px 26px;
    border-radius: 16px;
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
  }

  .arena-gate-card h2 {
    margin: 0 0 6px;
    font-family: var(--cds-font-serif);
    font-size: 21px;
    font-weight: 400;
    letter-spacing: -0.015em;
    color: var(--cds-text-primary);
  }

  .arena-gate-card p {
    margin: 0;
    font-size: 14px;
    line-height: 1.56;
    color: var(--cds-text-secondary);
  }

  .arena-form-stack {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .arena-field {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .arena-field-label,
  .arena-control-label {
    font-family: var(--cds-font-sans);
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--cds-text-muted);
  }

  .arena-select,
  .arena-input {
    appearance: none;
    width: 100%;
    height: 36px;
    padding: 0 12px;
    border-radius: 8px;
    border: 1px solid var(--cds-border-default);
    background: var(--cds-surface-0);
    color: var(--cds-text-primary);
    font-family: var(--cds-font-sans);
    font-size: 13.5px;
    outline: none;
    transition: border-color 0.14s ease;
  }

  .arena-select:focus,
  .arena-input:focus {
    border-color: var(--cds-clay);
  }

  /* Buttons aligned with main Hub .ui-btn */
  .arena-btn {
    appearance: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    min-height: 32px;
    padding: 5px 12px;
    border-radius: 8px;
    border: 1px solid var(--cds-border-default);
    background: var(--cds-surface-0);
    color: var(--cds-text-primary);
    font-family: var(--cds-font-sans);
    font-size: 12.5px;
    font-weight: 500;
    line-height: 1.2;
    white-space: nowrap;
    cursor: pointer;
    transition: background 0.14s var(--motion-ease), border-color 0.14s var(--motion-ease), color 0.14s var(--motion-ease), transform 0.1s ease;
    text-decoration: none;
  }

  .arena-btn:hover:not(:disabled) {
    background: var(--cds-fill-ghost-hover);
    border-color: var(--cds-border-strong);
  }

  .arena-btn:active:not(:disabled) {
    transform: translateY(1px);
  }

  .arena-btn-primary {
    background: var(--cds-fill-primary);
    border-color: var(--cds-fill-primary);
    color: var(--cds-text-on-primary);
  }

  .arena-btn-primary:hover:not(:disabled) {
    opacity: 0.92;
    background: var(--cds-fill-primary);
    border-color: var(--cds-fill-primary);
    color: var(--cds-text-on-primary);
  }

  .arena-btn-clay {
    background: var(--cds-clay);
    border-color: var(--cds-clay);
    color: #ffffff;
    font-weight: 500;
  }

  .arena-btn-clay:hover:not(:disabled) {
    opacity: 0.92;
    background: var(--cds-clay);
    border-color: var(--cds-clay);
    color: #ffffff;
  }

  .arena-btn-danger {
    color: #b44c36;
    border-color: color-mix(in oklab, #b44c36 32%, var(--cds-border-default));
    background: color-mix(in oklab, #b44c36 6%, var(--cds-surface-0));
  }

  .arena-btn-danger:hover:not(:disabled) {
    background: color-mix(in oklab, #b44c36 14%, var(--cds-surface-0));
    border-color: #b44c36;
  }

  /* Career Rank Pills & Warden Editorial Callout */
  .arena-rank-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px;
    margin-top: 10px;
  }

  .arena-rank-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 7px;
    border: 1px solid var(--cds-border-subtle);
    background: var(--cds-surface-0);
    font-family: var(--cds-font-sans);
    font-size: 12px;
    color: var(--cds-text-muted);
    transition: all 0.14s ease;
  }

  .arena-rank-chip code {
    font-family: var(--cds-font-mono);
    font-size: 10.5px;
    color: var(--cds-text-muted);
  }

  .arena-rank-chip.cleared {
    color: var(--cds-text-secondary);
    border-color: color-mix(in oklab, var(--cds-clay) 28%, var(--cds-border-subtle));
  }

  .arena-rank-chip.current {
    background: var(--cds-fill-primary);
    border-color: var(--cds-fill-primary);
    color: var(--cds-text-on-primary);
    font-weight: 500;
  }

  .arena-rank-chip.current code {
    color: var(--cds-clay);
    font-weight: 600;
  }

  /* Warden Editorial Spine Card */
  .arena-warden-card {
    padding: 16px 20px;
    background: var(--cds-surface-1);
    border-radius: var(--cds-radius-card);
    box-shadow: var(--cds-shadow-card-ring);
    border: 1px solid var(--cds-border-default);
    transition: border-color 0.16s ease, background 0.16s ease;
  }

  .arena-warden-card.harsh {
    border-left: 3px solid #b44c36;
  }

  .arena-warden-card.praise {
    border-left: 3px solid #2c6b45;
  }

  /* Main Workspace Split: Question App-Window + Contextual Chat App-Window */
  .arena-workspace-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 20px;
    align-items: start;
  }

  @media (min-width: 1020px) {
    .arena-workspace-grid {
      grid-template-columns: minmax(0, 1.36fr) minmax(330px, 0.64fr);
    }
  }

  .arena-window-card {
    margin: 0;
    border-radius: var(--cds-radius-card);
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
    overflow: hidden;
    min-width: 0;
  }

  .arena-window-body {
    padding: 22px 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    background: var(--cds-surface-0);
  }

  .arena-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 2px 8px;
    border-radius: 5px;
    border: 1px solid var(--cds-border-subtle);
    background: var(--cds-surface-0);
    font-family: var(--cds-font-mono);
    font-size: 11px;
    font-weight: 500;
    color: var(--cds-text-secondary);
  }

  .arena-pill.tier-shift {
    background: var(--glossary-badge-bg);
    color: var(--glossary-badge-text);
    border-color: transparent;
    font-weight: 600;
  }

  .arena-pill.sla-warn {
    border-color: color-mix(in oklab, #b44c36 45%, transparent);
    background: color-mix(in oklab, #b44c36 10%, var(--cds-surface-0));
    color: #b44c36;
    font-weight: 600;
  }

  .arena-tier-context-box {
    padding: 12px 15px;
    border-radius: 10px;
    background: var(--cds-surface-1);
    border: 1px solid var(--cds-border-subtle);
    font-size: 13px;
    line-height: 1.55;
    color: var(--cds-text-secondary);
  }

  .arena-q-stem {
    font-family: var(--cds-font-sans);
    font-size: 16px;
    line-height: 1.66;
    letter-spacing: -0.003em;
    color: var(--cds-text-primary);
    margin: 0;
  }

  .arena-code-block {
    margin: 0;
    padding: 14px 16px;
    border-radius: 10px;
    background: var(--code-block-bg, var(--cds-surface-1));
    box-shadow: var(--cds-shadow-card-ring);
    font-family: var(--cds-font-mono);
    font-size: 12.5px;
    line-height: 1.52;
    color: var(--cds-text-primary);
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-word;
  }

  .arena-options-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .arena-option-btn {
    appearance: none;
    display: grid;
    grid-template-columns: 28px minmax(0, 1fr);
    align-items: baseline;
    gap: 12px;
    width: 100%;
    padding: 14px 16px;
    border-radius: 12px;
    border: 1px solid var(--cds-border-default);
    background: var(--cds-surface-1);
    color: var(--cds-text-primary);
    font-family: var(--cds-font-sans);
    font-size: 14.5px;
    line-height: 1.56;
    text-align: left;
    cursor: pointer;
    transition: background 0.15s var(--motion-ease), border-color 0.15s var(--motion-ease), transform 0.12s var(--motion-ease);
  }

  .arena-option-btn:hover:not(:disabled) {
    background: var(--cds-surface-2);
    border-color: var(--cds-border-strong);
    transform: translateY(-1px);
  }

  .arena-option-btn.selected {
    border-color: var(--cds-clay);
    background: color-mix(in oklab, var(--cds-clay) 8%, var(--cds-surface-1));
  }

  .arena-option-btn.correct {
    border-color: #2c6b45;
    background: color-mix(in oklab, #2c6b45 10%, var(--cds-surface-1));
  }

  .arena-option-btn.wrong {
    border-color: #b44c36;
    background: color-mix(in oklab, #b44c36 10%, var(--cds-surface-1));
  }

  .arena-opt-letter {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    border-radius: 7px;
    background: var(--cds-surface-0);
    box-shadow: var(--cds-shadow-card-ring);
    font-family: var(--cds-font-mono);
    font-size: 12px;
    font-weight: 600;
    color: var(--cds-text-primary);
  }

  .arena-option-btn.correct .arena-opt-letter {
    background: #2c6b45;
    color: #ffffff;
  }

  .arena-option-btn.wrong .arena-opt-letter {
    background: #b44c36;
    color: #ffffff;
  }

  .arena-l3-defense-box {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 16px 18px;
    border-radius: 12px;
    background: var(--cds-surface-1);
    border: 1px solid var(--cds-border-default);
  }

  .arena-textarea,
  .arena-l3-textarea {
    width: 100%;
    min-height: 128px;
    padding: 12px 14px;
    border-radius: 8px;
    border: 1px solid var(--cds-border-default);
    background: var(--cds-surface-0);
    color: var(--cds-text-primary);
    font-family: var(--cds-font-sans);
    font-size: 14px;
    line-height: 1.58;
    resize: vertical;
    outline: none;
  }

  .arena-textarea:focus,
  .arena-l3-textarea:focus {
    border-color: var(--cds-clay);
  }

  /* Post-Submit Editorial Breakdown */
  .arena-feedback-panel {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 18px 20px;
    border-radius: 12px;
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
  }

  .arena-feedback-panel.pass {
    border-left: 3px solid #2c6b45;
  }

  .arena-feedback-panel.fail {
    border-left: 3px solid #b44c36;
  }

  .arena-distractor-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin: 4px 0 0;
    padding: 0;
    list-style: none;
  }

  .arena-distractor-item {
    padding: 9px 12px;
    border-radius: 8px;
    background: var(--cds-surface-0);
    border: 1px solid var(--cds-border-subtle);
    font-size: 13px;
    line-height: 1.54;
    color: var(--cds-text-secondary);
  }

  /* In-Arena Contextual Study Chat Window */
  .arena-chat-card {
    display: flex;
    flex-direction: column;
    min-height: 480px;
    max-height: 680px;
    border-radius: var(--cds-radius-card);
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
    overflow: hidden;
    min-width: 0;
  }

  .arena-chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    background: var(--cds-surface-0);
  }

  .arena-chat-bubble {
    padding: 11px 14px;
    border-radius: 10px;
    font-size: 13.5px;
    line-height: 1.56;
    word-break: break-word;
  }

  .arena-chat-bubble.user {
    align-self: flex-end;
    max-width: 88%;
    background: var(--cds-surface-2);
    border: 1px solid var(--cds-border-default);
    color: var(--cds-text-primary);
  }

  .arena-chat-bubble.assistant {
    align-self: flex-start;
    max-width: 94%;
    background: var(--cds-surface-1);
    border: 1px solid var(--cds-border-subtle);
    color: var(--cds-text-primary);
  }

  .arena-chat-bubble.warden {
    align-self: flex-start;
    max-width: 94%;
    background: color-mix(in oklab, #b44c36 8%, var(--cds-surface-1));
    border-left: 3px solid #b44c36;
    color: var(--cds-text-primary);
  }

  .arena-chat-quick-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    padding: 9px 14px;
    background: var(--cds-surface-1);
    border-top: 1px solid var(--cds-border-subtle);
  }

  .arena-chat-chip {
    appearance: none;
    padding: 4px 10px;
    border-radius: 7px;
    border: 1px solid var(--cds-border-subtle);
    background: var(--cds-surface-0);
    color: var(--cds-text-secondary);
    font-family: var(--cds-font-sans);
    font-size: 11.5px;
    cursor: pointer;
    transition: background 0.14s, color 0.14s, border-color 0.14s;
  }

  .arena-chat-chip:hover {
    background: var(--cds-fill-ghost-hover);
    border-color: var(--cds-border-strong);
    color: var(--cds-text-primary);
  }

  .arena-chat-input-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 14px;
    background: var(--cds-surface-1);
    border-top: 1px solid var(--cds-border-subtle);
  }

  /* Centered Anthropic-Style Modals */
  .arena-modal-dialog {
    width: min(740px, 96vw);
    max-height: 86vh;
    background: var(--cds-surface-0);
    border-radius: 16px;
    box-shadow: var(--cds-shadow-modal);
    border: 1px solid var(--cds-border-default);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .arena-modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 16px 22px;
    background: var(--cds-surface-1);
    border-bottom: 1px solid var(--cds-border-subtle);
  }

  .arena-modal-title {
    margin: 0;
    font-family: var(--cds-font-serif);
    font-size: 19px;
    font-weight: 400;
    letter-spacing: -0.015em;
    color: var(--cds-text-primary);
  }

  .arena-modal-body {
    flex: 1;
    overflow-y: auto;
    padding: 20px 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .arena-account-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 12px;
  }

  .arena-account-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 10px;
    padding: 15px 17px;
    border-radius: 12px;
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
  }

  .arena-account-card.active {
    box-shadow: 0 0 0 1.5px var(--cds-clay), var(--cds-shadow-card-ring);
    background: color-mix(in oklab, var(--cds-clay) 6%, var(--cds-surface-1));
  }

  @media (max-width: 640px) {
    .arena-window-body,
    .arena-gate-card {
      padding: 16px;
    }
  }
"""

ARENA_JS = r"""
  /* ==========================================================================
     AI ADAPTIVE PRACTICE & CAREER MASTERY ARENA ENGINE
     ========================================================================== */
  const ARENA_STORAGE_KEY = "fsds_arena_multi_account_v3";
  const ARENA_IDB_NAME = "fsds_arena_memory_db_v2";
  const ARENA_IDB_STORE = "arena_state_snapshots";

  let arenaRuntime = {
    initialized: false,
    isLoggedIn: false,
    activeAccountId: "virt_sinhvien_fresh",
    accounts: {},
    aiConfig: {
      providerId: "gemini",
      protocol: "gemini",
      baseUrl: "https://generativelanguage.googleapis.com/v1beta",
      apiKey: "",
      model: "models/gemini-2.5-flash",
      fetchedModels: [],
      lastFetchStatus: ""
    },
    supabaseConfig: {
      url: "",
      anonKey: "",
      syncStatus: "Local-First + IndexedDB Ready"
    },
    activeModal: null, // 'warden' | 'provider' | 'accounts' | null
    dwellTimerId: null,
    lastTickTs: 0,
    hotDigestCache: null,
    hotDigestPerfMs: 0.08
  };

  function getArenaCatalog() {
    return (typeof HUB_DATA !== "undefined" && HUB_DATA.arena) ? HUB_DATA.arena : {
      ranks: [],
      levels: [],
      mutationDomains: [],
      providerPresets: [],
      wardenConfig: { slaMs: { L1: 45000, L2: 75000, L3: 180000 } },
      virtualAccounts: [],
      blueprints: []
    };
  }

  function isArenaEn() {
    if (typeof currentAppLang !== "undefined") return currentAppLang === "en";
    return typeof state !== "undefined" && state.language === "en";
  }

  function arenaTr(viText, enText) {
    return isArenaEn() ? enText : viText;
  }

  /* --------------------------------------------------------------------------
     1. COMPLETE 49-COURSE BLUEPRINT COVERAGE (CANONICAL + DYNAMIC SYNTHESIS)
     -------------------------------------------------------------------------- */
  let _allBlueprintsCache = null;
  function getAllArenaBlueprints() {
    if (_allBlueprintsCache) return _allBlueprintsCache;
    const cat = getArenaCatalog();
    const list = Array.isArray(cat.blueprints) ? cat.blueprints.slice() : [];
    const coveredTopics = new Set(list.map((b) => b.topic));

    if (typeof SYLLABUS_GROUPS !== "undefined" && Array.isArray(SYLLABUS_GROUPS)) {
      SYLLABUS_GROUPS.forEach((grp) => {
        (grp.items || []).forEach((item) => {
          if (coveredTopics.has(item.code)) return;
          coveredTopics.add(item.code);
          list.push(synthesizeTopicBlueprint(item, grp));
        });
      });
    }
    _allBlueprintsCache = list;
    return _allBlueprintsCache;
  }

  function synthesizeTopicBlueprint(item, grp) {
    const code = item.code;
    const title = item.title || code;
    const summary = item.summary || "Nắm vững nguyên lý cốt lõi và vận hành thực chiến trên Production.";
    const bullets = (Array.isArray(item.bullets) && item.bullets.length >= 2)
      ? item.bullets
      : [summary, "Kiểm soát độ trễ, thông lượng và tính toàn vẹn dữ liệu ở quy mô lớn."];

    const hashNum = Array.from(code).reduce((acc, ch) => acc + ch.charCodeAt(0), 0);
    const l1Correct = hashNum % 4;
    const l2Correct = (hashNum + 1) % 4;
    const l3Correct = (hashNum + 2) % 4;

    function placeCorrectAt(correctOpt, distractors, targetIdx) {
      const opts = distractors.slice(0, 3);
      opts.splice(targetIdx, 0, correctOpt);
      return opts;
    }

    const l1Opts = placeCorrectAt(
      `Bảo toàn bất biến cốt lõi của ${title}: ${bullets[0]} — kết hợp kiểm chứng định lượng thay vì áp dụng cấu hình mù quáng.`,
      [
        `Bỏ qua hoàn toàn cơ chế kiểm soát trạng thái của ${title} và phó mặc cho phần cứng tự xử lý.`,
        `Tăng cấu hình bộ nhớ lên tối đa 100% RAM mà không cần phân tích nguyên nhân gốc rễ hay phân phối dữ liệu.`,
        `Tắt toàn bộ cơ chế kiểm định tính đúng đắn (Validation & Observability) để lấy tốc độ thực thi ảo.`
      ],
      l1Correct
    );

    const l2Opts = placeCorrectAt(
      `Phân tích trực tiếp số liệu thực thi của ${title} (${bullets[1] || bullets[0]}), khoanh vùng điểm nghẽn I/O hoặc lệch tải trước khi tinh chỉnh tham số có kiểm soát.`,
      [
        `Khởi động lại máy chủ định kỳ mỗi 5 phút bằng cronjob để xóa triệu chứng lỗi tạm thời.`,
        `Dùng câu lệnh bọc ngoài che giấu lỗi (silent try/catch hoặc DISTINCT mù quáng) khiến dữ liệu đầu ra bị sai lệch âm thầm.`,
        `Xóa toàn bộ dữ liệu lịch sử trên Production mỗi khi gặp cảnh báo độ trễ vượt ngưỡng SLA.`
      ],
      l2Correct
    );

    const l3Opts = placeCorrectAt(
      `Thiết kế kiến trúc ${title} theo nguyên lý phòng thủ nhiều lớp: đảm bảo tính lũy đẳng (Idempotency), cô lập lỗi (Fault Isolation) và giám sát SLA thực tế.`,
      [
        `Ghép chặt (tightly couple) mọi thành phần vào một tiến trình đơn luồng duy nhất không có cơ chế dự phòng.`,
        `Bỏ qua toàn bộ kiểm thử biên và đẩy thẳng cấu hình thử nghiệm lên cụm Production giờ cao điểm.`,
        `Lưu trữ toàn bộ trạng thái trọng yếu (critical) trên vùng nhớ tạm thời dễ bay hơi mà không có cơ chế đối soát hay phục hồi.`
      ],
      l3Correct
    );

    return {
      id: `${code}-BP-01`,
      topic: code,
      stage: 1,
      stationId: `${code.toLowerCase()}-1-1`,
      stationTitle: `${code} · ${title}`,
      roleTracks: ["DE", "AIE", "MLE"],
      skillName: `${code}: ${title}`,
      invariant: `${title}: ${summary} Trọng tâm kỹ thuật: ${bullets.slice(0, 2).join(" | ")}`,
      misconceptions: [
        `Áp dụng ${title} theo kiểu học vẹt công cụ mà không hiểu cơ chế gốc bên dưới.`,
        `Bỏ qua đánh đổi giữa Độ trễ (Latency), Chi phí (Cost) và Độ tin cậy (Reliability) khi mở rộng quy mô.`
      ],
      L1: {
        stem: `Trong chuyên đề ${code} (${title}), nguyên lý kỹ thuật cốt lõi nào dưới đây đảm bảo hệ thống vận hành đúng bản chất cơ học?`,
        options: l1Opts,
        correctIndex: l1Correct,
        explanation: `Nguyên lý bất biến của ${code} (${title}): ${summary} (${bullets[0]}).`,
        distractorReasons: [
          "Phản ánh đúng cơ chế gốc hoặc bẫy tư duy tương ứng của phương án.",
          "Phản ánh đúng cơ chế gốc hoặc bẫy tư duy tương ứng của phương án.",
          "Phản ánh đúng cơ chế gốc hoặc bẫy tư duy tương ứng của phương án.",
          "Phản ánh đúng cơ chế gốc hoặc bẫy tư duy tương ứng của phương án."
        ]
      },
      L2: {
        stem: `Khi vận hành ${code} (${title}) ở quy mô Production, hệ thống xuất hiện điểm nghẽn liên quan đến: "${bullets[1] || bullets[0]}". Phương án xử lý nào giải quyết tận gốc cơ chế thay vì vá tạm bợ?`,
        codeSnippet: `# Telemetry Alert · ${code} (${title})\n# Symptom: SLA degradation under peak production workload\n# Focus: ${bullets[0]}`,
        options: l2Opts,
        correctIndex: l2Correct,
        explanation: `Ở cấp độ Chuyên sâu (L2), mọi quyết định tối ưu ${title} đều phải dựa trên bằng chứng đo đạc (Metrics/Logs/Execution Plan) và giải quyết tận gốc: ${bullets[1] || bullets[0]}.`,
        distractorReasons: [
          "Phân tích kỹ thuật cho phương án A.",
          "Phân tích kỹ thuật cho phương án B.",
          "Phân tích kỹ thuật cho phương án C.",
          "Phân tích kỹ thuật cho phương án D."
        ]
      },
      L3: {
        stem: `Kịch bản Phỏng vấn Thiết kế & Phản biện (${code} · ${title}): Bạn chịu trách nhiệm kiến trúc mô-đun ${title} phục vụ lưu lượng cao với yêu cầu nghiêm ngặt về SLA và độ tin cậy.`,
        mcqPrompt: `Phần A (Quyết định Kiến trúc): Nguyên tắc thiết kế nào cần được chốt làm nền tảng cho ${code}?`,
        options: l3Opts,
        correctIndex: l3Correct,
        openPrompt: `Phần B (Bảo vệ Thiết kế & Đánh đổi): Hãy trình bày bằng lời của bạn: (1) Cơ chế cốt lõi của ${title} (${bullets[0]}), (2) Kịch bản lỗi nguy hiểm nhất khi tải tăng đột biến và cách phòng chống, (3) Đánh đổi kỹ thuật (Trade-off) mà bạn chấp nhận.`,
        rubric: {
          coreConcepts: [
            bullets[0],
            bullets[1] || summary,
            "Phân tích kịch bản lỗi (Failure Mode) và cơ chế tự phục hồi / lũy đẳng (Idempotency)."
          ],
          tradeoffs: [
            "Cân bằng giữa Độ trễ (Latency), Thông lượng (Throughput), Chi phí (Cost) và Độ phức tạp vận hành."
          ],
          referenceAnswer: `1. Cơ chế cốt lõi của ${title}: ${bullets[0]}.\n2. Kiểm soát chuyên sâu: ${bullets[1] || summary}.\n3. Đánh đổi thực chiến: Thiết lập giới hạn tài nguyên, cơ chế thử lại lũy đẳng (Idempotent Retry) và giám sát chủ động để bảo vệ SLA toàn trình.`
        }
      }
    };
  }

  /* --------------------------------------------------------------------------
     2. VIRTUAL ACCOUNTS SEEDING & ULTRA-FAST COGNITIVE MEMORY DB (<0.2ms)
     -------------------------------------------------------------------------- */
  function ensureAccountProfileMemory(acc) {
    if (!acc) return null;
    if (!acc.profileMemory) {
      acc.profileMemory = {
        githubVerified: false,
        avatarUrl: "",
        githubBio: "",
        githubReposCount: 0,
        githubToken: "",
        gistId: "",
        syncMode: "local_idb",
        lastCloudSyncAt: 0,
        lastSyncStatus: "LocalStorage + IndexedDB Active",
        totalStudyTimeMs: 0,
        totalQuestionsSolved: 0,
        totalCorrectAnswers: 0,
        totalChatQuestionsAsked: 0,
        mistakePatterns: [],
        masteredTopicsList: [],
        recentChatQueries: []
      };
    }
    if (!Array.isArray(acc.profileMemory.mistakePatterns)) acc.profileMemory.mistakePatterns = [];
    if (!Array.isArray(acc.profileMemory.masteredTopicsList)) acc.profileMemory.masteredTopicsList = [];
    if (!Array.isArray(acc.profileMemory.recentChatQueries)) acc.profileMemory.recentChatQueries = [];
    return acc.profileMemory;
  }

  function createBlankAccount(accountId, displayName, githubHandle, roleTrack, presetType) {
    const acc = {
      accountId: accountId || ("virt_" + Date.now()),
      displayName: displayName || "Kỹ sư Thực Chiến",
      githubHandle: githubHandle || "fsds-engineer",
      roleTrack: roleTrack || "DE",
      presetType: presetType || "custom",
      verifiedRankTier: 1,
      verifiedRankId: "student",
      totalXp: 0,
      selectedTopic: "F01",
      selectedLevel: 1,
      mastery: {}, // blueprintId -> { topic, l1Best, l2Best, l3Best, l1Unassisted, l2Unassisted, l3Unassisted, attempts, slaBreaches, seenFingerprints: [] }
      attemptHistory: [],
      chatThreads: {}, // instanceId -> [{ role, content, phase, ts, spoilerBlocked }]
      activeSession: null,
      wardenState: {
        tone: "neutral",
        lastCommentVi: "Chưa có dữ liệu làm bài. Chọn đáp án đi, đừng ngồi ngắm đề — tôi đang bấm giờ đấy.",
        lastCommentEn: "Zero attempts logged. Pick an answer instead of staring at the screen — the SLA clock is ticking.",
        slaBreachCount: 0,
        antiGrindFlags: 0,
        lastAuditReportVi: "",
        lastAuditReportEn: ""
      },
      updatedAt: Date.now()
    };
    ensureAccountProfileMemory(acc);
    return acc;
  }

  function seedPresetAccountData(acc) {
    ensureAccountProfileMemory(acc);
    const bps = getAllArenaBlueprints();
    if (acc.presetType === "anti_grind_victim") {
      // Farmed F01 18 times (2,400 XP) but 0 other topics!
      acc.totalXp = 2400;
      acc.selectedTopic = "F01";
      acc.mastery["F01-BP-01"] = {
        topic: "F01",
        l1Best: 100,
        l2Best: 100,
        l3Best: 0,
        l1Unassisted: 1,
        l2Unassisted: 1,
        l3Unassisted: 0,
        attempts: 18,
        slaBreaches: 2,
        seenFingerprints: ["F01-BP-01:L1:d0", "F01-BP-01:L1:d1", "F01-BP-01:L2:d0"]
      };
      acc.profileMemory.totalStudyTimeMs = 540000;
      acc.profileMemory.totalQuestionsSolved = 18;
      acc.profileMemory.totalCorrectAnswers = 16;
      acc.profileMemory.totalChatQuestionsAsked = 2;
      acc.profileMemory.masteredTopicsList = ["F01"];
      acc.profileMemory.mistakePatterns = ["F01:L3 (Né tránh câu hỏi tự luận bảo vệ kiến trúc L3)"];
      acc.profileMemory.recentChatQueries = ["F01(L1): Tại sao cày 2400 XP mà vẫn chưa lên Intern?"];
      acc.wardenState = {
        tone: "harsh",
        lastCommentVi: "Ông cày đi cày lại bài F01 tới 18 lần để tích 2.400 XP ảo mà không dám đụng vào L3 hay các chuyên đề SQL/Spark/API khác à? Đừng mơ lên cấp với tôi! Vẫn giam ở T1 · Sinh viên.",
        lastCommentEn: "You farmed F01 18 times for 2,400 vanity XP while dodging Level 3 and every other course in the syllabus? Zero chance of promotion under my watch. Locked at T1 · Student.",
        slaBreachCount: 2,
        antiGrindFlags: 16,
        lastAuditReportVi: "",
        lastAuditReportEn: ""
      };
    } else if (acc.presetType === "slow_and_flawed") {
      acc.totalXp = 210;
      acc.selectedTopic = "F03";
      acc.mastery["F02-BP-01"] = {
        topic: "F02",
        l1Best: 0,
        l2Best: 0,
        l3Best: 0,
        l1Unassisted: 0,
        l2Unassisted: 0,
        l3Unassisted: 0,
        attempts: 4,
        slaBreaches: 4,
        seenFingerprints: ["F02-BP-01:L1:d0"]
      };
      acc.mastery["F03-BP-01"] = {
        topic: "F03",
        l1Best: 100,
        l2Best: 0,
        l3Best: 0,
        l1Unassisted: 0,
        l2Unassisted: 0,
        l3Unassisted: 0,
        attempts: 3,
        slaBreaches: 3,
        seenFingerprints: ["F03-BP-01:L1:d0"]
      };
      acc.attemptHistory = [
        {
          id: "att_slow_1",
          topic: "F02",
          blueprintId: "F02-BP-01",
          level: 1,
          isCorrect: false,
          scorePct: 0,
          activeAnswerMs: 112000,
          slaTargetMs: 45000,
          slaBreached: true,
          assisted: true,
          ts: Date.now() - 3600000
        },
        {
          id: "att_slow_2",
          topic: "F03",
          blueprintId: "F03-BP-01",
          level: 2,
          isCorrect: false,
          scorePct: 0,
          activeAnswerMs: 138000,
          slaTargetMs: 75000,
          slaBreached: true,
          assisted: false,
          ts: Date.now() - 1800000
        }
      ];
      acc.profileMemory.totalStudyTimeMs = 820000;
      acc.profileMemory.totalQuestionsSolved = 7;
      acc.profileMemory.totalCorrectAnswers = 1;
      acc.profileMemory.totalChatQuestionsAsked = 5;
      acc.profileMemory.mistakePatterns = [
        "F02:L1 (Nhầm lẫn Python GIL vs Multiprocessing cho tác vụ CPU-bound)",
        "F03:L2 (Không phân biệt được MVCC Snapshot Isolation và Deadlock)"
      ];
      acc.profileMemory.recentChatQueries = [
        "F02(L1): Cho mình xin đáp án đúng câu này với?",
        "F03(L2): Tại sao câu truy vấn bị chậm quá SLA?"
      ];
      acc.wardenState = {
        tone: "harsh",
        lastCommentVi: "Câu L1 nền tảng mà ngâm tới 112 giây (vượt gấp đôi SLA 45s) xong vẫn chọn trúng bẫy sơ đẳng! Kiến thức nền về Python GIL và MVCC đang thủng lỗ chỗ, phải đọc lại bài ngay.",
        lastCommentEn: "112 seconds on a foundational Level 1 question (over 2x the 45s SLA) only to pick the most obvious distractor trap! Your Python GIL and MVCC fundamentals are leaking badly.",
        slaBreachCount: 7,
        antiGrindFlags: 0,
        lastAuditReportVi: "",
        lastAuditReportEn: ""
      };
    } else if (acc.presetType === "solid_junior") {
      acc.totalXp = 2450;
      acc.selectedTopic = "D03";
      acc.selectedLevel = 2;
      ["F01-BP-01", "F02-BP-01", "F03-BP-01", "D01-BP-01", "D03-BP-01"].forEach((bpId) => {
        const tCode = bpId.split("-")[0];
        acc.mastery[bpId] = {
          topic: tCode,
          l1Best: 100,
          l2Best: 100,
          l3Best: 88,
          l1Unassisted: 1,
          l2Unassisted: 1,
          l3Unassisted: 1,
          attempts: 3,
          slaBreaches: 0,
          seenFingerprints: [`${bpId}:L1:d0`, `${bpId}:L2:d1`, `${bpId}:L3:d2`]
        };
      });
      acc.verifiedRankTier = 4;
      acc.verifiedRankId = "junior";
      acc.profileMemory.totalStudyTimeMs = 1420000;
      acc.profileMemory.totalQuestionsSolved = 15;
      acc.profileMemory.totalCorrectAnswers = 14;
      acc.profileMemory.totalChatQuestionsAsked = 4;
      acc.profileMemory.masteredTopicsList = ["F01", "F02", "F03", "D01", "D03"];
      acc.profileMemory.mistakePatterns = ["D03:L3 (Thiếu cấu hình Salting Key khi xử lý Skew Join lớn)"];
      acc.profileMemory.recentChatQueries = ["D03(L2): Khi nào nên bật AQE 대신 Broadcast Hash Join?"];
      acc.wardenState = {
        tone: "praise",
        lastCommentVi: "Đã chứng minh năng lực tự lập qua 5 chuyên đề (cả L1, L2 và bảo vệ kiến trúc L3) trong chuẩn SLA. Công nhận trình độ thực tế: T4 · Junior Engineer. Giờ toàn bộ đề đã tự động đẩy độ khó lên chuẩn Junior!",
        lastCommentEn: "Proven unassisted mastery across 5 core topics (L1, L2, and L3 defense) within SLA. Certified rank: T4 · Junior Engineer. Global question complexity has shifted to Junior tier.",
        slaBreachCount: 0,
        antiGrindFlags: 0,
        lastAuditReportVi: "",
        lastAuditReportEn: ""
      };
    } else if (acc.presetType === "senior_plus_master") {
      acc.totalXp = 12800;
      acc.selectedTopic = "S21";
      acc.selectedLevel = 3;
      bps.slice(0, 12).forEach((bp) => {
        acc.mastery[bp.id] = {
          topic: bp.topic,
          l1Best: 100,
          l2Best: 100,
          l3Best: 95,
          l1Unassisted: 1,
          l2Unassisted: 1,
          l3Unassisted: 1,
          attempts: 3,
          slaBreaches: 0,
          seenFingerprints: [`${bp.id}:L1:d0`, `${bp.id}:L2:d1`, `${bp.id}:L3:d2`]
        };
      });
      acc.verifiedRankTier = 7;
      acc.verifiedRankId = "senior_plus";
      acc.profileMemory.totalStudyTimeMs = 4680000;
      acc.profileMemory.totalQuestionsSolved = 36;
      acc.profileMemory.totalCorrectAnswers = 36;
      acc.profileMemory.totalChatQuestionsAsked = 9;
      acc.profileMemory.masteredTopicsList = bps.slice(0, 12).map((b) => b.topic);
      acc.profileMemory.mistakePatterns = [];
      acc.profileMemory.recentChatQueries = ["S21(L3): Phân tích trade-off giữa Dynamic Batching và PagedAttention trên cụm H100"];
      acc.wardenState = {
        tone: "praise",
        lastCommentVi: "Hiếm lắm tôi mới phải gật đầu: 12 chuyên đề từ Kernel/DB/Spark/Flink đến GPU Triton đều qua L1-L2-L3 sắc bén không cần gợi ý. Xứng đáng bậc T7 · Senior+ / Staff Architect!",
        lastCommentEn: "Rarely do I nod in approval: 12 topics from Kernel/DB/Spark/Flink to GPU Triton cleared across L1-L2-L3 unassisted. Certified T7 · Senior+ / Staff Architect!",
        slaBreachCount: 0,
        antiGrindFlags: 0,
        lastAuditReportVi: "",
        lastAuditReportEn: ""
      };
    }
    return acc;
  }

  function initArenaPersistence() {
    if (arenaRuntime.initialized) return;
    const cat = getArenaCatalog();
    let loaded = null;
    try {
      const raw = localStorage.getItem(ARENA_STORAGE_KEY);
      if (raw) loaded = JSON.parse(raw);
    } catch (err) {
      loaded = null;
    }

    if (loaded && loaded.accounts && Object.keys(loaded.accounts).length > 0) {
      arenaRuntime.accounts = loaded.accounts;
      arenaRuntime.activeAccountId = loaded.activeAccountId || Object.keys(loaded.accounts)[0];
      if (typeof loaded.isLoggedIn === "boolean") {
        arenaRuntime.isLoggedIn = loaded.isLoggedIn;
      }
      if (loaded.aiConfig) {
        arenaRuntime.aiConfig = Object.assign(arenaRuntime.aiConfig, loaded.aiConfig);
      }
      if (loaded.supabaseConfig) {
        arenaRuntime.supabaseConfig = Object.assign(arenaRuntime.supabaseConfig, loaded.supabaseConfig);
      }
    }

    // Ensure all 5 preset virtual accounts always exist
    (cat.virtualAccounts || []).forEach((preset) => {
      if (!arenaRuntime.accounts[preset.accountId]) {
        const acc = createBlankAccount(
          preset.accountId,
          preset.displayName,
          preset.githubHandle,
          preset.roleTrack,
          preset.presetType
        );
        arenaRuntime.accounts[preset.accountId] = seedPresetAccountData(acc);
      }
    });

    Object.values(arenaRuntime.accounts).forEach((acc) => {
      ensureAccountProfileMemory(acc);
    });

    if (!arenaRuntime.accounts[arenaRuntime.activeAccountId]) {
      arenaRuntime.activeAccountId = "virt_sinhvien_fresh";
      if (!arenaRuntime.accounts[arenaRuntime.activeAccountId]) {
        arenaRuntime.accounts[arenaRuntime.activeAccountId] = createBlankAccount(
          "virt_sinhvien_fresh",
          "Nguyễn Minh An (Acc Ảo #1 · Sinh Viên Mới)",
          "minhan-student-dev",
          "DE",
          "fresh_student"
        );
      }
    }

    arenaRuntime.initialized = true;
    recomputeAccountAdjudication(getActiveArenaAccount());
    saveArenaPersistence();
  }

  function saveArenaPersistence() {
    try {
      const activeAcc = arenaRuntime.accounts[arenaRuntime.activeAccountId];
      if (activeAcc) {
        activeAcc.updatedAt = Date.now();
        ensureAccountProfileMemory(activeAcc);
      }
      const payload = {
        isLoggedIn: Boolean(arenaRuntime.isLoggedIn),
        activeAccountId: arenaRuntime.activeAccountId,
        accounts: arenaRuntime.accounts,
        aiConfig: arenaRuntime.aiConfig,
        supabaseConfig: arenaRuntime.supabaseConfig,
        savedAt: Date.now()
      };
      localStorage.setItem(ARENA_STORAGE_KEY, JSON.stringify(payload));
      mirrorToIndexedDB(payload);
    } catch (err) {
      // Ignore quota errors in restricted environments
    }
    rebuildHotCognitiveDigest();
  }

  function logoutArenaSession() {
    initArenaPersistence();
    arenaRuntime.isLoggedIn = false;
    arenaRuntime.activeModal = null;
    saveArenaPersistence();
    if (typeof activeTopic !== "undefined" && activeTopic === "PRACTICE") {
      renderArenaView();
    }
  }

  function mirrorToIndexedDB(payload) {
    try {
      if (typeof indexedDB === "undefined") return;
      const req = indexedDB.open(ARENA_IDB_NAME, 1);
      req.onupgradeneeded = function(ev) {
        const db = ev.target.result;
        if (!db.objectStoreNames.contains(ARENA_IDB_STORE)) {
          db.createObjectStore(ARENA_IDB_STORE, { keyPath: "id" });
        }
      };
      req.onsuccess = function(ev) {
        const db = ev.target.result;
        const tx = db.transaction(ARENA_IDB_STORE, "readwrite");
        const store = tx.objectStore(ARENA_IDB_STORE);
        store.put({ id: "latest_snapshot", payload: payload });
        // Also persist each user profile as an individual record in IndexedDB
        if (payload && payload.accounts) {
          Object.entries(payload.accounts).forEach(([accId, accData]) => {
            store.put({
              id: "account_" + accId,
              accountId: accId,
              githubHandle: accData.githubHandle,
              updatedAt: accData.updatedAt || Date.now(),
              account: accData
            });
          });
        }
      };
    } catch (e) {
      // Non-blocking IDB mirror
    }
  }

  function getActiveArenaAccount() {
    initArenaPersistence();
    const acc = arenaRuntime.accounts[arenaRuntime.activeAccountId];
    ensureAccountProfileMemory(acc);
    return acc;
  }

  /* --------------------------------------------------------------------------
     2B. MULTI-USER PROFILE LOGIN, GITHUB GIST DB & SUPABASE CLOUD DB SYNC
     -------------------------------------------------------------------------- */
  async function verifyAndFetchGitHubIdentity(githubHandle, displayName, roleTrack, githubToken) {
    initArenaPersistence();
    const cleanHandle = (githubHandle || "").trim().replace(/^@+/, "") || ("dev-" + Math.floor(Math.random() * 9000 + 1000));
    const cleanRole = roleTrack || "DE";
    const cleanToken = (githubToken || "").trim();

    let ghData = null;
    let verified = false;
    try {
      const headers = { "Accept": "application/vnd.github+json" };
      if (cleanToken) headers["Authorization"] = `Bearer ${cleanToken}`;
      // Query search/users first so non-existent/virtual handles return HTTP 200 (0 items) instead of triggering a browser 404 console error
      const searchRes = await fetch(
        `https://api.github.com/search/users?q=${encodeURIComponent(cleanHandle)}+in:login&per_page=5`,
        { headers }
      );
      if (searchRes.ok) {
        const searchJson = await searchRes.json();
        const exactMatch = (searchJson.items || []).find(
          (u) => (u.login || "").toLowerCase() === cleanHandle.toLowerCase()
        );
        if (exactMatch) {
          verified = true;
          ghData = exactMatch;
          const userRes = await fetch(`https://api.github.com/users/${encodeURIComponent(exactMatch.login)}`, { headers });
          if (userRes.ok) {
            ghData = await userRes.json();
          }
        }
      }
    } catch (err) {
      verified = false;
    }

    // Check if an account with this GitHub handle already exists in our DB
    let existingAcc = Object.values(arenaRuntime.accounts).find(
      (a) => (a.githubHandle || "").toLowerCase() === cleanHandle.toLowerCase()
    );

    if (!existingAcc) {
      const newId = "user_gh_" + cleanHandle.toLowerCase().replace(/[^a-z0-9_-]/g, "_");
      const resolvedName = (displayName && displayName.trim()) || (ghData && ghData.name) || cleanHandle;
      existingAcc = createBlankAccount(newId, resolvedName, cleanHandle, cleanRole, "github_user");
      arenaRuntime.accounts[newId] = existingAcc;
    } else {
      if (displayName && displayName.trim()) existingAcc.displayName = displayName.trim();
      if (roleTrack) existingAcc.roleTrack = cleanRole;
    }

    const pm = ensureAccountProfileMemory(existingAcc);
    pm.githubVerified = verified;
    if (ghData) {
      pm.avatarUrl = ghData.avatar_url || "";
      pm.githubBio = ghData.bio || "";
      pm.githubReposCount = Number(ghData.public_repos || 0);
      if (!displayName && ghData.name) existingAcc.displayName = ghData.name;
    }
    if (cleanToken) {
      pm.githubToken = cleanToken;
      pm.syncMode = "github_gist";
    }
    pm.lastSyncStatus = verified
      ? `GitHub Verified (@${cleanHandle} · ${pm.githubReposCount} repos)`
      : `Local Profile Active (@${cleanHandle})`;

    arenaRuntime.activeAccountId = existingAcc.accountId;
    arenaRuntime.isLoggedIn = true;
    saveArenaPersistence();
    return { account: existingAcc, verified: verified, ghData: ghData };
  }

  async function syncAccountWithGitHubGist(direction) {
    const acc = getActiveArenaAccount();
    const pm = ensureAccountProfileMemory(acc);
    const token = (pm.githubToken || "").trim();
    if (!token) {
      pm.lastSyncStatus = arenaTr("Cần nhập GitHub Token (quyền gist) để đồng bộ Cloud Gist", "GitHub Token (gist scope) required for Gist sync");
      saveArenaPersistence();
      return { ok: false, status: pm.lastSyncStatus };
    }

    const headers = {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    };
    const fileName = `fsds_arena_profile_${acc.githubHandle || acc.accountId}.json`;

    try {
      if (direction === "pull") {
        let targetGistId = (pm.gistId || "").trim();
        if (!targetGistId) {
          // Discover gist automatically from user's gists
          const listRes = await fetch("https://api.github.com/gists?per_page=30", { headers });
          if (!listRes.ok) throw new Error(`HTTP ${listRes.status}`);
          const gists = await listRes.json();
          const found = (gists || []).find((g) => g.files && (g.files[fileName] || g.files["fsds_arena_profile_memory.json"]));
          if (found) targetGistId = found.id;
        }
        if (!targetGistId) {
          throw new Error(arenaTr("Không tìm thấy Gist lưu trữ hồ sơ nào trên GitHub của bạn", "No Arena profile Gist found on your GitHub account"));
        }
        const getRes = await fetch(`https://api.github.com/gists/${encodeURIComponent(targetGistId)}`, { headers });
        if (!getRes.ok) throw new Error(`HTTP ${getRes.status}`);
        const gistObj = await getRes.json();
        const fileEntry = gistObj.files[fileName] || gistObj.files["fsds_arena_profile_memory.json"] || Object.values(gistObj.files || {})[0];
        if (!fileEntry || !fileEntry.content) throw new Error("Empty Gist payload");
        const imported = JSON.parse(fileEntry.content);
        const restoredAcc = imported.account || imported;
        if (restoredAcc && restoredAcc.accountId) {
          ensureAccountProfileMemory(restoredAcc);
          restoredAcc.profileMemory.githubToken = token;
          restoredAcc.profileMemory.gistId = targetGistId;
          restoredAcc.profileMemory.syncMode = "github_gist";
          restoredAcc.profileMemory.lastCloudSyncAt = Date.now();
          restoredAcc.profileMemory.lastSyncStatus = `Pulled from GitHub Gist (${targetGistId.slice(0, 8)})`;
          arenaRuntime.accounts[restoredAcc.accountId] = restoredAcc;
          arenaRuntime.activeAccountId = restoredAcc.accountId;
          saveArenaPersistence();
          return { ok: true, status: restoredAcc.profileMemory.lastSyncStatus };
        }
        throw new Error("Invalid profile JSON in Gist");
      } else {
        // Push active account to GitHub Gist
        const exportObj = {
          schemaVersion: 2,
          exportedAt: new Date().toISOString(),
          account: Object.assign({}, acc, {
            profileMemory: Object.assign({}, pm, { githubToken: "" }) // Never leak token inside gist body
          }),
          cognitiveDigest: readHotCognitiveDigest()
        };
        const bodyPayload = {
          description: `FSDS AI Practice Arena — Profile & Cognitive Memory DB (@${acc.githubHandle})`,
          public: false,
          files: {
            [fileName]: { content: JSON.stringify(exportObj, null, 2) },
            "fsds_arena_profile_memory.json": { content: JSON.stringify(exportObj, null, 2) }
          }
        };
        const targetGistId = (pm.gistId || "").trim();
        const url = targetGistId
          ? `https://api.github.com/gists/${encodeURIComponent(targetGistId)}`
          : "https://api.github.com/gists";
        const method = targetGistId ? "PATCH" : "POST";
        const res = await fetch(url, { method, headers, body: JSON.stringify(bodyPayload) });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        pm.gistId = data.id || targetGistId;
        pm.syncMode = "github_gist";
        pm.lastCloudSyncAt = Date.now();
        pm.lastSyncStatus = `Synced to GitHub Gist (${(pm.gistId || "").slice(0, 8)})`;
        saveArenaPersistence();
        return { ok: true, status: pm.lastSyncStatus, gistId: pm.gistId };
      }
    } catch (err) {
      pm.lastSyncStatus = `Gist Sync Error: ${err.message || "Network error"}`;
      saveArenaPersistence();
      return { ok: false, status: pm.lastSyncStatus };
    }
  }

  async function syncAccountWithSupabase(direction) {
    const acc = getActiveArenaAccount();
    const pm = ensureAccountProfileMemory(acc);
    const sbUrl = (arenaRuntime.supabaseConfig.url || "").trim().replace(/\/+$/, "");
    const sbKey = (arenaRuntime.supabaseConfig.anonKey || "").trim();
    if (!sbUrl || !sbKey) {
      arenaRuntime.supabaseConfig.syncStatus = arenaTr("Cần nhập Supabase URL & Anon Key để đồng bộ DB nhóm", "Supabase URL & Anon Key required for Team DB sync");
      saveArenaPersistence();
      return { ok: false, status: arenaRuntime.supabaseConfig.syncStatus };
    }

    const headers = {
      "apikey": sbKey,
      "Authorization": `Bearer ${sbKey}`,
      "Content-Type": "application/json"
    };

    try {
      if (direction === "pull_all") {
        const res = await fetch(`${sbUrl}/rest/v1/arena_user_memory_store?select=*&order=total_xp.desc&limit=50`, { headers });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const rows = await res.json();
        let count = 0;
        (rows || []).forEach((r) => {
          if (r && r.account_payload && r.account_id) {
            const remoteAcc = r.account_payload;
            ensureAccountProfileMemory(remoteAcc);
            remoteAcc.profileMemory.syncMode = "supabase_cloud";
            remoteAcc.profileMemory.lastCloudSyncAt = Date.now();
            remoteAcc.profileMemory.lastSyncStatus = "Synced from Supabase Team DB";
            arenaRuntime.accounts[r.account_id] = remoteAcc;
            count += 1;
          }
        });
        arenaRuntime.supabaseConfig.syncStatus = `Pulled ${count} user profile(s) from Supabase Team DB`;
        pm.lastSyncStatus = arenaRuntime.supabaseConfig.syncStatus;
        saveArenaPersistence();
        return { ok: true, count: count, status: arenaRuntime.supabaseConfig.syncStatus };
      } else {
        // Push current active account to Supabase
        const digest = readHotCognitiveDigest();
        const cleanAccCopy = Object.assign({}, acc, {
          profileMemory: Object.assign({}, pm, { githubToken: "" })
        });
        const rowPayload = {
          account_id: acc.accountId,
          github_handle: acc.githubHandle || "fsds-user",
          display_name: acc.displayName || "FSDS User",
          role_track: acc.roleTrack || "DE",
          verified_rank_tier: acc.verifiedRankTier || 1,
          verified_rank_id: acc.verifiedRankId || "student",
          total_xp: acc.totalXp || 0,
          topics_mastered_count: (acc.computedMetrics && acc.computedMetrics.topicsMasteredCount) || 0,
          avg_depth_pct: (acc.computedMetrics && acc.computedMetrics.avgDepthPct) || 0,
          l3_unassisted_count: (acc.computedMetrics && acc.computedMetrics.l3UnassistedCount) || 0,
          sla_breach_count: (acc.wardenState && acc.wardenState.slaBreachCount) || 0,
          anti_grind_flags: (acc.wardenState && acc.wardenState.antiGrindFlags) || 0,
          account_payload: cleanAccCopy,
          cognitive_digest: digest,
          updated_at: new Date().toISOString()
        };
        const postHeaders = Object.assign({}, headers, {
          "Prefer": "resolution=merge-duplicates,return=minimal"
        });
        const res = await fetch(`${sbUrl}/rest/v1/arena_user_memory_store`, {
          method: "POST",
          headers: postHeaders,
          body: JSON.stringify(rowPayload)
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        pm.syncMode = "supabase_cloud";
        pm.lastCloudSyncAt = Date.now();
        arenaRuntime.supabaseConfig.syncStatus = `Synced @${acc.githubHandle} to Supabase Team DB`;
        pm.lastSyncStatus = arenaRuntime.supabaseConfig.syncStatus;
        saveArenaPersistence();
        return { ok: true, status: arenaRuntime.supabaseConfig.syncStatus };
      }
    } catch (err) {
      arenaRuntime.supabaseConfig.syncStatus = `Supabase Sync Error: ${err.message || "Network error"}`;
      pm.lastSyncStatus = arenaRuntime.supabaseConfig.syncStatus;
      saveArenaPersistence();
      return { ok: false, status: arenaRuntime.supabaseConfig.syncStatus };
    }
  }

  function exportActiveAccountJson() {
    const acc = getActiveArenaAccount();
    const pm = ensureAccountProfileMemory(acc);
    const snapshot = {
      schemaVersion: 2,
      exportedAt: new Date().toISOString(),
      account: Object.assign({}, acc, {
        profileMemory: Object.assign({}, pm, { githubToken: "" })
      }),
      cognitiveDigest: readHotCognitiveDigest()
    };
    return JSON.stringify(snapshot, null, 2);
  }

  function importAccountJsonString(rawJson) {
    initArenaPersistence();
    const parsed = JSON.parse(rawJson);
    const acc = parsed.account || parsed;
    if (!acc || !acc.accountId) {
      throw new Error("Invalid Arena Profile JSON structure");
    }
    ensureAccountProfileMemory(acc);
    acc.profileMemory.lastSyncStatus = "Imported from JSON Backup";
    arenaRuntime.accounts[acc.accountId] = acc;
    arenaRuntime.activeAccountId = acc.accountId;
    saveArenaPersistence();
    return acc;
  }

  /* --------------------------------------------------------------------------
     3. ANTI-GRIND ADJUDICATION MATRIX & HOT COGNITIVE DIGEST (<0.2ms READ)
     -------------------------------------------------------------------------- */
  function recomputeAccountAdjudication(acc) {
    if (!acc) return;
    const pm = ensureAccountProfileMemory(acc);
    const cat = getArenaCatalog();
    const ranks = cat.ranks || [];
    const masteryEntries = Object.values(acc.mastery || {});

    let topicsMasteredCount = 0;
    let totalWeightedDepth = 0;
    let l3UnassistedCount = 0;
    let totalUnassistedPasses = 0;
    let totalAttempts = 0;
    const masteredTopics = [];

    masteryEntries.forEach((m) => {
      // Weighted depth per blueprint: L1 (20%) + L2 (35%) + L3 (45%)
      const depth = (Number(m.l1Best || 0) * 0.20) + (Number(m.l2Best || 0) * 0.35) + (Number(m.l3Best || 0) * 0.45);
      if (m.l1Best >= 80 && m.l2Best >= 80) {
        topicsMasteredCount += 1;
        totalWeightedDepth += depth;
        if (m.topic && !masteredTopics.includes(m.topic)) {
          masteredTopics.push(m.topic);
        }
      }
      if (m.l3Unassisted >= 1 && m.l3Best >= 70) {
        l3UnassistedCount += 1;
      }
      totalUnassistedPasses += (m.l1Unassisted || 0) + (m.l2Unassisted || 0) + (m.l3Unassisted || 0);
      totalAttempts += (m.attempts || 0);
    });

    pm.masteredTopicsList = masteredTopics;

    const avgDepthPct = topicsMasteredCount > 0 ? Math.round(totalWeightedDepth / topicsMasteredCount) : 0;
    const breadthPct = Math.min(100, Math.round((topicsMasteredCount / 12) * 100));

    // Determine highest rank where ALL anti-grind criteria are satisfied
    let verifiedTier = 1;
    let verifiedId = "student";
    ranks.forEach((r) => {
      if (
        topicsMasteredCount >= r.minTopicsMastered &&
        avgDepthPct >= r.minMasteryPct &&
        l3UnassistedCount >= r.minL3Passed
      ) {
        verifiedTier = r.tier;
        verifiedId = r.id;
      }
    });

    acc.verifiedRankTier = verifiedTier;
    acc.verifiedRankId = verifiedId;
    acc.computedMetrics = {
      topicsMasteredCount: topicsMasteredCount,
      breadthPct: breadthPct,
      avgDepthPct: avgDepthPct,
      l3UnassistedCount: l3UnassistedCount,
      totalUnassistedPasses: totalUnassistedPasses,
      totalAttempts: totalAttempts
    };
  }

  function rebuildHotCognitiveDigest() {
    const t0 = (typeof performance !== "undefined" && performance.now) ? performance.now() : Date.now();
    const acc = arenaRuntime.accounts[arenaRuntime.activeAccountId];
    if (!acc) return null;
    const pm = ensureAccountProfileMemory(acc);
    recomputeAccountAdjudication(acc);

    const weakSkills = [];
    const strongSkills = [];
    Object.entries(acc.mastery || {}).forEach(([bpId, m]) => {
      const depth = Math.round((m.l1Best * 0.2) + (m.l2Best * 0.35) + (m.l3Best * 0.45));
      if (depth < 65 || m.slaBreaches >= 2) {
        weakSkills.push(`${m.topic}(depth:${depth}%,slaBreach:${m.slaBreaches})`);
      } else if (depth >= 85) {
        strongSkills.push(`${m.topic}(depth:${depth}%)`);
      }
    });

    arenaRuntime.hotDigestCache = {
      schemaVersion: 2,
      accountId: acc.accountId,
      displayName: acc.displayName,
      githubHandle: acc.githubHandle,
      roleTrack: acc.roleTrack,
      verifiedRankTier: acc.verifiedRankTier,
      verifiedRankId: acc.verifiedRankId,
      totalXp: acc.totalXp,
      metrics: acc.computedMetrics,
      slaBreachCount: acc.wardenState.slaBreachCount || 0,
      antiGrindFlags: acc.wardenState.antiGrindFlags || 0,
      weakSkills: weakSkills.slice(0, 8),
      strongSkills: strongSkills.slice(0, 8),
      recentAttempts: (acc.attemptHistory || []).slice(-5),
      profileMemory: {
        githubVerified: !!pm.githubVerified,
        syncMode: pm.syncMode || "local_idb",
        totalStudyTimeMs: pm.totalStudyTimeMs || 0,
        totalQuestionsSolved: pm.totalQuestionsSolved || 0,
        totalCorrectAnswers: pm.totalCorrectAnswers || 0,
        totalChatQuestionsAsked: pm.totalChatQuestionsAsked || 0,
        mistakePatterns: (pm.mistakePatterns || []).slice(-8),
        masteredTopicsList: (pm.masteredTopicsList || []).slice(0, 49),
        recentChatQueries: (pm.recentChatQueries || []).slice(-6)
      },
      activeTopic: acc.selectedTopic,
      activeLevel: acc.selectedLevel
    };
    const t1 = (typeof performance !== "undefined" && performance.now) ? performance.now() : Date.now();
    arenaRuntime.hotDigestPerfMs = Math.max(0.02, Number((t1 - t0).toFixed(3)));
    return arenaRuntime.hotDigestCache;
  }

  function readHotCognitiveDigest() {
    if (!arenaRuntime.hotDigestCache) {
      return rebuildHotCognitiveDigest();
    }
    return arenaRuntime.hotDigestCache;
  }

  function buildUnifiedProfileContextPacket(includeSecretAnswer) {
    const digest = readHotCognitiveDigest();
    const acc = getActiveArenaAccount();
    const inst = acc ? acc.activeSession : null;
    const activeQuestionContext = inst ? {
      instanceId: inst.instanceId,
      topic: inst.topic,
      stationTitle: inst.stationTitle,
      levelKey: inst.levelKey,
      rankBadge: inst.rankBadge,
      roleTrack: inst.roleTrack,
      stem: inst.stem,
      options: inst.options,
      invariant: inst.invariant,
      submitted: !!inst.submitted,
      assisted: !!inst.assisted,
      activeAnswerMs: inst.activeAnswerMs || 0,
      slaTargetMs: inst.slaTargetMs || 45000,
      selectedOption: inst.selectedOption,
      correctOption: (includeSecretAnswer || inst.submitted) ? inst.options[inst.correctIndex] : "[HIDDEN_PRE_SUBMIT]",
      explanation: (includeSecretAnswer || inst.submitted) ? inst.explanation : "[HIDDEN_PRE_SUBMIT]"
    } : null;

    return {
      profile: {
        accountId: digest.accountId,
        displayName: digest.displayName,
        githubHandle: acc ? acc.githubHandle : "",
        roleTrack: digest.roleTrack,
        verifiedRankTier: digest.verifiedRankTier,
        verifiedRankId: digest.verifiedRankId,
        totalXp: digest.totalXp,
        breadthPct: digest.metrics.breadthPct,
        topicsMasteredCount: digest.metrics.topicsMasteredCount,
        avgDepthPct: digest.metrics.avgDepthPct,
        l3UnassistedCount: digest.metrics.l3UnassistedCount,
        slaBreachCount: digest.slaBreachCount,
        antiGrindFlags: digest.antiGrindFlags,
        weakSkills: digest.weakSkills,
        strongSkills: digest.strongSkills,
        recentAttempts: digest.recentAttempts,
        longTermMemory: digest.profileMemory
      },
      activeQuestion: activeQuestionContext
    };
  }

  /* --------------------------------------------------------------------------
     4. POLYMORPHIC QUESTION GENERATOR (ZERO EXACT REPEAT + RANK TIER SHIFT)
     -------------------------------------------------------------------------- */
  function getBlueprintForTopic(topicCode) {
    const bps = getAllArenaBlueprints();
    return bps.find((b) => b.topic === topicCode) || bps[0];
  }

  function generatePolymorphicInstance(acc, forceNewSeed) {
    const cat = getArenaCatalog();
    const bp = getBlueprintForTopic(acc.selectedTopic);
    const levelNum = Number(acc.selectedLevel || 1);
    const levelKey = "L" + levelNum;
    const rawLevel = bp[levelKey] || bp.L1;
    const ranks = cat.ranks || [];
    const currentRank = ranks.find((r) => r.tier === acc.verifiedRankTier) || ranks[0] || {
      tier: 1,
      title: "Sinh viên",
      enTitle: "Student",
      badgeCode: "T1 · STUDENT",
      tierDirective: "",
      jdExpectations: { DE: "", AIE: "", MLE: "" }
    };

    const mRecord = acc.mastery[bp.id] || {
      topic: bp.topic,
      l1Best: 0,
      l2Best: 0,
      l3Best: 0,
      l1Unassisted: 0,
      l2Unassisted: 0,
      l3Unassisted: 0,
      attempts: 0,
      slaBreaches: 0,
      seenFingerprints: []
    };
    acc.mastery[bp.id] = mRecord;

    const domains = cat.mutationDomains || [
      { id: "ecom_flash", name: "Sàn TMĐT Flash Sale 11/11", scale: "85.000 req/s" }
    ];

    // Pick a domain + variant index that has NOT been seen yet
    if (!Array.isArray(mRecord.seenFingerprints)) {
      mRecord.seenFingerprints = [];
    }
    let variantCounter = mRecord.seenFingerprints.length + (forceNewSeed ? 1 : 0);
    let domainIdx = (variantCounter + acc.verifiedRankTier) % domains.length;
    let chosenDomain = domains[domainIdx];
    let fingerprint = `${bp.id}:${levelKey}:T${currentRank.tier}:${acc.roleTrack}:${chosenDomain.id}:v${variantCounter}`;

    while (mRecord.seenFingerprints.includes(fingerprint)) {
      variantCounter += 1;
      domainIdx = (domainIdx + 1) % domains.length;
      chosenDomain = domains[domainIdx];
      fingerprint = `${bp.id}:${levelKey}:T${currentRank.tier}:${acc.roleTrack}:${chosenDomain.id}:v${variantCounter}`;
    }
    mRecord.seenFingerprints.push(fingerprint);

    // Permute options so even repeating the same blueprint has a fresh option order
    const origOptions = (rawLevel.options || []).slice();
    const origReasons = (rawLevel.distractorReasons || []).slice();
    const origCorrect = Number(rawLevel.correctIndex || 0);
    const indices = origOptions.map((_, idx) => idx);

    // Deterministic Fisher-Yates shuffle based on variantCounter + tier
    let seedVal = variantCounter * 31 + currentRank.tier * 17 + levelNum * 13;
    for (let i = indices.length - 1; i > 0; i--) {
      seedVal = (seedVal * 1103515245 + 12345) & 0x7fffffff;
      const j = seedVal % (i + 1);
      const tmp = indices[i];
      indices[i] = indices[j];
      indices[j] = tmp;
    }

    const shuffledOptions = indices.map((i) => origOptions[i]);
    const shuffledReasons = indices.map((i) => origReasons[i] || "");
    const newCorrectIndex = indices.indexOf(origCorrect);

    // Parametric context mutation for scale numbers & scenario framing
    const scaleFactor = 1 + (variantCounter % 5);
    const mutatedStem = applyParametricMutation(rawLevel.stem, scaleFactor, chosenDomain, currentRank, acc.roleTrack);

    const instance = {
      instanceId: "inst_" + Date.now() + "_" + (variantCounter % 1000),
      fingerprint: fingerprint,
      blueprintId: bp.id,
      topic: bp.topic,
      stationId: bp.stationId,
      stationTitle: bp.stationTitle,
      skillName: bp.skillName,
      invariant: bp.invariant,
      level: levelNum,
      levelKey: levelKey,
      rankTier: currentRank.tier,
      rankBadge: currentRank.badgeCode,
      rankTitle: isArenaEn() ? currentRank.enTitle : currentRank.title,
      roleTrack: acc.roleTrack,
      domainName: chosenDomain.name,
      domainScale: chosenDomain.scale,
      tierDirective: currentRank.tierDirective,
      jdExpectation: (currentRank.jdExpectations && currentRank.jdExpectations[acc.roleTrack]) || "",
      stem: mutatedStem,
      codeSnippet: rawLevel.codeSnippet || "",
      mcqPrompt: rawLevel.mcqPrompt || "",
      openPrompt: rawLevel.openPrompt || "",
      options: shuffledOptions,
      distractorReasons: shuffledReasons,
      correctIndex: newCorrectIndex,
      explanation: rawLevel.explanation || "",
      rubric: rawLevel.rubric || null,
      selectedOption: null,
      l3OpenDraft: "",
      submitted: false,
      assisted: false,
      isCorrect: false,
      scorePct: 0,
      l3Evaluation: null,
      activeAnswerMs: 0,
      slaTargetMs: (cat.wardenConfig && cat.wardenConfig.slaMs && cat.wardenConfig.slaMs[levelKey]) || 45000,
      slaWarned: false,
      aiMutated: false
    };

    acc.activeSession = instance;
    saveArenaPersistence();
    return instance;
  }

  function applyParametricMutation(stem, factor, domain, rank, roleTrack) {
    if (!stem) return "";
    let out = stem;
    if (factor > 1) {
      out = out
        .replace(/\b8888\b/g, String(8800 + factor * 37))
        .replace(/\b10423\b/g, String(10400 + factor * 53))
        .replace(/\b500\b/g, String(500 + factor * 100));
    }
    return `[Bối cảnh Thực chiến · ${rank.badgeCode} · ${roleTrack} · ${domain.name} (${domain.scale})] ${out}`;
  }

  /* --------------------------------------------------------------------------
     5. UNIVERSAL MULTI-PROVIDER AI CLIENT + AUTO FETCH MODELS
     -------------------------------------------------------------------------- */
  function getProviderPreset(providerId) {
    const cat = getArenaCatalog();
    const presets = cat.providerPresets || [];
    return presets.find((p) => p.id === providerId) || presets[0] || {
      id: "gemini",
      name: "Google Gemini API",
      protocol: "gemini",
      baseUrl: "https://generativelanguage.googleapis.com/v1beta",
      modelsPath: "/models",
      defaultModel: "models/gemini-2.5-flash",
      fallbackModels: ["models/gemini-2.5-flash"]
    };
  }

  async function fetchArenaProviderModels(providerId, baseUrl, apiKey) {
    const preset = getProviderPreset(providerId);
    const cleanBase = (baseUrl || preset.baseUrl || "").replace(/\/+$/, "");
    const cleanKey = (apiKey || "").trim();

    if (!cleanKey) {
      return {
        ok: false,
        models: preset.fallbackModels || [preset.defaultModel],
        statusMsg: arenaTr(
          "Chưa nhập API Key — đã nạp danh sách model chuẩn của hãng để bạn chọn trước.",
          "No API Key provided — loaded curated default models for this provider."
        )
      };
    }

    try {
      if (preset.protocol === "gemini") {
        const url = `${cleanBase}/models?key=${encodeURIComponent(cleanKey)}`;
        const resp = await fetch(url, { method: "GET" });
        if (resp.status === 400 || resp.status === 401 || resp.status === 403) {
          throw new Error(`HTTP ${resp.status}: API Key không hợp lệ hoặc bị từ chối.`);
        }
        const data = await resp.json();
        const models = ((data && data.models) || [])
          .filter((m) => !m.supportedGenerationMethods || m.supportedGenerationMethods.includes("generateContent"))
          .map((m) => m.name)
          .slice(0, 35);
        if (models.length > 0) {
          return {
            ok: true,
            models: models,
            statusMsg: arenaTr(
              `Fetch thành công ${models.length} models trực tiếp từ Google Gemini API!`,
              `Successfully fetched ${models.length} models from Google Gemini API!`
            )
          };
        }
      } else if (preset.protocol === "anthropic") {
        const url = `${cleanBase}/models`;
        const resp = await fetch(url, {
          method: "GET",
          headers: {
            "x-api-key": cleanKey,
            "anthropic-version": "2023-06-01",
            "anthropic-dangerous-direct-browser-access": "true"
          }
        });
        if (resp.status === 401 || resp.status === 403) {
          throw new Error(`HTTP ${resp.status}: Anthropic API Key không hợp lệ.`);
        }
        const data = await resp.json();
        const models = ((data && data.data) || []).map((m) => m.id).filter(Boolean);
        if (models.length > 0) {
          return {
            ok: true,
            models: models,
            statusMsg: arenaTr(
              `Fetch thành công ${models.length} models từ Anthropic Claude API!`,
              `Successfully fetched ${models.length} models from Anthropic Claude API!`
            )
          };
        }
      } else {
        // OpenAI-compatible (/models) for OpenAI, Grok, DeepSeek, Qwen, GLM, Kimi, OpenRouter, Custom
        const url = `${cleanBase}${preset.modelsPath || "/models"}`;
        const resp = await fetch(url, {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${cleanKey}`
          }
        });
        if (resp.status === 401 || resp.status === 403) {
          throw new Error(`HTTP ${resp.status}: API Key bị từ chối (Unauthorized).`);
        }
        const data = await resp.json();
        const rawList = (data && (data.data || data.models)) || [];
        const models = rawList.map((m) => (typeof m === "string" ? m : (m.id || m.name))).filter(Boolean).slice(0, 50);
        if (models.length > 0) {
          return {
            ok: true,
            models: models,
            statusMsg: arenaTr(
              `Fetch thành công ${models.length} models từ ${preset.name}!`,
              `Successfully fetched ${models.length} models from ${preset.name}!`
            )
          };
        }
      }
    } catch (err) {
      const msg = String(err && err.message ? err.message : err);
      if (msg.includes("401") || msg.includes("403") || msg.includes("không hợp lệ")) {
        return {
          ok: false,
          models: preset.fallbackModels || [preset.defaultModel],
          statusMsg: msg
        };
      }
      return {
        ok: true,
        models: preset.fallbackModels || [preset.defaultModel],
        statusMsg: arenaTr(
          `Endpoint chặn CORS liệt kê /models trực tiếp trên trình duyệt — đã nạp sẵn ${preset.fallbackModels.length} model chuẩn của ${preset.name}.`,
          `Browser CORS restricted live /models listing — populated ${preset.fallbackModels.length} official models for ${preset.name}.`
        )
      };
    }

    return {
      ok: true,
      models: preset.fallbackModels || [preset.defaultModel],
      statusMsg: arenaTr("Đã nạp danh sách model chuẩn.", "Loaded default model catalog.")
    };
  }

  async function callUniversalArenaAI(prompt, systemInstruction) {
    const cfg = arenaRuntime.aiConfig;
    const cleanKey = (cfg.apiKey || "").trim();

    // If user configured a custom BYOK key, use their selected provider & model first
    if (cleanKey) {
      const cleanBase = (cfg.baseUrl || "").replace(/\/+$/, "");
      if (cfg.protocol === "gemini") {
        const modelPath = cfg.model.startsWith("models/") ? cfg.model : `models/${cfg.model}`;
        const url = `${cleanBase}/${modelPath}:generateContent?key=${encodeURIComponent(cleanKey)}`;
        const body = {
          contents: [{ role: "user", parts: [{ text: prompt }] }],
          generationConfig: { temperature: 0.35, maxOutputTokens: 1024 }
        };
        if (systemInstruction) {
          body.systemInstruction = { parts: [{ text: systemInstruction }] };
        }
        const resp = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body)
        });
        if (!resp.ok) throw new Error(`Gemini HTTP ${resp.status}`);
        const data = await resp.json();
        const text = data?.candidates?.[0]?.content?.parts?.map((p) => p.text || "").join("") || "";
        if (text.trim()) return text.trim();
      } else if (cfg.protocol === "anthropic") {
        const url = `${cleanBase}/messages`;
        const body = {
          model: cfg.model || "claude-3-5-sonnet-latest",
          max_tokens: 1024,
          system: systemInstruction || "",
          messages: [{ role: "user", content: prompt }]
        };
        const resp = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-api-key": cleanKey,
            "anthropic-version": "2023-06-01",
            "anthropic-dangerous-direct-browser-access": "true"
          },
          body: JSON.stringify(body)
        });
        if (!resp.ok) throw new Error(`Anthropic HTTP ${resp.status}`);
        const data = await resp.json();
        const text = (data?.content || []).map((c) => c.text || "").join("");
        if (text.trim()) return text.trim();
      } else {
        // OpenAI-compatible (/chat/completions)
        const url = `${cleanBase}/chat/completions`;
        const messages = [];
        if (systemInstruction) messages.push({ role: "system", content: systemInstruction });
        messages.push({ role: "user", content: prompt });
        const resp = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${cleanKey}`
          },
          body: JSON.stringify({
            model: cfg.model || "gpt-4o-mini",
            messages: messages,
            temperature: 0.35,
            max_tokens: 1024
          })
        });
        if (!resp.ok) throw new Error(`Provider HTTP ${resp.status}`);
        const data = await resp.json();
        const text = data?.choices?.[0]?.message?.content || "";
        if (text.trim()) return text.trim();
      }
    }

    // Fallback to built-in Hub Gemini rotator if available
    if (typeof callGeminiAI === "function") {
      return await callGeminiAI(prompt, systemInstruction);
    }
    throw new Error("No active AI provider connection.");
  }

  /* --------------------------------------------------------------------------
     6. INSTANT L1/L2 GRADING, L3 SEMANTIC GRADING & WARDEN ROAST ENGINE
     -------------------------------------------------------------------------- */
  function buildWardenSubmissionComment(acc, inst, isCorrect, slaBreached, antiGrindCapped) {
    if (antiGrindCapped) {
      return {
        tone: "harsh",
        vi: `Cày lặp lại bài ${inst.topic} lần thứ ${acc.mastery[inst.blueprintId].attempts} à? Tôi khóa cộng điểm độ phủ (Breadth) rồi. Làm đúng bài cũ không chứng minh ông lên trình đâu, chuyển sang chủ đề chưa làm hoặc bật Level 3 đi!`,
        en: `Grinding ${inst.topic} for the ${acc.mastery[inst.blueprintId].attempts}th time? Breadth mastery gain is locked. Repeating familiar blueprints proves nothing — switch to an untouched topic or tackle Level 3!`
      };
    }

    if (!isCorrect) {
      const chosenReason = (inst.distractorReasons && inst.distractorReasons[inst.selectedOption]) || "";
      const sec = Math.round((inst.activeAnswerMs || 0) / 1000);
      return {
        tone: "harsh",
        vi: `Sai bét cơ chế gốc ở ${inst.topic} (${inst.levelKey}) sau ${sec}s! ${chosenReason} Mang tư duy này vào phỏng vấn hay vận hành Production là rớt ngay vòng gửi xe. Đọc kỹ phần mổ xẻ bên dưới rồi làm biến thể mới!`,
        en: `Dead wrong on ${inst.topic} (${inst.levelKey}) after ${sec}s! ${chosenReason} Bring that assumption into a production interview and you fail on the spot. Study the mechanical breakdown below and try a fresh mutation.`
      };
    }

    if (slaBreached) {
      const sec = Math.round((inst.activeAnswerMs || 0) / 1000);
      const slaSec = Math.round((inst.slaTargetMs || 45000) / 1000);
      return {
        tone: "harsh",
        vi: `Đáp án thì đúng đấy nhưng ngâm tới ${sec}s (vượt chuẩn SLA ${slaSec}s của ${inst.levelKey})! Đi phỏng vấn thực chiến mà ngập ngừng lâu thế này là người phỏng vấn biết ngay phản xạ chưa vững.`,
        en: `Right answer, but you stalled for ${sec}s (exceeding the ${slaSec}s SLA for ${inst.levelKey})! In a live technical interview, hesitating that long signals shaky muscle memory.`
      };
    }

    if (inst.assisted) {
      return {
        tone: "neutral",
        vi: `Làm đúng nhưng đã phải cầu cứu gợi ý trong Box Chat trước khi nộp (` + "`assisted: true`" + `). Tôi ghi nhận điểm luyện tập nhưng KHÔNG tính là bằng chứng tự lập (Unassisted First-Try) để xét lên cấp!`,
        en: `Correct, but you relied on pre-submit hints in the Chatbox (marked assisted: true). Practice XP granted, but this does NOT count as unassisted first-try evidence for rank promotion.`
      };
    }

    const sec = Math.round((inst.activeAnswerMs || 0) / 1000);
    return {
      tone: "praise",
      vi: `Chuẩn xác trong ${sec}s, không cần trợ giúp. Nắm đúng bất biến kỹ thuật của ${inst.topic}. Đừng tự mãn, đẩy lên cấp độ tiếp theo đi.`,
      en: `Clean unassisted execution in ${sec}s. Core invariant of ${inst.topic} verified. Don't get comfortable — push to the next level.`
    };
  }

  function gradeLevel3Deterministic(inst, openText) {
    const clean = (openText || "").trim().toLowerCase();
    const mcqCorrect = inst.selectedOption === inst.correctIndex;
    const mcqScore = mcqCorrect ? 35 : 0;

    if (clean.length < 25) {
      return {
        totalScore: mcqScore,
        mcqScore: mcqScore,
        openScore: 0,
        matchedConcepts: [],
        missingConcepts: (inst.rubric && inst.rubric.coreConcepts) || [],
        feedbackVi: "Phần tự luận (Phần B) quá ngắn hoặc bỏ trống. Ở cấp độ phỏng vấn thực chiến (L3), bạn bắt buộc phải bảo vệ lập luận và chỉ rõ đánh đổi kỹ thuật (Trade-off).",
        feedbackEn: "Open-ended defense (Part B) is empty or too brief. At Level 3, you must articulate core mechanisms and production trade-offs."
      };
    }

    const rubric = inst.rubric || { coreConcepts: [], tradeoffs: [], referenceAnswer: "" };
    const allPoints = [].concat(rubric.coreConcepts || [], rubric.tradeoffs || []);
    const matched = [];
    const missing = [];

    allPoints.forEach((pt) => {
      // Extract technical tokens from rubric point
      const tokens = (pt.toLowerCase().match(/[a-z0-9_/-]{3,}|[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]{3,}/g) || [])
        .filter((w) => w.length >= 4);
      let hits = 0;
      tokens.forEach((tk) => {
        if (clean.includes(tk)) hits += 1;
      });
      const ratio = tokens.length > 0 ? hits / Math.min(tokens.length, 6) : 0.5;
      if (ratio >= 0.25 || clean.length >= 140) {
        matched.push(pt);
      } else {
        missing.push(pt);
      }
    });

    const conceptCoverage = allPoints.length > 0 ? (matched.length / allPoints.length) : 0.75;
    const lengthBonus = Math.min(1, clean.length / 120);
    const openScore = Math.round(65 * Math.min(1, conceptCoverage * 0.78 + lengthBonus * 0.22));
    const totalScore = Math.min(100, mcqScore + openScore);

    return {
      totalScore: totalScore,
      mcqScore: mcqScore,
      openScore: openScore,
      matchedConcepts: matched,
      missingConcepts: missing,
      feedbackVi: totalScore >= 75
        ? `Chấm điểm Bản chất (Semantic Rubric): Đạt ${totalScore}/100 (Trắc nghiệm Phần A: ${mcqScore}/35 · Bảo vệ Kiến trúc Phần B: ${openScore}/65). Bạn đã nắm được cơ chế cốt lõi và luồng xử lý thực tế.`
        : `Chấm điểm Bản chất (Semantic Rubric): Đạt ${totalScore}/100 (Phần A: ${mcqScore}/35 · Phần B: ${openScore}/65). Lập luận còn thiếu một số chốt chặn quan trọng khi tải cao hoặc sự cố dây chuyền.`,
      feedbackEn: totalScore >= 75
        ? `Semantic Rubric Score: ${totalScore}/100 (Part A MCQ: ${mcqScore}/35 · Part B Defense: ${openScore}/65). Core engineering mechanics and trade-offs verified.`
        : `Semantic Rubric Score: ${totalScore}/100 (Part A: ${mcqScore}/35 · Part B: ${openScore}/65). Your defense missed key failure-mode or trade-off constraints.`
    };
  }

  async function submitArenaAnswer() {
    const acc = getActiveArenaAccount();
    const inst = acc.activeSession;
    if (!inst || inst.submitted) return;

    if (inst.selectedOption === null || inst.selectedOption === undefined) {
      if (typeof showToast === "function") {
        showToast(arenaTr("Hãy chọn 1 phương án trả lời trước khi nộp!", "Please select an option before submitting!"));
      }
      return;
    }

    const levelNum = Number(inst.level);
    let isCorrect = false;
    let scorePct = 0;

    if (levelNum === 1 || levelNum === 2) {
      isCorrect = (inst.selectedOption === inst.correctIndex);
      scorePct = isCorrect ? 100 : 0;
    } else {
      // Level 3 Hybrid: Deterministic instant rubric + optional async AI refinement
      const l3Eval = gradeLevel3Deterministic(inst, inst.l3OpenDraft);
      inst.l3Evaluation = l3Eval;
      scorePct = l3Eval.totalScore;
      isCorrect = (scorePct >= 70 && inst.selectedOption === inst.correctIndex);
    }

    inst.submitted = true;
    inst.isCorrect = isCorrect;
    inst.scorePct = scorePct;

    const m = acc.mastery[inst.blueprintId] || {
      topic: inst.topic,
      l1Best: 0,
      l2Best: 0,
      l3Best: 0,
      l1Unassisted: 0,
      l2Unassisted: 0,
      l3Unassisted: 0,
      attempts: 0,
      slaBreaches: 0,
      seenFingerprints: []
    };

    const prevBestKey = `l${levelNum}Best`;
    const unassistedKey = `l${levelNum}Unassisted`;
    const alreadyClearedThisLevel = Number(m[prevBestKey] || 0) >= 80;
    const antiGrindCapped = alreadyClearedThisLevel && m.attempts >= 3;

    m.attempts = (m.attempts || 0) + 1;
    if (!m.seenFingerprints.includes(inst.fingerprint)) {
      m.seenFingerprints.push(inst.fingerprint);
    }

    const slaBreached = (inst.activeAnswerMs || 0) > (inst.slaTargetMs || 45000);
    if (slaBreached) {
      m.slaBreaches = (m.slaBreaches || 0) + 1;
      acc.wardenState.slaBreachCount = (acc.wardenState.slaBreachCount || 0) + 1;
    }
    if (antiGrindCapped) {
      acc.wardenState.antiGrindFlags = (acc.wardenState.antiGrindFlags || 0) + 1;
    }

    if (scorePct > Number(m[prevBestKey] || 0)) {
      m[prevBestKey] = scorePct;
    }
    if (isCorrect && !inst.assisted && !slaBreached) {
      m[unassistedKey] = (m[unassistedKey] || 0) + 1;
    }
    acc.mastery[inst.blueprintId] = m;

    // Calculate XP (capped if grinding repeated blueprint)
    const cat = getArenaCatalog();
    const lvlMeta = (cat.levels || []).find((l) => l.level === levelNum) || { baseXp: 50 };
    const rankMeta = (cat.ranks || []).find((r) => r.tier === acc.verifiedRankTier) || { xpMultiplier: 1.0 };
    let xpEarned = 0;
    if (isCorrect) {
      const rawXp = Math.round((lvlMeta.baseXp || 50) * (rankMeta.xpMultiplier || 1.0) * (scorePct / 100));
      xpEarned = antiGrindCapped ? Math.max(5, Math.round(rawXp * 0.15)) : rawXp;
      acc.totalXp = (acc.totalXp || 0) + xpEarned;
    }

    const prevTier = acc.verifiedRankTier;
    recomputeAccountAdjudication(acc);
    const promoted = acc.verifiedRankTier > prevTier;

    const wComment = buildWardenSubmissionComment(acc, inst, isCorrect, slaBreached, antiGrindCapped);
    if (promoted) {
      const newRankObj = (cat.ranks || []).find((r) => r.tier === acc.verifiedRankTier);
      const rName = newRankObj ? (isArenaEn() ? newRankObj.enTitle : newRankObj.title) : acc.verifiedRankId;
      acc.wardenState.tone = "praise";
      acc.wardenState.lastCommentVi = `THĂNG CẤP THỰC CHIẾN! Bạn đã vượt qua trọn vẹn ma trận Độ rộng × Độ sâu × L3 Tự lập. Quản Giáo chính thức công nhận bạn đạt cấp: ${newRankObj ? newRankObj.badgeCode : ""} (${rName}). Toàn bộ 3 level câu hỏi từ giờ sẽ tự động nâng độ khó lên tầm ${rName}!`;
      acc.wardenState.lastCommentEn = `RANK PROMOTION VERIFIED! You satisfied the full Breadth × Depth × Unassisted L3 matrix. The Warden officially certifies you at ${newRankObj ? newRankObj.badgeCode : ""} (${rName}). All 3 question levels now shift to ${rName} complexity!`;
    } else {
      acc.wardenState.tone = wComment.tone;
      acc.wardenState.lastCommentVi = wComment.vi;
      acc.wardenState.lastCommentEn = wComment.en;
    }

    acc.attemptHistory.push({
      id: "att_" + Date.now(),
      topic: inst.topic,
      blueprintId: inst.blueprintId,
      level: levelNum,
      rankTier: inst.rankTier,
      isCorrect: isCorrect,
      scorePct: scorePct,
      xpAwarded: xpEarned,
      activeAnswerMs: inst.activeAnswerMs || 0,
      slaTargetMs: inst.slaTargetMs || 45000,
      slaBreached: slaBreached,
      assisted: !!inst.assisted,
      antiGrindCapped: antiGrindCapped,
      ts: Date.now()
    });

    // Update long-term user progress & AI memory ledger
    const pm = ensureAccountProfileMemory(acc);
    pm.totalStudyTimeMs = Number(pm.totalStudyTimeMs || 0) + Number(inst.activeAnswerMs || 1000);
    pm.totalQuestionsSolved = Number(pm.totalQuestionsSolved || 0) + 1;
    if (isCorrect) {
      pm.totalCorrectAnswers = Number(pm.totalCorrectAnswers || 0) + 1;
    } else {
      const patternEntry = `${inst.topic}:${inst.levelKey} (${inst.stationTitle || inst.blueprintId})`;
      if (!pm.mistakePatterns.includes(patternEntry)) {
        pm.mistakePatterns.push(patternEntry);
        if (pm.mistakePatterns.length > 12) pm.mistakePatterns.shift();
      }
    }

    saveArenaPersistence();
    renderArenaView();

    // Non-blocking background cloud DB sync if configured
    if (pm.syncMode === "github_gist" && pm.githubToken) {
      syncAccountWithGitHubGist("push").catch(() => {});
    }
    if (arenaRuntime.supabaseConfig.url && arenaRuntime.supabaseConfig.anonKey) {
      syncAccountWithSupabase("push").catch(() => {});
    }
  }

  /* --------------------------------------------------------------------------
     7. CONTEXTUAL IN-ARENA STUDY CHATBOX (2-PHASE ANTI-SPOILER ENGINE)
     -------------------------------------------------------------------------- */
  function isSpoilerQuestionRequest(userMsg) {
    const lower = (userMsg || "").toLowerCase();
    const patterns = [
      "đáp án đúng",
      "chọn câu nào",
      "chọn đáp án nào",
      "câu nào đúng",
      "phương án nào đúng",
      "a, b, c hay d",
      "a hay b",
      "give me the answer",
      "which option is correct",
      "what is the correct answer",
      "tell me the answer",
      "chỉ đáp án"
    ];
    return patterns.some((p) => lower.includes(p));
  }

  async function sendArenaContextualChat(rawText) {
    const acc = getActiveArenaAccount();
    const inst = acc.activeSession;
    if (!inst) return;
    const text = (rawText || "").trim();
    if (!text) return;

    const pm = ensureAccountProfileMemory(acc);
    pm.totalChatQuestionsAsked = Number(pm.totalChatQuestionsAsked || 0) + 1;
    pm.recentChatQueries.push(`${inst.topic}(${inst.levelKey}): ${text.slice(0, 90)}`);
    if (pm.recentChatQueries.length > 10) pm.recentChatQueries.shift();

    const thread = acc.chatThreads[inst.instanceId] || [];
    const phase = inst.submitted ? "post_submit" : "pre_submit";

    thread.push({
      role: "user",
      content: text,
      phase: phase,
      ts: Date.now(),
      spoilerBlocked: false
    });

    // Pre-submit anti-spoiler enforcement
    if (!inst.submitted) {
      inst.assisted = true; // Asking for help before submitting marks the attempt as assisted!
      if (isSpoilerQuestionRequest(text)) {
        const blockMsgVi = `[CHỐT CHẶN CHỐNG LỘ ĐÁP ÁN · PRE-SUBMIT] Bạn chưa nộp bài nên Box Chat tuyệt đối không chỉ thẳng đáp án A/B/C/D (và Quản Giáo đã ghi nhận lượt làm này có trợ giúp 'assisted: true').\n\nGợi ý Tư duy Nguyên lý gốc (Socratic Hint): Hãy bám sát bất biến của trạm "${inst.stationTitle}": ${inst.invariant}`;
        const blockMsgEn = `[PRE-SUBMIT ANTI-SPOILER GUARD] You haven't submitted yet, so the Chatbox will not reveal the correct option A/B/C/D (and The Warden has flagged this attempt as 'assisted: true').\n\nSocratic First-Principles Hint: Focus on the core invariant of "${inst.stationTitle}": ${inst.invariant}`;
        thread.push({
          role: "warden",
          content: arenaTr(blockMsgVi, blockMsgEn),
          phase: phase,
          ts: Date.now(),
          spoilerBlocked: true
        });
        acc.wardenState.tone = "harsh";
        acc.wardenState.lastCommentVi = `Chưa tự suy nghĩ xong câu ${inst.topic} (${inst.levelKey}) mà đã gõ vào Box Chat xin đáp án đúng à? Tôi đã chặn lộ đáp án và đánh dấu 'assisted: true' — câu này làm đúng cũng không được tính vào chuẩn tự lập lên cấp!`;
        acc.wardenState.lastCommentEn = `Asking the Chatbox for the answer on ${inst.topic} (${inst.levelKey}) before submitting? Spoiler blocked and attempt marked 'assisted: true' — this won't count toward unassisted promotion!`;
        acc.chatThreads[inst.instanceId] = thread;
        saveArenaPersistence();
        renderArenaView();
        return;
      }
    }

    acc.chatThreads[inst.instanceId] = thread;
    saveArenaPersistence();
    renderArenaView();

    // Build 2-phase projection prompt (Pre-submit NEVER includes correctIndex or referenceAnswer)
    const digest = readHotCognitiveDigest();
    const profilePacket = JSON.stringify(buildUnifiedProfileContextPacket(false), null, 2);
    let replyText = "";
    try {
      const sysPrompt = !inst.submitted
        ? "Bạn là Trợ giảng Kỹ thuật Socratic nằm trong khu vực làm bài Arena. Người học CHƯA nộp bài. TUYỆT ĐỐI KHÔNG tiết lộ phương án A/B/C/D nào là đúng hoặc loại trừ trực tiếp đáp án. Chỉ gợi mở nguyên lý cơ học cốt lõi ngắn gọn trong 3-5 câu dựa trên trình độ hồ sơ người học."
        : "Bạn là Kiến trúc sư Trưởng hỗ trợ mổ xẻ câu hỏi sau khi người học ĐÃ nộp bài. Hãy giải thích trực diện, sắc bén cơ chế gốc, tại sao đáp án đúng hoạt động và tại sao các phương án nhiễu lại sai phù hợp với cấp bậc hồ sơ người học.";

      const projection = !inst.submitted
        ? `Ngữ cảnh Hồ sơ Đăng nhập:\n${profilePacket}\n\nNgữ cảnh câu hỏi đang làm (Pre-Submit — Đã ẩn đáp án):\n- Chuyên đề: ${inst.topic} (${inst.stationTitle})\n- Cấp độ: ${inst.levelKey} · Rank: ${inst.rankBadge}\n- Câu hỏi: ${inst.stem}\n- Nguyên lý nền: ${inst.invariant}\n- Câu hỏi của người học: ${text}`
        : `Ngữ cảnh Hồ sơ Đăng nhập:\n${profilePacket}\n\nNgữ cảnh câu hỏi đã nộp (Post-Submit — Mở khóa toàn bộ):\n- Chuyên đề: ${inst.topic} (${inst.stationTitle})\n- Câu hỏi: ${inst.stem}\n- Phương án đúng: ${inst.options[inst.correctIndex]}\n- Giải thích chuẩn: ${inst.explanation}\n- Hồ sơ người học: Rank Tier ${digest.verifiedRankTier}, Role ${digest.roleTrack}\n- Câu hỏi của người học: ${text}`;

      replyText = await callUniversalArenaAI(projection, sysPrompt);
    } catch (err) {
      // Deterministic contextual response when offline or no API key
      if (!inst.submitted) {
        replyText = arenaTr(
          `[Gợi ý Socratic · Pre-Submit (${inst.topic} · ${inst.levelKey} · Hồ sơ ${acc.displayName} T${acc.verifiedRankTier})]: Vì bạn đang trong quá trình làm bài (đã ghi nhận trạng thái có trợ giúp 'assisted: true'), hãy đối chiếu câu hỏi của bạn với nguyên lý bất biến của trạm "${inst.stationTitle}":\n\n"${inst.invariant}"\n\nHãy tự hỏi: trong 4 phương án trên, phương án nào bảo toàn được cơ chế vật lý/hệ thống này khi tải tăng đột biến mà không sinh tác dụng phụ? Chọn xong và bấm Nộp bài để xem giải phẫu từng phương án!`,
          `[Socratic Hint · Pre-Submit (${inst.topic} · ${inst.levelKey} · Profile ${acc.displayName} T${acc.verifiedRankTier})]: Since you have not submitted yet (attempt marked 'assisted: true'), anchor your reasoning on the core invariant of "${inst.stationTitle}":\n\n"${inst.invariant}"\n\nAsk yourself which option preserves this mechanical guarantee under production load, then submit to unlock the full distractor breakdown.`
        );
      } else {
        replyText = arenaTr(
          `[Giải phẫu Chuyên sâu · Post-Submit (${inst.topic} · ${inst.levelKey} · Hồ sơ ${acc.displayName} T${acc.verifiedRankTier})]:\n- Đáp án chuẩn: "${inst.options[inst.correctIndex]}"\n- Cơ chế gốc: ${inst.explanation}\n- Liên hệ câu hỏi của bạn: ${inst.invariant}`,
          `[Post-Submit Deep Breakdown (${inst.topic} · ${inst.levelKey} · Profile ${acc.displayName} T${acc.verifiedRankTier})]:\n- Verified Option: "${inst.options[inst.correctIndex]}"\n- Core Mechanism: ${inst.explanation}\n- Invariant Link: ${inst.invariant}`
        );
      }
    }

    thread.push({
      role: "assistant",
      content: replyText,
      phase: phase,
      ts: Date.now(),
      spoilerBlocked: false
    });
    acc.chatThreads[inst.instanceId] = thread;
    saveArenaPersistence();
    renderArenaView();
  }

  /* --------------------------------------------------------------------------
     8. ACTIVE DWELL-TIME SLA TRACKER
     -------------------------------------------------------------------------- */
  function startArenaDwellTimer() {
    if (arenaRuntime.dwellTimerId) clearInterval(arenaRuntime.dwellTimerId);
    arenaRuntime.lastTickTs = Date.now();
    arenaRuntime.dwellTimerId = setInterval(() => {
      if (typeof activeTopic === "undefined" || activeTopic !== "PRACTICE") return;
      if (typeof document !== "undefined" && document.hidden) {
        arenaRuntime.lastTickTs = Date.now();
        return;
      }
      const acc = getActiveArenaAccount();
      const inst = acc && acc.activeSession;
      if (!inst || inst.submitted) {
        arenaRuntime.lastTickTs = Date.now();
        return;
      }
      const now = Date.now();
      const delta = Math.min(2000, Math.max(0, now - arenaRuntime.lastTickTs));
      arenaRuntime.lastTickTs = now;
      inst.activeAnswerMs = (inst.activeAnswerMs || 0) + delta;

      // Update timer badge in DOM without full re-render
      const badgeEl = document.getElementById("arenaSlaTimerPill");
      if (badgeEl) {
        const sec = Math.floor(inst.activeAnswerMs / 1000);
        const slaSec = Math.floor((inst.slaTargetMs || 45000) / 1000);
        badgeEl.textContent = `SLA: ${sec}s / ${slaSec}s`;
        if (inst.activeAnswerMs > inst.slaTargetMs) {
          badgeEl.classList.add("sla-warn");
          if (!inst.slaWarned) {
            inst.slaWarned = true;
            acc.wardenState.tone = "harsh";
            acc.wardenState.lastCommentVi = `Đang ngâm câu ${inst.topic} (${inst.levelKey}) quá ${slaSec}s SLA rồi đấy! Đang lúng túng cơ chế gốc hay vừa mở tab khác tra cứu?`;
            acc.wardenState.lastCommentEn = `You just breached the ${slaSec}s SLA on ${inst.topic} (${inst.levelKey})! Hesitating on core mechanics or tab-switching to search?`;
            const quoteEl = document.getElementById("arenaWardenLiveQuote");
            if (quoteEl) {
              quoteEl.textContent = isArenaEn() ? acc.wardenState.lastCommentEn : acc.wardenState.lastCommentVi;
            }
          }
        }
      }
    }, 1000);
  }

  /* --------------------------------------------------------------------------
     9. RENDER ARENA VIEW (#/practice) & MODALS
     -------------------------------------------------------------------------- */
  function openPracticeView(topicFilter = null, pushHistory = true) {
    initArenaPersistence();
    const acc = getActiveArenaAccount();
    if (topicFilter && topicFilter !== "PRACTICE" && topicFilter !== "CATALOG" && topicFilter !== "GLOSSARY") {
      acc.selectedTopic = topicFilter;
      generatePolymorphicInstance(acc, false);
    } else if (!acc.activeSession) {
      generatePolymorphicInstance(acc, false);
    }

    if (typeof syncStateVars === "function") {
      syncStateVars("PRACTICE", 1, null);
    }
    document.body.classList.add("catalog-mode");
    document.body.classList.remove("mobile-rail-open");
    if (typeof renderSyllabus === "function") renderSyllabus();
    if (typeof renderMain === "function") {
      renderMain(false);
    } else {
      renderArenaView();
      startArenaDwellTimer();
    }
    if (pushHistory && (typeof isHandlingRouteEvent === "undefined" || !isHandlingRouteEvent)) {
      if (window.location.hash !== "#/practice") {
        history.pushState({ topic: "PRACTICE", stage: 1, section: null }, "", "#/practice");
      }
    }
  }

  function renderArenaLoginGateHtml() {
    const allAccs = Object.values(arenaRuntime.accounts);
    const customAccs = allAccs.filter((a) => a.presetType === "github_user" || a.presetType === "custom");
    const presetAccs = allAccs.filter((a) => a.presetType !== "github_user" && a.presetType !== "custom");

    const customListHtml = customAccs.length > 0 ? `
      <div style="margin-top:16px;padding-top:16px;border-top:1px solid var(--cds-border-subtle);display:flex;flex-direction:column;gap:8px;">
        <span style="font-family:var(--cds-font-mono);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;color:var(--cds-text-muted);">
          ${arenaTr("Hồ Sơ Cá Nhân Đã Lưu Trên Máy Này (" + customAccs.length + ")", "Saved Personal Profiles on This Browser (" + customAccs.length + ")")}
        </span>
        <div class="arena-persona-list">
          ${customAccs.map((a) => {
            recomputeAccountAdjudication(a);
            const pm = ensureAccountProfileMemory(a);
            return `
              <button type="button" class="stage-pill-btn" data-gate-quick-login="${escapeHtml(a.accountId)}">
                <span class="stage-pill-num">T${a.verifiedRankTier}</span>
                <span>
                  <strong style="display:block;font-size:13.5px;color:var(--cds-text-primary);">
                    ${escapeHtml(a.displayName)} (@${escapeHtml(a.githubHandle)})
                    ${pm.githubVerified ? " ✓" : ""}
                  </strong>
                  <span style="font-size:12px;color:var(--cds-text-secondary);">
                    ${escapeHtml(a.roleTrack)} · ${a.totalXp} XP · ${pm.totalQuestionsSolved || 0} ${arenaTr("câu đã giải", "solved")}
                  </span>
                </span>
              </button>
            `;
          }).join("")}
        </div>
      </div>
    ` : "";

    const presetListHtml = presetAccs.map((a) => {
      recomputeAccountAdjudication(a);
      const pm = ensureAccountProfileMemory(a);
      return `
        <button type="button" class="stage-pill-btn" data-gate-quick-login="${escapeHtml(a.accountId)}">
          <span class="stage-pill-num">T${a.verifiedRankTier}</span>
          <span>
            <strong style="display:block;font-size:13.5px;color:var(--cds-text-primary);">${escapeHtml(a.displayName)}</strong>
            <span style="font-size:12px;color:var(--cds-text-secondary);">
              @${escapeHtml(a.githubHandle)} · ${escapeHtml(a.roleTrack)} · ${a.totalXp} XP · ${a.computedMetrics ? a.computedMetrics.topicsMasteredCount : 0}/12 topics · SLA: ${a.wardenState.slaBreachCount}
            </span>
          </span>
        </button>
      `;
    }).join("");

    const sealArt = typeof renderBadgeSealHtml === "function"
      ? renderBadgeSealHtml("ObjectShield", "IDENTITY & MASTERY GATE")
      : "";

    return `
      <div class="arena-shell" id="arenaLoginGate">
        <header class="catalog-hero swatch-peach" id="arena-login-hero">
          <div class="lesson-hero-dots" aria-hidden="true"></div>
          <div class="lesson-header-grid has-artwork">
            <div class="lesson-header-copy">
              <div class="lesson-meta">
                <span class="cds-swatch-pill">ANTHROPIC ACADEMY · PRACTICE ARENA</span>
                <span class="cds-swatch-pill">${arenaTr("CỔNG ĐỊNH DANH & ĐỒNG BỘ HỒ SƠ", "AUTHENTICATION & PROFILE GATE")}</span>
                <span class="cds-swatch-pill">MULTI-USER DB READY</span>
              </div>
              <h1 class="lesson-title">${arenaTr("Đăng Nhập Hồ Sơ Kỹ Sư Để Vào Đấu Trường Sát Hạch", "Sign In to Enter the Engineering Mastery Arena")}</h1>
              <p class="lesson-lead">
                ${arenaTr(
                  "Mỗi kỹ sư có bộ nhớ tiến độ, lịch sử lỗi sai, điểm độ phủ × độ sâu và phán quyết Quản Giáo AI hoàn toàn độc lập. Đăng nhập bằng GitHub cá nhân để lưu trữ lâu dài hoặc chọn nhanh 1 trong 5 hồ sơ giả lập để kiểm thử.",
                  "Every engineer has an isolated AI profile memory ledger, Breadth × Depth mastery matrix, and AI Warden adjudication history. Sign in with GitHub or pick a pre-seeded persona below."
                )}
              </p>
              <div class="arena-hero-actions-bar">
                <button type="button" class="arena-btn" id="arenaOpenProviderModalBtn">
                  ${arenaTr("Cấu Hình AI / BYOK API", "Configure AI Provider / BYOK")}
                </button>
                <button type="button" class="arena-btn" id="arenaOpenAccountsModalBtn">
                  ${arenaTr("Quản Lý Database & Đồng Bộ Cloud", "Manage Multi-User Cloud DB")}
                </button>
              </div>
            </div>
            <div class="lesson-hero-art">${sealArt}</div>
          </div>
        </header>

        <section class="arena-gate-grid" id="arena-gate-cards">
          <!-- Column 1: Real GitHub / Custom Profile Login -->
          <div class="arena-gate-card">
            <span class="arena-gate-eyebrow">${arenaTr("ĐỊNH DANH CÁ NHÂN & ĐỒNG BỘ ĐÁM MÂY", "PERSONAL IDENTITY & CLOUD SYNC")}</span>
            <h2 class="arena-gate-title">${arenaTr("Đăng Nhập Bằng Tài Khoản GitHub", "Sign In with GitHub Identity")}</h2>
            <p class="arena-gate-desc">
              ${arenaTr(
                "Hệ thống tự động đối chiếu hồ sơ qua api.github.com, khởi tạo sổ cái bộ nhớ AI riêng cho bạn và duy trì phiên đăng nhập kể cả khi tải lại trang (F5).",
                "Automatically verifies your handle via api.github.com, initializes your dedicated AI profile memory ledger, and persists your session across F5 reloads."
              )}
            </p>

            <form id="arenaGateLoginForm" style="display:flex;flex-direction:column;gap:12px;margin-top:4px;">
              <div class="arena-control-col">
                <label class="arena-control-label" for="arenaGateGithubInput">${arenaTr("GitHub Username (*)", "GitHub Username (*)")}</label>
                <input type="text" class="arena-input" id="arenaGateGithubInput" placeholder="VD: torvalds, karpathy, ten-cua-ban..." required autocomplete="username" />
              </div>

              <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                <div class="arena-control-col">
                  <label class="arena-control-label" for="arenaGateNameInput">${arenaTr("Tên hiển thị", "Display Name")}</label>
                  <input type="text" class="arena-input" id="arenaGateNameInput" placeholder="${arenaTr("Tự động lấy từ GitHub nếu để trống", "Auto-filled from GitHub if blank")}" />
                </div>
                <div class="arena-control-col">
                  <label class="arena-control-label" for="arenaGateRoleSelect">${arenaTr("Vị trí mục tiêu (JD Track)", "Target JD Role Track")}</label>
                  <select class="arena-select" id="arenaGateRoleSelect">
                    <option value="DE">Data Engineer (DE)</option>
                    <option value="AIE">AI Engineer (AIE)</option>
                    <option value="MLE">ML Engineer (MLE)</option>
                  </select>
                </div>
              </div>

              <div class="arena-control-col">
                <label class="arena-control-label" for="arenaGateTokenInput">${arenaTr("GitHub Personal Access Token (Tùy chọn · Quyền 'gist' để đồng bộ Cloud)", "Optional: GitHub Token ('gist' scope for Cloud DB Sync)")}</label>
                <input type="password" class="arena-input" id="arenaGateTokenInput" placeholder="ghp_... (Để trống nếu chỉ lưu trên trình duyệt & IndexedDB)" autocomplete="current-password" />
              </div>

              <div style="display:flex;justify-content:flex-end;margin-top:6px;">
                <button type="submit" class="arena-btn arena-btn-primary" id="arenaGateLoginBtn" style="width:100%;justify-content:center;padding:12px 18px;font-size:14px;">
                  ${arenaTr("Xác Thực GitHub & Vào Đấu Trường →", "Verify GitHub & Enter Practice Arena →")}
                </button>
              </div>
            </form>

            ${customListHtml}
          </div>

          <!-- Column 2: 5 Pre-seeded Sandbox Personas -->
          <div class="arena-gate-card">
            <span class="arena-gate-eyebrow">${arenaTr("CHẾ ĐỘ THỬ NGHIỆM NHANH · 5 HỒ SƠ MẪU", "INSTANT SANDBOX · 5 PRE-SEEDED PERSONAS")}</span>
            <h2 class="arena-gate-title">${arenaTr("Chọn Hồ Sơ Giả Lập Để Vào Ngay", "One-Click Sandbox Persona Login")}</h2>
            <p class="arena-gate-desc">
              ${arenaTr(
                "Dành cho việc kiểm thử nhanh các kịch bản của Quản Giáo AI: từ Sinh viên mới tinh (T1), Người cày lặp 1 bài F01 bị khóa cấp, Người ngâm câu hỏi lố SLA, cho tới Kỹ sư Senior+ (T7).",
                "Test how The AI Warden and Polymorphic Question Engine adapt across 5 realistic engineering personas with pre-populated telemetry."
              )}
            </p>

            <div class="arena-persona-list" id="arenaGatePersonaList">
              ${presetListHtml}
            </div>
          </div>
        </section>
      </div>
    `;
  }

  function renderArenaView() {
    initArenaPersistence();
    const container = document.getElementById("articleContainer");
    if (!container) return;

    if (!arenaRuntime.isLoggedIn) {
      const tocList = document.getElementById("tocList");
      if (tocList) {
        tocList.innerHTML = `
          <li><a class="toc-link active" href="#arena-login-hero">${arenaTr("Cổng Đăng Nhập Đấu Trường", "Arena Sign-In Gate")}</a></li>
          <li><a class="toc-link" href="#arena-gate-cards">${arenaTr("Chọn Hồ Sơ Kỹ Sư", "Select Engineering Profile")}</a></li>
        `;
      }
      container.innerHTML = renderArenaLoginGateHtml() + renderArenaActiveModalHtml();
      bindArenaDomEvents();
      return;
    }

    const cat = getArenaCatalog();
    const acc = getActiveArenaAccount();
    const pm = ensureAccountProfileMemory(acc);
    const digest = readHotCognitiveDigest();
    if (!acc.activeSession || acc.activeSession.topic !== acc.selectedTopic || acc.activeSession.level !== Number(acc.selectedLevel)) {
      generatePolymorphicInstance(acc, false);
    }
    const inst = acc.activeSession;
    const ranks = cat.ranks || [];
    const levels = cat.levels || [];
    const currentRank = ranks.find((r) => r.tier === acc.verifiedRankTier) || ranks[0] || {
      tier: 1, title: "Sinh viên", enTitle: "Student", badgeCode: "T1 · STUDENT", summary: ""
    };

    const tocList = document.getElementById("tocList");
    if (tocList) {
      tocList.innerHTML = `
        <li><a class="toc-link active" href="#arena-hero">${arenaTr("Hồ Sơ & Cấp Bậc", "Profile & Career Rank")}</a></li>
        <li><a class="toc-link" href="#arena-warden-bar">${arenaTr("Quản Giáo AI Giám Sát", "AI Warden Telemetry")}</a></li>
        <li><a class="toc-link" href="#arena-workspace">${arenaTr("Trạm Sát Hạch Biến Thể", "Polymorphic Question Lab")}</a></li>
        <li><a class="toc-link" href="#arena-chat-panel">${arenaTr("Box Chat Nội Khu", "In-Arena Study Chat")}</a></li>
      `;
    }

    const bps = getAllArenaBlueprints();
    const topicOptionsHtml = bps.map((bp) => {
      const m = acc.mastery[bp.id];
      const depth = m ? Math.round((m.l1Best * 0.2) + (m.l2Best * 0.35) + (m.l3Best * 0.45)) : 0;
      const mark = depth >= 80 ? `[Đạt ${depth}%]` : (depth > 0 ? `[${depth}%]` : "[Mới]");
      return `<option value="${escapeHtml(bp.topic)}" ${bp.topic === acc.selectedTopic ? "selected" : ""}>${escapeHtml(bp.stationTitle)} ${mark}</option>`;
    }).join("");

    const rankLadderHtml = ranks.map((r) => {
      const cls = r.tier === acc.verifiedRankTier ? "current" : (r.tier < acc.verifiedRankTier ? "cleared" : "");
      const rTitle = isArenaEn() ? r.enTitle : r.title;
      return `
        <div class="arena-rank-step ${cls}" data-rank-tier="${r.tier}">
          <span class="arena-rank-step-code">${escapeHtml(r.badgeCode)}</span>
          <span class="arena-rank-step-name">${escapeHtml(rTitle)}</span>
          <span class="arena-rank-step-sub">${r.minTopicsMastered} ${arenaTr("bài", "topics")} · L3≥${r.minL3Passed}</span>
        </div>
      `;
    }).join("");

    const levelTabsHtml = levels.map((lvl) => {
      const activeCls = Number(acc.selectedLevel) === lvl.level ? "active" : "";
      const m = acc.mastery[inst.blueprintId] || {};
      const bestVal = m[`l${lvl.level}Best`] || 0;
      return `
        <button type="button" class="glossary-filter-pill ${activeCls}" data-arena-level="${lvl.level}">
          <span>${escapeHtml(isArenaEn() ? lvl.enTitle : lvl.title)} (${escapeHtml(lvl.formatBadge)})</span>
          <span class="glossary-filter-count">${bestVal}%</span>
        </button>
      `;
    }).join("");

    const rolePillsHtml = [
      { id: "DE", label: "Data Engineer (DE)" },
      { id: "AIE", label: "AI Engineer (AIE)" },
      { id: "MLE", label: "ML Engineer (MLE)" }
    ].map((r) => `
      <button type="button" class="glossary-filter-pill ${acc.roleTrack === r.id ? "active" : ""}" data-arena-role-pill="${r.id}">
        <span>${r.label}</span>
      </button>
    `).join("");

    const letters = ["A", "B", "C", "D"];
    const optionsHtml = (inst.options || []).map((optText, idx) => {
      let stateCls = "";
      if (inst.submitted) {
        if (idx === inst.correctIndex) stateCls = "correct";
        else if (idx === inst.selectedOption) stateCls = "wrong";
      } else if (idx === inst.selectedOption) {
        stateCls = "selected";
      }
      const disabledAttr = inst.submitted && inst.level !== 3 ? "disabled" : "";
      return `
        <button type="button" class="arena-option-btn ${stateCls}" data-arena-opt="${idx}" ${disabledAttr}>
          <span class="arena-opt-letter">${letters[idx] || idx + 1}</span>
          <span>${escapeHtml(optText)}</span>
        </button>
      `;
    }).join("");

    const secElapsed = Math.floor((inst.activeAnswerMs || 0) / 1000);
    const secSla = Math.floor((inst.slaTargetMs || 45000) / 1000);
    const slaWarnCls = (inst.activeAnswerMs || 0) > (inst.slaTargetMs || 45000) ? "sla-warn" : "";

    const thread = acc.chatThreads[inst.instanceId] || [];
    const chatMessagesHtml = thread.length === 0
      ? `<div class="arena-chat-bubble assistant">
           ${arenaTr(
             `<strong>Box Chat Nội Khu (${inst.topic} · ${inst.levelKey})</strong>: Tôi nắm toàn bộ ngữ cảnh của biến thể câu hỏi này và hồ sơ năng lực của bạn (@${escapeHtml(acc.githubHandle)}). Khi bạn <em>chưa nộp bài</em>, tôi chỉ gợi ý tư duy nguyên lý gốc (chống lộ đáp án A/B/C/D). Sau khi <em>nộp bài</em>, bạn có thể hỏi mổ xẻ sâu bất kỳ phương án nào!`,
             `<strong>In-Arena Contextual Chat (${inst.topic} · ${inst.levelKey})</strong>: I hold the full context of this polymorphic question and your profile (@${escapeHtml(acc.githubHandle)}). <em>Before submission</em>, I provide Socratic first-principles hints only (spoiler-locked). <em>After submission</em>, ask anything for a deep breakdown!`
           )}
         </div>`
      : thread.map((msg) => `
          <div class="arena-chat-bubble ${escapeHtml(msg.role)}">
            <div style="font-size:11px;font-weight:600;margin-bottom:4px;opacity:0.78;">
              ${msg.role === "user" ? escapeHtml(acc.displayName) : (msg.role === "warden" ? arenaTr("Quản Giáo AI · Chốt Chặn", "AI Warden · Anti-Spoiler") : "Arena Contextual AI")}
              · ${msg.phase === "pre_submit" ? "Pre-Submit" : "Post-Submit"}
            </div>
            <div style="white-space:pre-wrap;">${escapeHtml(msg.content)}</div>
          </div>
        `).join("");

    let feedbackHtml = "";
    if (inst.submitted) {
      const distractorItems = (inst.options || []).map((opt, i) => {
        const reason = (inst.distractorReasons && inst.distractorReasons[i]) || "";
        const prefix = i === inst.correctIndex ? "[ĐÚNG]" : "[BẪY NHIỄU]";
        return `<li class="arena-distractor-item"><strong>${letters[i]}. ${prefix}:</strong> ${escapeHtml(reason || opt)}</li>`;
      }).join("");

      const l3EvalBlock = (inst.level === 3 && inst.l3Evaluation)
        ? `<div style="padding:12px;border-radius:8px;background:var(--cds-surface-1);border:1px solid var(--cds-border-subtle);margin-top:6px;">
             <div style="font-weight:600;margin-bottom:6px;">${escapeHtml(isArenaEn() ? inst.l3Evaluation.feedbackEn : inst.l3Evaluation.feedbackVi)}</div>
             <div style="font-size:12.5px;color:var(--cds-text-secondary);white-space:pre-wrap;"><strong>${arenaTr("Đáp án tham chiếu chuẩn Kiến trúc sư:", "Reference Principal Answer:")}</strong>\n${escapeHtml((inst.rubric && inst.rubric.referenceAnswer) || "")}</div>
           </div>`
        : "";

      feedbackHtml = `
        <div class="arena-feedback-panel ${inst.isCorrect ? "pass" : "fail"}" id="arenaFeedbackPanel">
          <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px;">
            <strong style="font-size:15px;">
              ${inst.isCorrect
                ? arenaTr(`Chính xác (${inst.scorePct}%) — Đã xác minh cơ chế gốc!`, `Verified (${inst.scorePct}%) — Core mechanics proven!`)
                : arenaTr(`Chưa đạt (${inst.scorePct}%) — Sập bẫy kỹ thuật!`, `Failed (${inst.scorePct}%) — Hit a technical trap!`)}
            </strong>
            <div style="display:flex;gap:8px;">
              <button type="button" class="arena-btn" id="arenaJumpStationBtn" data-topic="${escapeHtml(inst.topic)}" data-stage="${inst.stage || 1}">
                ${arenaTr("Mở bài học gốc", "Open Lesson Station")}
              </button>
              <button type="button" class="arena-btn arena-btn-primary" id="arenaNextMutatedBtn">
                ${arenaTr("Làm biến thể mới (Không lặp lại)", "Next Fresh Variant (Zero Repeat)")}
              </button>
            </div>
          </div>
          <p style="margin:0;font-size:13.5px;line-height:1.58;color:var(--cds-text-primary);">${escapeHtml(inst.explanation)}</p>
          ${l3EvalBlock}
          <ul class="arena-distractor-list">${distractorItems}</ul>
        </div>
      `;
    }

    const heroSealArt = typeof renderBadgeSealHtml === "function"
      ? renderBadgeSealHtml("ObjectShield", `${currentRank.badgeCode} · ${acc.roleTrack}`)
      : "";

    container.innerHTML = `
      <div class="arena-shell" id="arenaRoot">
        <!-- 1. ANTHROPIC ACADEMY HERO BANNER -->
        <header class="catalog-hero swatch-heather" id="arena-hero">
          <div class="lesson-hero-dots" aria-hidden="true"></div>
          <div class="lesson-header-grid has-artwork">
            <div class="lesson-header-copy">
              <div class="lesson-meta">
                <span class="cds-swatch-pill">PRACTICE ARENA · ${escapeHtml(currentRank.badgeCode)}</span>
                <span class="cds-swatch-pill">${escapeHtml(acc.displayName)} (@${escapeHtml(acc.githubHandle)})${pm.githubVerified ? " ✓" : ""}</span>
                <span class="cds-swatch-pill">TRACK: ${escapeHtml(acc.roleTrack)}</span>
                <span class="cds-swatch-pill">DB: ${arenaRuntime.hotDigestPerfMs}ms</span>
              </div>
              <h1 class="lesson-title">${arenaTr("Đấu Trường Luyện Tập Thích Ứng & Sát Hạch Cấp Bậc Kỹ Sư", "AI Adaptive Practice & Engineering Career Arena")}</h1>
              <p class="lesson-lead">
                ${arenaTr(
                  "Mỗi lần làm mới hoặc chuyển cấp đều sinh biến thể ngữ cảnh mới 100%. Trình độ thực tế từ Sinh viên (T1) tới Senior+ (T7) được phán quyết bởi Quản Giáo AI dựa trên Ma trận Độ phủ × Độ sâu × Tốc độ SLA.",
                  "Every refresh or rank-up generates 100% fresh contextual variants. Overall rank from Student (T1) to Senior+ (T7) is adjudicated by The AI Warden across Breadth × Depth × SLA Speed."
                )}
              </p>
              <div class="arena-hero-actions-bar">
                <button type="button" class="arena-btn arena-btn-clay" id="arenaOpenWardenModalBtn">
                  ${arenaTr("Hồ Sơ Phán Quyết Quản Giáo", "Warden Adjudication Dossier")}
                </button>
                <button type="button" class="arena-btn" id="arenaOpenProviderModalBtn">
                  ${arenaTr("Cấu Hình AI / BYOK API", "AI Provider & BYOK Hub")}
                </button>
                <button type="button" class="arena-btn" id="arenaOpenAccountsModalBtn">
                  ${arenaTr("Đổi Hồ Sơ & Đồng Bộ DB", "Switch Profile & Cloud DB")} (${Object.keys(arenaRuntime.accounts).length})
                </button>
                <button type="button" class="arena-btn arena-btn-danger" id="arenaLogoutBtn" title="${arenaTr("Đăng xuất khỏi phiên làm việc hiện tại", "Sign out of current session")}">
                  ${arenaTr("Đăng xuất", "Sign Out")} (@${escapeHtml(acc.githubHandle)})
                </button>
              </div>
            </div>
            <div class="lesson-hero-art">${heroSealArt}</div>
          </div>
        </header>

        <!-- 2. ACADEMY ROADMAP GRID: CAREER LADDER + AI WARDEN LIVE TELEMETRY -->
        <section class="lesson-roadmap-grid">
          <div class="lesson-roadmap-card">
            <div class="roadmap-card-head">
              <span class="roadmap-eyebrow">${arenaTr("THANG CẤP BẬC KỸ SƯ ĐÃ XÁC MINH", "VERIFIED ENGINEERING CAREER LADDER")}</span>
              <h2 class="roadmap-title">${escapeHtml(currentRank.badgeCode)} — ${escapeHtml(isArenaEn() ? currentRank.enTitle : currentRank.title)}</h2>
            </div>
            <div class="arena-rank-ladder" id="arenaRankLadder">
              ${rankLadderHtml}
            </div>
            <div class="arena-metrics-strip">
              <div class="arena-metric-box">
                <span class="arena-metric-label">${arenaTr("Cấp Bậc Thực Tế", "Verified Rank")}</span>
                <span class="arena-metric-value" id="arenaVerifiedRankText">${escapeHtml(currentRank.badgeCode)}</span>
                <span class="arena-metric-note">${escapeHtml(isArenaEn() ? currentRank.enTitle : currentRank.title)}</span>
              </div>
              <div class="arena-metric-box">
                <span class="arena-metric-label">${arenaTr("Độ Phủ (Breadth)", "Breadth Coverage")}</span>
                <span class="arena-metric-value">${digest.metrics.topicsMasteredCount} / 12 (${digest.metrics.breadthPct}%)</span>
                <span class="arena-metric-note">${arenaTr("Chống cày lặp 1 bài", "Anti-grind enforced")}</span>
              </div>
              <div class="arena-metric-box">
                <span class="arena-metric-label">${arenaTr("Độ Sâu (Depth)", "Weighted Depth")}</span>
                <span class="arena-metric-value">${digest.metrics.avgDepthPct}% · L3: ${digest.metrics.l3UnassistedCount}</span>
                <span class="arena-metric-note">L1(20%)+L2(35%)+L3(45%)</span>
              </div>
              <div class="arena-metric-box">
                <span class="arena-metric-label">${arenaTr("Kinh Nghiệm & SLA", "Total XP & SLA")}</span>
                <span class="arena-metric-value">${acc.totalXp} XP · ${acc.wardenState.slaBreachCount} SLA</span>
                <span class="arena-metric-note">Grind flags: ${acc.wardenState.antiGrindFlags}</span>
              </div>
            </div>
          </div>

          <div class="lesson-roadmap-card arena-warden-card ${escapeHtml(acc.wardenState.tone || "neutral")}" id="arena-warden-bar">
            <div class="roadmap-card-head">
              <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;">
                <span class="roadmap-eyebrow">${arenaTr("QUẢN GIÁO AI · GIÁM SÁT TRỰC TIẾP", "THE AI WARDEN · LIVE TELEMETRY MONITOR")}</span>
                <span class="arena-pill">${arenaTr("Chống Học Vẹt & Cày Điểm", "Anti-Rote & Anti-Grind")}</span>
              </div>
              <h2 class="roadmap-title">${arenaTr("Nhận Xét & Chỉ Thị Sát Hạch Trực Tiếp", "Live Adjudication & Remedial Directive")}</h2>
            </div>
            <p class="arena-warden-quote" id="arenaWardenLiveQuote" style="flex:1;">
              ${escapeHtml(isArenaEn() ? acc.wardenState.lastCommentEn : acc.wardenState.lastCommentVi)}
            </p>
            <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;padding-top:10px;border-top:1px solid var(--cds-border-subtle);">
              <span style="font-family:var(--cds-font-mono);font-size:11.5px;color:var(--cds-text-muted);">
                Solved: ${pm.totalQuestionsSolved || 0} · Accuracy: ${pm.totalQuestionsSolved > 0 ? Math.round((pm.totalCorrectAnswers / pm.totalQuestionsSolved) * 100) : 0}% · Chat Q&A: ${pm.totalChatQuestionsAsked || 0}
              </span>
              <button type="button" class="arena-btn" id="arenaQuickWardenBtn">
                ${arenaTr("Mổ Xẻ Trình Độ Chi Tiết →", "Open Full Warden Dossier →")}
              </button>
            </div>
          </div>
        </section>

        <!-- 3. GLOSSARY-STYLE FILTER BAR: TRACK, SYLLABUS STATION, MASTERY LEVEL -->
        <section class="glossary-dict-controls" aria-label="Arena Practice Controls">
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;align-items:end;">
            <div class="arena-control-col">
              <label class="arena-control-label" for="arenaTopicSelect">${arenaTr("Chuyên Đề Sát Hạch (49 Học Phần)", "Syllabus Station Selection")}</label>
              <select class="arena-select" id="arenaTopicSelect">
                ${topicOptionsHtml}
              </select>
            </div>
            <div class="arena-control-col">
              <label class="arena-control-label" for="arenaRoleSelect">${arenaTr("Vị Trí Mục Tiêu (Khớp JD Thị Trường)", "Target JD Role Track")}</label>
              <select class="arena-select" id="arenaRoleSelect">
                <option value="DE" ${acc.roleTrack === "DE" ? "selected" : ""}>Data Engineer (DE · Pipeline / Storage / Streaming)</option>
                <option value="AIE" ${acc.roleTrack === "AIE" ? "selected" : ""}>AI Engineer (AIE · RAG / LLM Serving / Agents)</option>
                <option value="MLE" ${acc.roleTrack === "MLE" ? "selected" : ""}>ML Engineer (MLE · Training / Feature Store / GPU Kernel)</option>
              </select>
            </div>
          </div>

          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;padding-top:10px;border-top:1px solid var(--cds-border-subtle);">
            <div class="glossary-filter-pills" id="arenaLevelTabs" role="tablist">
              ${levelTabsHtml}
            </div>
            <div class="glossary-filter-pills">
              ${rolePillsHtml}
            </div>
          </div>
        </section>

        <!-- 4. WORKSPACE: ANTHROPIC WINDOW CARDS FOR POLYMORPHIC LAB & CONTEXTUAL CHAT -->
        <section class="arena-workspace-grid" id="arena-workspace">
          <div class="arena-window-card">
            <div class="visual-bar">
              <span class="visual-window-dots" aria-hidden="true"><span></span><span></span><span></span></span>
              <span class="visual-bar-title">${escapeHtml(inst.topic)} · ${escapeHtml(inst.levelKey)} · ${escapeHtml(inst.rankBadge)} (${escapeHtml(inst.roleTrack)})</span>
              <span class="visual-engine-tag ${slaWarnCls}" id="arenaSlaTimerPill">SLA: ${secElapsed}s / ${secSla}s</span>
            </div>

            <div class="arena-window-body">
              <div class="arena-q-meta-bar">
                <div class="arena-q-badges">
                  <span class="arena-pill tier-shift">${escapeHtml(inst.rankBadge)} · ${escapeHtml(inst.roleTrack)}</span>
                  <span class="arena-pill">Variant #${escapeHtml(String(inst.variantSeed || 1))}</span>
                  ${inst.assisted ? `<span class="arena-pill sla-warn">Assisted (Có gợi ý)</span>` : ""}
                </div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;">
                  <button type="button" class="arena-btn" id="arenaMutateSeedBtn" title="Sinh biến thể ngữ cảnh mới ngay lập tức">
                    ${arenaTr("↻ Sinh Biến Thể Mới", "↻ Mutate Variant")}
                  </button>
                  <button type="button" class="arena-btn" id="arenaAiRewriteBtn" title="Dùng LLM viết lại góc hỏi mới">
                    ${arenaTr("AI Biến Thể Sâu", "AI Deep Rewrite")}
                  </button>
                </div>
              </div>

              <div class="arena-tier-context-box">
                <strong>${arenaTr("Chuẩn JD & Độ khó theo Cấp bậc hiện tại", "Adaptive Rank & JD Calibration")} (${escapeHtml(inst.rankBadge)}):</strong>
                ${escapeHtml(inst.jdExpectation || inst.tierDirective)}
              </div>

              <p class="arena-q-stem" id="arenaQuestionStem">${escapeHtml(inst.stem)}</p>

              ${inst.codeSnippet ? `<pre class="arena-code-block"><code>${escapeHtml(inst.codeSnippet)}</code></pre>` : ""}

              ${inst.mcqPrompt ? `<div style="font-weight:600;font-size:14px;color:var(--cds-text-primary);">${escapeHtml(inst.mcqPrompt)}</div>` : ""}

              <div class="arena-options-list" id="arenaOptionsList">
                ${optionsHtml}
              </div>

              ${inst.level === 3 ? `
                <div class="arena-l3-defense-box">
                  <label style="font-weight:600;font-size:13.5px;color:var(--cds-text-primary);" for="arenaL3Textarea">
                    ${escapeHtml(inst.openPrompt)}
                  </label>
                  <textarea class="arena-textarea" id="arenaL3Textarea" placeholder="${arenaTr(
                    "Trình bày lập luận nguyên lý gốc, cơ chế xử lý lỗi và đánh đổi kỹ thuật bằng lời của bạn (AI chấm theo bản chất cốt lõi, không bắt bẻ câu chữ máy móc)...",
                    "Write your architectural defense and trade-offs in your own words (AI Semantic Grader evaluates core concepts, not rigid wording)..."
                  )}">${escapeHtml(inst.l3OpenDraft || "")}</textarea>
                  <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;">
                    <span style="font-size:12px;color:var(--cds-text-muted);">
                      ${arenaTr("Tự động lưu nháp tức thì (F5 không mất chữ).", "Draft auto-saved instantaneously across F5.")}
                    </span>
                    <button type="button" class="arena-btn arena-btn-primary" id="arenaSubmitL3Btn">
                      ${arenaTr("Nộp Bài & Chấm Điểm Bản Chất (L3)", "Submit & Run Semantic Grader (L3)")}
                    </button>
                  </div>
                </div>
              ` : ""}

              ${feedbackHtml}
            </div>
          </div>

          <!-- CONTEXTUAL IN-ARENA CHATBOX WINDOW -->
          <aside class="arena-window-card" id="arena-chat-panel">
            <div class="visual-bar">
              <span class="visual-window-dots" aria-hidden="true"><span></span><span></span><span></span></span>
              <span class="visual-bar-title">${arenaTr("Box Chat Hỏi Đáp Trong Bài", "Contextual Study Chat")}</span>
              <span class="visual-engine-tag">
                ${inst.submitted ? arenaTr("Post-Submit · Mở Khóa", "Post-Submit · Unlocked") : arenaTr("Pre-Submit · Chống Lộ Đáp Án", "Pre-Submit · Anti-Spoiler")}
              </span>
            </div>

            <div class="arena-chat-header">
              <span style="font-size:11.5px;color:var(--cds-text-muted);">
                ${arenaTr(
                  `Đang neo ngữ cảnh vào: ${inst.topic} (${inst.levelKey}) · Hồ sơ @${acc.githubHandle}`,
                  `Context anchored to: ${inst.topic} (${inst.levelKey}) · Profile @${acc.githubHandle}`
                )}
              </span>
            </div>

            <div class="arena-chat-messages" id="arenaChatMessages">
              ${chatMessagesHtml}
            </div>

            <div class="arena-chat-quick-row">
              <button type="button" class="arena-chat-chip" data-chat-prompt="${arenaTr("Gợi ý cho tôi nguyên lý gốc để suy luận câu này?", "Give me a first-principles hint for this question?")}">
                ${arenaTr("Gợi ý nguyên lý gốc", "First-principles hint")}
              </button>
              <button type="button" class="arena-chat-chip" data-chat-prompt="${arenaTr("Tại sao các phương án nhiễu lại gây lỗi trên Production?", "Why would the distractor options fail in Production?")}">
                ${arenaTr("Phân tích bẫy Production", "Analyze production traps")}
              </button>
              <button type="button" class="arena-chat-chip" data-chat-prompt="${arenaTr("Cho tôi biết đáp án đúng câu này là A, B, C hay D?", "Tell me the correct answer: A, B, C, or D?")}">
                ${arenaTr("Test hỏi xin đáp án", "Test spoiler guard")}
              </button>
            </div>

            <form class="arena-chat-input-row" id="arenaChatForm">
              <input type="text" class="arena-input" id="arenaChatInput" placeholder="${arenaTr("Hỏi về cơ chế, thuật ngữ hoặc phản biện câu hỏi này...", "Ask about mechanisms, edge cases, or debate this question...")}" autocomplete="off" />
              <button type="submit" class="arena-btn arena-btn-primary" id="arenaChatSendBtn">
                ${arenaTr("Gửi", "Send")}
              </button>
            </form>
          </aside>
        </section>
      </div>
      ${renderArenaActiveModalHtml()}
    `;

    bindArenaDomEvents();
  }

  /* --------------------------------------------------------------------------
     10. MODALS: WARDEN ASSESSMENT, BYOK AI PROVIDER HUB, MULTI-ACCOUNT SANDBOX
     -------------------------------------------------------------------------- */
  function renderArenaActiveModalHtml() {
    if (!arenaRuntime.activeModal) return "";
    const cat = getArenaCatalog();
    const acc = getActiveArenaAccount();
    const digest = readHotCognitiveDigest();

    if (arenaRuntime.activeModal === "warden") {
      const ranks = cat.ranks || [];
      const curRank = ranks.find((r) => r.tier === acc.verifiedRankTier) || ranks[0];
      const nextRank = ranks.find((r) => r.tier === acc.verifiedRankTier + 1) || null;

      const missingReqsVi = nextRank
        ? `Để lên bậc ${nextRank.badgeCode} (${nextRank.title}): cần hoàn thành tối thiểu ${nextRank.minTopicsMastered} chuyên đề (hiện tại: ${digest.metrics.topicsMasteredCount}), độ sâu trung bình ≥ ${nextRank.minMasteryPct}% (hiện tại: ${digest.metrics.avgDepthPct}%), và vượt qua ${nextRank.minL3Passed} bài tự luận L3 không trợ giúp (hiện tại: ${digest.metrics.l3UnassistedCount}).`
        : "Bạn đã đạt đỉnh T7 · Senior+ / Staff Architect!";
      const missingReqsEn = nextRank
        ? `To unlock ${nextRank.badgeCode} (${nextRank.enTitle}): master at least ${nextRank.minTopicsMastered} topics (current: ${digest.metrics.topicsMasteredCount}), weighted depth >= ${nextRank.minMasteryPct}% (current: ${digest.metrics.avgDepthPct}%), and pass ${nextRank.minL3Passed} unassisted L3 defenses (current: ${digest.metrics.l3UnassistedCount}).`
        : "You have reached the pinnacle: T7 · Senior+ / Staff Architect!";

      const customAudit = isArenaEn() ? acc.wardenState.lastAuditReportEn : acc.wardenState.lastAuditReportVi;

      return `
        <div class="modal-backdrop open" id="arenaModalBackdrop">
          <div class="arena-modal-dialog" role="dialog" aria-modal="true" aria-labelledby="arenaWardenModalTitle">
            <div class="arena-modal-header">
              <h2 class="arena-modal-title" id="arenaWardenModalTitle">
                ${arenaTr("Hồ Sơ Phán Quyết Của Quản Giáo AI (The Warden)", "The AI Warden · Principal Adjudication Dossier")}
              </h2>
              <button type="button" class="arena-btn" id="arenaCloseModalBtn">${arenaTr("Đóng", "Close")}</button>
            </div>
            <div class="arena-modal-body">
              <div class="arena-warden-strip ${escapeHtml(acc.wardenState.tone || "neutral")}">
                <div class="arena-warden-left">
                  <span class="arena-warden-badge">W-AI</span>
                  <div class="arena-warden-text-wrap">
                    <div class="arena-warden-header">
                      <span>${escapeHtml(acc.displayName)} · ${escapeHtml(curRank.badgeCode)}</span>
                    </div>
                    <p class="arena-warden-quote" id="arenaWardenModalVerdict">
                      ${escapeHtml(isArenaEn() ? acc.wardenState.lastCommentEn : acc.wardenState.lastCommentVi)}
                    </p>
                  </div>
                </div>
              </div>

              <div class="arena-metrics-strip">
                <div class="arena-metric-box">
                  <span class="arena-metric-label">${arenaTr("Level Thực Tế Đã Chứng Minh", "Verified Actual Rank")}</span>
                  <span class="arena-metric-value">${escapeHtml(curRank.badgeCode)}</span>
                  <span class="arena-metric-note">${escapeHtml(isArenaEn() ? curRank.enTitle : curRank.title)}</span>
                </div>
                <div class="arena-metric-box">
                  <span class="arena-metric-label">${arenaTr("Độ Rộng × Độ Sâu", "Breadth × Depth")}</span>
                  <span class="arena-metric-value">${digest.metrics.breadthPct}% × ${digest.metrics.avgDepthPct}%</span>
                  <span class="arena-metric-note">${digest.metrics.topicsMasteredCount} topics · ${digest.metrics.l3UnassistedCount} L3</span>
                </div>
                <div class="arena-metric-box">
                  <span class="arena-metric-label">${arenaTr("Nhật Ký Chậm SLA & Cày Điểm", "SLA Breaches & Grind Flags")}</span>
                  <span class="arena-metric-value">${acc.wardenState.slaBreachCount} SLA · ${acc.wardenState.antiGrindFlags} Grind</span>
                  <span class="arena-metric-note">${arenaTr("Tự động trừ quyền xét duyệt ảo", "Blocks vanity XP promotion")}</span>
                </div>
              </div>

              <div class="arena-tier-context-box">
                <strong>${arenaTr("Điều kiện Chốt chặn Lên Cấp Tiếp Theo:", "Next Promotion Gate Requirements:")}</strong><br/>
                ${escapeHtml(arenaTr(missingReqsVi, missingReqsEn))}
              </div>

              <div class="arena-tier-context-box">
                <strong>${arenaTr("Điểm yếu & Chuyên đề cần chấn chỉnh:", "Weak Skills & SLA Bottlenecks:")}</strong><br/>
                ${digest.weakSkills.length > 0
                  ? escapeHtml(digest.weakSkills.join(" · "))
                  : arenaTr("Chưa phát hiện lỗ hổng nghiêm trọng hoặc bạn mới làm quá ít bài.", "No critical bottlenecks flagged yet (or insufficient attempts logged).")}
              </div>

              ${customAudit ? `
                <div class="arena-feedback-panel" id="arenaWardenLiveAuditBox">
                  <strong>${arenaTr("Bản Phân Tích Chuyên Sâu Từ Quản Giáo AI:", "Live AI Warden Deep Audit:")}</strong>
                  <div style="font-size:13.5px;line-height:1.58;white-space:pre-wrap;">${escapeHtml(customAudit)}</div>
                </div>
              ` : ""}

              <div style="display:flex;justify-content:flex-end;gap:8px;">
                <button type="button" class="arena-btn arena-btn-primary" id="arenaRunWardenAiAuditBtn">
                  ${arenaTr("Yêu Cầu Quản Giáo AI Mổ Xẻ Toàn Diện (Live)", "Run Live AI Warden Deep Audit")}
                </button>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    if (arenaRuntime.activeModal === "provider") {
      const presets = cat.providerPresets || [];
      const cfg = arenaRuntime.aiConfig;
      const curPreset = getProviderPreset(cfg.providerId);
      const modelList = (cfg.fetchedModels && cfg.fetchedModels.length > 0)
        ? cfg.fetchedModels
        : (curPreset.fallbackModels || [curPreset.defaultModel]);

      const providerOpts = presets.map((p) =>
        `<option value="${escapeHtml(p.id)}" ${p.id === cfg.providerId ? "selected" : ""}>${escapeHtml(p.name)}</option>`
      ).join("");

      const modelOpts = modelList.map((m) =>
        `<option value="${escapeHtml(m)}" ${m === cfg.model ? "selected" : ""}>${escapeHtml(m)}</option>`
      ).join("");

      return `
        <div class="modal-backdrop open" id="arenaModalBackdrop">
          <div class="arena-modal-dialog" role="dialog" aria-modal="true" aria-labelledby="arenaProviderModalTitle">
            <div class="arena-modal-header">
              <h2 class="arena-modal-title" id="arenaProviderModalTitle">
                ${arenaTr("Cấu Hình Đa Nhà Cung Cấp AI (BYOK + Auto Fetch Models)", "Universal AI Provider Hub & Auto Model Discovery")}
              </h2>
              <button type="button" class="arena-btn" id="arenaCloseModalBtn">${arenaTr("Đóng", "Close")}</button>
            </div>
            <div class="arena-modal-body">
              <p style="margin:0;font-size:13px;line-height:1.55;color:var(--cds-text-secondary);">
                ${arenaTr(
                  "Chọn nhà cung cấp (Google Gemini, OpenAI/Codex, Anthropic Claude, xAI Grok, DeepSeek, Alibaba Qwen, Zhipu GLM, Moonshot Kimi, OpenRouter hoặc Custom URL), dán API Key và bấm Fetch Models để nạp danh sách mô hình thực tế.",
                  "Select any AI provider preset, paste your API key, and click Fetch Models to populate live models from the provider's endpoint."
                )}
              </p>

              <div class="arena-control-col">
                <label class="arena-control-label" for="arenaProviderSelect">${arenaTr("1. Nhà Cung Cấp AI (Preset)", "1. AI Provider Preset")}</label>
                <select class="arena-select" id="arenaProviderSelect">${providerOpts}</select>
                <span style="font-size:11.5px;color:var(--cds-text-muted);">${escapeHtml(curPreset.notes || "")}</span>
              </div>

              <div class="arena-control-col">
                <label class="arena-control-label" for="arenaBaseUrlInput">${arenaTr("2. Endpoint Base URL", "2. Endpoint Base URL")}</label>
                <input type="text" class="arena-input" id="arenaBaseUrlInput" value="${escapeHtml(cfg.baseUrl || curPreset.baseUrl)}" />
              </div>

              <div class="arena-control-col">
                <label class="arena-control-label" for="arenaApiKeyInput">${arenaTr("3. API Key Của Bạn (Lưu cục bộ trên trình duyệt)", "3. Your API Key (Stored locally in browser)")}</label>
                <div style="display:flex;gap:8px;">
                  <input type="password" class="arena-input" id="arenaApiKeyInput" value="${escapeHtml(cfg.apiKey || "")}" placeholder="${escapeHtml(curPreset.keyPlaceholder || "API Key...")}" />
                  <button type="button" class="arena-btn arena-btn-clay" id="arenaFetchModelsBtn">
                    Fetch Models
                  </button>
                </div>
              </div>

              <div class="arena-control-col">
                <label class="arena-control-label" for="arenaModelSelect">${arenaTr("4. Chọn Model Hoặc Nhập Model ID", "4. Select Fetched Model or Custom Model ID")}</label>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                  <select class="arena-select" id="arenaModelSelect">${modelOpts}</select>
                  <input type="text" class="arena-input" id="arenaCustomModelInput" value="${escapeHtml(cfg.model || curPreset.defaultModel)}" placeholder="Model ID..." />
                </div>
              </div>

              ${cfg.lastFetchStatus ? `
                <div class="arena-tier-context-box" id="arenaFetchStatusBox">
                  ${escapeHtml(cfg.lastFetchStatus)}
                </div>
              ` : ""}

              <div style="display:flex;justify-content:flex-end;gap:8px;">
                <button type="button" class="arena-btn arena-btn-primary" id="arenaSaveProviderBtn">
                  ${arenaTr("Lưu Cấu Hình AI & Áp Dụng Ngay", "Save & Activate AI Provider")}
                </button>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    if (arenaRuntime.activeModal === "accounts") {
      const allAccs = Object.values(arenaRuntime.accounts);
      const activeAcc = getActiveArenaAccount();
      const activePm = ensureAccountProfileMemory(activeAcc);
      const studyMinutes = Math.max(1, Math.round((activePm.totalStudyTimeMs || 0) / 60000));
      const accuracyPct = activePm.totalQuestionsSolved > 0
        ? Math.round((activePm.totalCorrectAnswers / activePm.totalQuestionsSolved) * 100)
        : 0;

      const cardsHtml = allAccs.map((a) => {
        recomputeAccountAdjudication(a);
        const pm = ensureAccountProfileMemory(a);
        const isCurrent = a.accountId === arenaRuntime.activeAccountId;
        const solvedCount = pm.totalQuestionsSolved || 0;
        const chatCount = pm.totalChatQuestionsAsked || 0;
        return `
          <div class="arena-account-card ${isCurrent ? "active" : ""}" data-account-card="${escapeHtml(a.accountId)}">
            <div>
              <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;">
                <strong style="font-size:13.5px;color:var(--cds-text-primary);">
                  ${escapeHtml(a.displayName)}
                  ${pm.githubVerified ? `<span style="color:var(--cds-olive);font-size:11px;" title="GitHub Verified">✓</span>` : ""}
                </strong>
                <span class="arena-pill">${escapeHtml(a.roleTrack)} · T${a.verifiedRankTier}</span>
              </div>
              <div style="font-size:11.5px;color:var(--cds-text-muted);margin-top:3px;">
                @${escapeHtml(a.githubHandle)} · ${a.totalXp} XP · ${a.computedMetrics ? a.computedMetrics.topicsMasteredCount : 0}/49 topics · SLA:${a.wardenState.slaBreachCount}
              </div>
              <div style="font-size:11px;color:var(--cds-text-secondary);margin-top:3px;font-family:var(--cds-font-mono);">
                Solved: ${solvedCount} · Chat Q&A: ${chatCount} · DB: ${escapeHtml((pm.syncMode || "local_idb").toUpperCase())}
              </div>
            </div>
            <div style="display:flex;gap:6px;margin-top:6px;">
              <button type="button" class="arena-btn ${isCurrent ? "arena-btn-primary" : ""}" data-switch-acc="${escapeHtml(a.accountId)}">
                ${isCurrent ? arenaTr("Đang sử dụng", "Active Profile") : arenaTr("Chuyển sang Acc này", "Switch to Account")}
              </button>
              <button type="button" class="arena-btn" data-reset-acc="${escapeHtml(a.accountId)}">
                Reset
              </button>
            </div>
          </div>
        `;
      }).join("");

      return `
        <div class="modal-backdrop open" id="arenaModalBackdrop">
          <div class="arena-modal-dialog" role="dialog" aria-modal="true" aria-labelledby="arenaAccountsModalTitle">
            <div class="arena-modal-header">
              <h2 class="arena-modal-title" id="arenaAccountsModalTitle">
                ${arenaTr("Đăng Nhập GitHub, Bộ Nhớ Hồ Sơ AI & Đồng Bộ Database Đa Người Dùng", "GitHub Identity, AI Profile Memory & Multi-User Cloud DB")}
              </h2>
              <button type="button" class="arena-btn" id="arenaCloseModalBtn">${arenaTr("Đóng", "Close")}</button>
            </div>
            <div class="arena-modal-body">
              <!-- Active User Long-Term AI Memory & Progress Summary -->
              <div class="arena-l3-defense-box" id="arenaActiveProfileMemoryCard">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                  <div>
                    <strong style="font-size:14px;color:var(--cds-text-primary);">
                      ${arenaTr("Bộ Nhớ Ngữ Cảnh AI Của Hồ Sơ Đang Mở:", "Active Profile Long-Term AI Memory Ledger:")}
                      ${escapeHtml(activeAcc.displayName)} (@${escapeHtml(activeAcc.githubHandle)})
                    </strong>
                    <div style="font-size:11.5px;color:var(--cds-text-muted);margin-top:2px;" id="arenaProfileSyncStatusText">
                      Trạng thái DB: ${escapeHtml(activePm.lastSyncStatus || "LocalStorage + IndexedDB Active")} · Hot Digest Latency: ${arenaRuntime.hotDigestPerfMs}ms
                    </div>
                  </div>
                  <div style="display:flex;gap:6px;flex-wrap:wrap;">
                    <button type="button" class="arena-btn" id="arenaExportJsonBtn">
                      ${arenaTr("Xuất File DB (.JSON)", "Export Profile (.JSON)")}
                    </button>
                    <button type="button" class="arena-btn" id="arenaToggleImportJsonBtn">
                      ${arenaTr("Nhập File DB (.JSON)", "Import Profile (.JSON)")}
                    </button>
                  </div>
                </div>

                <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(135px,1fr));gap:8px;margin-top:6px;">
                  <div class="arena-tier-context-box" style="padding:8px 10px;">
                    <div style="font-size:10.5px;color:var(--cds-text-muted);text-transform:uppercase;">${arenaTr("Câu đã giải / Chính xác", "Solved / Accuracy")}</div>
                    <strong style="font-size:14px;">${activePm.totalQuestionsSolved} câu (${accuracyPct}%)</strong>
                  </div>
                  <div class="arena-tier-context-box" style="padding:8px 10px;">
                    <div style="font-size:10.5px;color:var(--cds-text-muted);text-transform:uppercase;">${arenaTr("Thời gian thực luyện", "Active Study Time")}</div>
                    <strong style="font-size:14px;">${studyMinutes} phút (${Math.round((activePm.totalStudyTimeMs || 0) / 1000)}s)</strong>
                  </div>
                  <div class="arena-tier-context-box" style="padding:8px 10px;">
                    <div style="font-size:10.5px;color:var(--cds-text-muted);text-transform:uppercase;">${arenaTr("Tương tác Box Chat AI", "In-Arena Chat Q&A")}</div>
                    <strong style="font-size:14px;">${activePm.totalChatQuestionsAsked} câu hỏi</strong>
                  </div>
                  <div class="arena-tier-context-box" style="padding:8px 10px;">
                    <div style="font-size:10.5px;color:var(--cds-text-muted);text-transform:uppercase;">${arenaTr("Chuyên đề đã làm chủ", "Mastered Topics")}</div>
                    <strong style="font-size:14px;">${activePm.masteredTopicsList.length > 0 ? escapeHtml(activePm.masteredTopicsList.join(", ")) : arenaTr("Chưa có", "None yet")}</strong>
                  </div>
                </div>

                <div style="font-size:12px;color:var(--cds-text-secondary);margin-top:4px;">
                  <strong>${arenaTr("Lỗi sai lặp lại được 3 luồng AI ghi nhớ để xoáy sâu:", "Recurring Mistake Patterns Remembered by All 3 AI Engines:")}</strong>
                  ${activePm.mistakePatterns.length > 0
                    ? escapeHtml(activePm.mistakePatterns.join(" · "))
                    : arenaTr("Chưa phát hiện mẫu lỗi sai hệ thống nào.", "No recurring misconception patterns logged yet.")}
                </div>

                <div id="arenaImportJsonCollapse" style="display:none;flex-direction:column;gap:8px;margin-top:8px;">
                  <textarea class="arena-l3-textarea" id="arenaImportJsonTextarea" style="min-height:80px;" placeholder="${arenaTr("Dán nội dung JSON hồ sơ đã xuất vào đây để khôi phục...", "Paste exported profile JSON here to restore...")}"></textarea>
                  <div style="display:flex;justify-content:flex-end;">
                    <button type="button" class="arena-btn arena-btn-primary" id="arenaConfirmImportJsonBtn">
                      ${arenaTr("Khôi Phục Hồ Sơ Từ JSON", "Restore Profile from JSON")}
                    </button>
                  </div>
                </div>
              </div>

              <!-- GitHub Login & Personal Gist Cloud DB Sync -->
              <div class="arena-l3-defense-box">
                <strong style="font-size:13.5px;">${arenaTr("1. Đăng Nhập GitHub Thực Tế & Đồng Bộ Cloud Cá Nhân (GitHub Gist DB)", "1. Live GitHub Login & Personal Cloud Sync (GitHub Gist DB)")}</strong>
                <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px;">
                  <input type="text" class="arena-input" id="arenaNewAccName" value="" placeholder="${arenaTr("Tên hiển thị (VD: Vũ Hải Đang)", "Display Name")}" />
                  <input type="text" class="arena-input" id="arenaNewAccGithub" value="" placeholder="GitHub username (VD: torvalds)..." />
                  <select class="arena-select" id="arenaNewAccRole">
                    <option value="DE">Data Engineer (DE)</option>
                    <option value="AIE">AI Engineer (AIE)</option>
                    <option value="MLE">ML Engineer (MLE)</option>
                  </select>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:4px;">
                  <input type="password" class="arena-input" id="arenaGithubTokenInput" value="${escapeHtml(activePm.githubToken || "")}" placeholder="${arenaTr("Tùy chọn: GitHub Token (quyền 'gist') để lưu Cloud...", "Optional: GitHub PAT (gist scope) for Cloud Sync...")}" />
                  <input type="text" class="arena-input" id="arenaGithubGistIdInput" value="${escapeHtml(activePm.gistId || "")}" placeholder="${arenaTr("Tùy chọn: Gist ID (để trống sẽ tự tạo/tìm)", "Optional: Gist ID (auto-created if blank)")}" />
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-top:4px;">
                  <span style="font-size:11.5px;color:var(--cds-text-muted);">
                    ${arenaTr("Nhập GitHub Username để tự động xác thực qua api.github.com và tạo/chuyển sang hồ sơ riêng.", "Enter GitHub username to verify via api.github.com and activate dedicated profile DB.")}
                  </span>
                  <div style="display:flex;gap:6px;flex-wrap:wrap;">
                    <button type="button" class="arena-btn arena-btn-primary" id="arenaCreateAccBtn">
                      ${arenaTr("Xác Thực GitHub & Đăng Nhập / Tạo Hồ Sơ", "Verify GitHub & Login / Create Profile")}
                    </button>
                    <button type="button" class="arena-btn" id="arenaGistPushBtn">
                      ${arenaTr("Push Lên Gist DB", "Push to Gist DB")}
                    </button>
                    <button type="button" class="arena-btn" id="arenaGistPullBtn">
                      ${arenaTr("Pull Từ Gist DB", "Pull from Gist DB")}
                    </button>
                  </div>
                </div>
              </div>

              <!-- Multi-User Team Cloud DB (Supabase PostgREST) -->
              <div class="arena-l3-defense-box">
                <strong style="font-size:13.5px;">${arenaTr("2. Đồng Bộ Database Nhóm Nhiều Người Dùng (Supabase Cloud DB)", "2. Multi-User Team Cloud Database (Supabase PostgREST Sync)")}</strong>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                  <input type="text" class="arena-input" id="arenaSupabaseUrlInput" value="${escapeHtml(arenaRuntime.supabaseConfig.url || "")}" placeholder="Supabase Project URL (https://xxx.supabase.co)..." />
                  <input type="password" class="arena-input" id="arenaSupabaseKeyInput" value="${escapeHtml(arenaRuntime.supabaseConfig.anonKey || "")}" placeholder="Supabase Anon Public Key..." />
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-top:4px;">
                  <span style="font-size:11.5px;color:var(--cds-text-muted);" id="arenaSupabaseStatusLabel">
                    ${escapeHtml(arenaRuntime.supabaseConfig.syncStatus || "Local-First + IndexedDB Ready")}
                  </span>
                  <div style="display:flex;gap:6px;flex-wrap:wrap;">
                    <button type="button" class="arena-btn" id="arenaSupabasePushBtn">
                      ${arenaTr("Lưu Hồ Sơ Lên Supabase Nhóm", "Push Profile to Team Supabase")}
                    </button>
                    <button type="button" class="arena-btn" id="arenaSupabasePullBtn">
                      ${arenaTr("Tải Toàn Bộ Hồ Sơ Nhóm Về Máy", "Pull All Team Profiles")}
                    </button>
                  </div>
                </div>
              </div>

              <!-- Multi-Account Switcher Grid -->
              <div class="arena-tier-context-box">
                <strong>${arenaTr("3. Danh Sách Người Dùng Trong DB & 5 Acc Ảo Kiểm Thử (" + allAccs.length + " Profiles):", "3. Multi-User DB Profiles & Virtual Sandbox Personas (" + allAccs.length + " Profiles):")}</strong>
                ${arenaTr(
                  "Mỗi người dùng có bộ nhớ tiến độ, lịch sử lỗi sai, điểm độ phủ/độ sâu và nhật ký Quản Giáo hoàn toàn độc lập.",
                  "Each user profile isolates its own mastery matrix, verified rank, AI memory digest, SLA telemetry, and Warden verdicts."
                )}
              </div>

              <div class="arena-account-grid" id="arenaAccountGrid">
                ${cardsHtml}
              </div>
            </div>
          </div>
        </div>
      `;
    }

    return "";
  }

  /* --------------------------------------------------------------------------
     11. DOM EVENT WIRING & LIVE AI ACTIONS
     -------------------------------------------------------------------------- */
  function bindArenaDomEvents() {
    const acc = getActiveArenaAccount();
    const inst = acc.activeSession;

    // Login Gate events
    const gateForm = document.getElementById("arenaGateLoginForm");
    if (gateForm) {
      gateForm.onsubmit = async (ev) => {
        ev.preventDefault();
        const ghInp = document.getElementById("arenaGateGithubInput");
        const nameInp = document.getElementById("arenaGateNameInput");
        const roleInp = document.getElementById("arenaGateRoleSelect");
        const tokInp = document.getElementById("arenaGateTokenInput");
        const loginBtn = document.getElementById("arenaGateLoginBtn");
        const gh = (ghInp && ghInp.value.trim()) || "engineer-dev";
        const name = (nameInp && nameInp.value.trim()) || "";
        const role = (roleInp && roleInp.value) || "DE";
        const tok = (tokInp && tokInp.value.trim()) || "";
        if (loginBtn) {
          loginBtn.disabled = true;
          loginBtn.textContent = arenaTr("Đang xác thực hồ sơ GitHub...", "Verifying GitHub identity...");
        }
        await verifyAndFetchGitHubIdentity(gh, name, role, tok);
        arenaRuntime.isLoggedIn = true;
        saveArenaPersistence();
        renderArenaView();
      };
    }

    document.querySelectorAll("[data-gate-quick-login]").forEach((btn) => {
      btn.onclick = () => {
        const targetId = btn.getAttribute("data-gate-quick-login");
        if (targetId && arenaRuntime.accounts[targetId]) {
          arenaRuntime.activeAccountId = targetId;
          arenaRuntime.isLoggedIn = true;
          arenaRuntime.activeModal = null;
          saveArenaPersistence();
          renderArenaView();
        }
      };
    });

    const logoutBtn = document.getElementById("arenaLogoutBtn");
    if (logoutBtn) {
      logoutBtn.onclick = () => {
        logoutArenaSession();
      };
    }

    const wardenBtn = document.getElementById("arenaOpenWardenModalBtn");
    if (wardenBtn) wardenBtn.onclick = () => { arenaRuntime.activeModal = "warden"; renderArenaView(); };

    const quickWardenBtn = document.getElementById("arenaQuickWardenBtn");
    if (quickWardenBtn) quickWardenBtn.onclick = () => { arenaRuntime.activeModal = "warden"; renderArenaView(); };

    const providerBtn = document.getElementById("arenaOpenProviderModalBtn");
    if (providerBtn) providerBtn.onclick = () => { arenaRuntime.activeModal = "provider"; renderArenaView(); };

    const accountsBtn = document.getElementById("arenaOpenAccountsModalBtn");
    if (accountsBtn) accountsBtn.onclick = () => { arenaRuntime.activeModal = "accounts"; renderArenaView(); };

    const closeModalBtn = document.getElementById("arenaCloseModalBtn");
    if (closeModalBtn) closeModalBtn.onclick = () => { arenaRuntime.activeModal = null; renderArenaView(); };

    const backdrop = document.getElementById("arenaModalBackdrop");
    if (backdrop) {
      backdrop.onclick = (ev) => {
        if (ev.target === backdrop) {
          arenaRuntime.activeModal = null;
          renderArenaView();
        }
      };
    }

    const roleSelect = document.getElementById("arenaRoleSelect");
    if (roleSelect) {
      roleSelect.onchange = () => {
        acc.roleTrack = roleSelect.value;
        generatePolymorphicInstance(acc, true);
        renderArenaView();
      };
    }

    document.querySelectorAll("[data-arena-role-pill]").forEach((btn) => {
      btn.onclick = () => {
        const newRole = btn.getAttribute("data-arena-role-pill");
        if (newRole) {
          acc.roleTrack = newRole;
          generatePolymorphicInstance(acc, true);
          renderArenaView();
        }
      };
    });

    const topicSelect = document.getElementById("arenaTopicSelect");
    if (topicSelect) {
      topicSelect.onchange = () => {
        acc.selectedTopic = topicSelect.value;
        generatePolymorphicInstance(acc, false);
        renderArenaView();
      };
    }

    document.querySelectorAll("[data-arena-level]").forEach((btn) => {
      btn.onclick = () => {
        acc.selectedLevel = Number(btn.getAttribute("data-arena-level"));
        generatePolymorphicInstance(acc, false);
        renderArenaView();
      };
    });

    const mutateBtn = document.getElementById("arenaMutateSeedBtn");
    if (mutateBtn) {
      mutateBtn.onclick = () => {
        generatePolymorphicInstance(acc, true);
        renderArenaView();
      };
    }

    const aiRewriteBtn = document.getElementById("arenaAiRewriteBtn");
    if (aiRewriteBtn) {
      aiRewriteBtn.onclick = async () => {
        aiRewriteBtn.disabled = true;
        aiRewriteBtn.textContent = arenaTr("Đang sinh biến thể AI...", "Generating AI Variant...");
        try {
          const profilePacket = JSON.stringify(buildUnifiedProfileContextPacket(false), null, 2);
          const prompt = `Ngữ cảnh Hồ sơ Đăng nhập:\n${profilePacket}\n\nHãy viết lại bối cảnh câu hỏi kỹ thuật sau sang một tình huống vận hành thực tế mới mẻ ở cấp bậc ${inst.rankBadge} (${inst.roleTrack}) nhưng giữ nguyên 100% đáp án đúng và bản chất cơ chế gốc:\nCâu hỏi gốc: ${inst.stem}`;
          const rewritten = await callUniversalArenaAI(prompt, "Chỉ trả về đúng nội dung câu hỏi đã biến đổi ngữ cảnh (3-5 câu) khớp với cấp bậc hồ sơ người học, không kèm lời chào hay đáp án.");
          if (rewritten && rewritten.length > 25) {
            inst.stem = rewritten.trim();
            inst.aiMutated = true;
            saveArenaPersistence();
          } else {
            generatePolymorphicInstance(acc, true);
          }
        } catch (e) {
          generatePolymorphicInstance(acc, true);
        }
        renderArenaView();
      };
    }

    document.querySelectorAll("[data-arena-opt]").forEach((btn) => {
      btn.onclick = () => {
        const idx = Number(btn.getAttribute("data-arena-opt"));
        inst.selectedOption = idx;
        saveArenaPersistence();
        if (inst.level === 1 || inst.level === 2) {
          submitArenaAnswer();
        } else {
          renderArenaView();
        }
      };
    });

    const l3Textarea = document.getElementById("arenaL3Textarea");
    if (l3Textarea) {
      l3Textarea.oninput = () => {
        inst.l3OpenDraft = l3Textarea.value;
        saveArenaPersistence();
      };
    }

    const submitL3Btn = document.getElementById("arenaSubmitL3Btn");
    if (submitL3Btn) {
      submitL3Btn.onclick = () => {
        submitArenaAnswer();
      };
    }

    const nextMutatedBtn = document.getElementById("arenaNextMutatedBtn");
    if (nextMutatedBtn) {
      nextMutatedBtn.onclick = () => {
        generatePolymorphicInstance(acc, true);
        renderArenaView();
      };
    }

    const jumpBtn = document.getElementById("arenaJumpStationBtn");
    if (jumpBtn) {
      jumpBtn.onclick = () => {
        const tCode = jumpBtn.getAttribute("data-topic") || "F01";
        const stg = Number(jumpBtn.getAttribute("data-stage") || 1);
        selectTopic(tCode, stg, true);
      };
    }

    // Contextual Chatbox events
    document.querySelectorAll("[data-chat-prompt]").forEach((chip) => {
      chip.onclick = () => {
        const q = chip.getAttribute("data-chat-prompt");
        sendArenaContextualChat(q);
      };
    });

    const chatForm = document.getElementById("arenaChatForm");
    if (chatForm) {
      chatForm.onsubmit = (ev) => {
        ev.preventDefault();
        const inp = document.getElementById("arenaChatInput");
        if (inp && inp.value.trim()) {
          const val = inp.value.trim();
          inp.value = "";
          sendArenaContextualChat(val);
        }
      };
    }

    // Modal-specific events
    const runAuditBtn = document.getElementById("arenaRunWardenAiAuditBtn");
    if (runAuditBtn) {
      runAuditBtn.onclick = async () => {
        runAuditBtn.disabled = true;
        runAuditBtn.textContent = arenaTr("Quản Giáo AI đang mổ xẻ hồ sơ...", "The Warden is auditing your profile...");
        const digest = readHotCognitiveDigest();
        const profilePacket = JSON.stringify(buildUnifiedProfileContextPacket(true), null, 2);
        const cat = getArenaCatalog();
        const langKey = isArenaEn() ? "en" : "vi";
        const sysPrompt = (cat.wardenConfig && cat.wardenConfig.persona && cat.wardenConfig.persona[langKey] && cat.wardenConfig.persona[langKey].systemPrompt) || "";
        const userPrompt = `Ngữ cảnh Hồ sơ Đăng nhập & Câu hỏi hiện tại:\n${profilePacket}\n\nHãy đưa ra bản phán quyết thẳng thừng, sắc bén (4-6 câu) về trình độ thực tế, các lỗi chậm SLA, hành vi cày điểm lặp (nếu có) và chỉ định rõ 2 bài tập cần làm ngay.`;
        try {
          const res = await callUniversalArenaAI(userPrompt, sysPrompt);
          if (isArenaEn()) acc.wardenState.lastAuditReportEn = res;
          else acc.wardenState.lastAuditReportVi = res;
        } catch (e) {
          const fallbackVi = `[Phán Quyết Quản Giáo AI · Hồ sơ ${acc.displayName} (@${acc.githubHandle})]:\n1. Trình độ đã chứng minh: Tier ${digest.verifiedRankTier} (${digest.verifiedRankId.toUpperCase()}) với độ phủ ${digest.metrics.topicsMasteredCount}/12 chuyên đề (${digest.metrics.breadthPct}%) và độ sâu trung bình ${digest.metrics.avgDepthPct}%.\n2. Kỷ luật tốc độ & Chống cày điểm: Ghi nhận ${digest.slaBreachCount} lần ngâm câu hỏi vượt chuẩn SLA và ${digest.antiGrindFlags} cờ cảnh báo cày lặp bài cũ.\n3. Chỉ thị bắt buộc: ${digest.weakSkills.length > 0 ? "Lập tức khắc phục lỗ hổng tại " + digest.weakSkills.join(", ") : "Mở rộng sang các chuyên đề chưa chạm tới và vượt qua bài tự luận Level 3 mà không dùng gợi ý"}.`;
          const fallbackEn = `[The AI Warden Audit · Profile ${acc.displayName} (@${acc.githubHandle})]:\n1. Proven Rank: Tier ${digest.verifiedRankTier} (${digest.verifiedRankId.toUpperCase()}) with ${digest.metrics.topicsMasteredCount}/12 topic breadth (${digest.metrics.breadthPct}%) and ${digest.metrics.avgDepthPct}% weighted depth.\n2. SLA & Anti-Grind Telemetry: Logged ${digest.slaBreachCount} SLA dwell-time breaches and ${digest.antiGrindFlags} repeated-topic grind flags.\n3. Mandatory Directive: ${digest.weakSkills.length > 0 ? "Remediate weak fundamentals in " + digest.weakSkills.join(", ") : "Expand into untouched syllabus topics and pass Level 3 defenses unassisted"}.`;
          acc.wardenState.lastAuditReportVi = fallbackVi;
          acc.wardenState.lastAuditReportEn = fallbackEn;
        }
        saveArenaPersistence();
        renderArenaView();
      };
    }

    const provSelect = document.getElementById("arenaProviderSelect");
    if (provSelect) {
      provSelect.onchange = () => {
        const p = getProviderPreset(provSelect.value);
        arenaRuntime.aiConfig.providerId = p.id;
        arenaRuntime.aiConfig.protocol = p.protocol;
        arenaRuntime.aiConfig.baseUrl = p.baseUrl;
        arenaRuntime.aiConfig.model = p.defaultModel;
        arenaRuntime.aiConfig.fetchedModels = p.fallbackModels.slice();
        arenaRuntime.aiConfig.lastFetchStatus = "";
        saveArenaPersistence();
        renderArenaView();
      };
    }

    const fetchModelsBtn = document.getElementById("arenaFetchModelsBtn");
    if (fetchModelsBtn) {
      fetchModelsBtn.onclick = async () => {
        const baseInp = document.getElementById("arenaBaseUrlInput");
        const keyInp = document.getElementById("arenaApiKeyInput");
        if (baseInp) arenaRuntime.aiConfig.baseUrl = baseInp.value.trim();
        if (keyInp) arenaRuntime.aiConfig.apiKey = keyInp.value.trim();
        fetchModelsBtn.disabled = true;
        fetchModelsBtn.textContent = "Fetching...";
        const res = await fetchArenaProviderModels(
          arenaRuntime.aiConfig.providerId,
          arenaRuntime.aiConfig.baseUrl,
          arenaRuntime.aiConfig.apiKey
        );
        arenaRuntime.aiConfig.fetchedModels = res.models;
        if (res.models && res.models.length > 0) {
          arenaRuntime.aiConfig.model = res.models[0];
        }
        arenaRuntime.aiConfig.lastFetchStatus = res.statusMsg;
        saveArenaPersistence();
        renderArenaView();
      };
    }

    const modSelect = document.getElementById("arenaModelSelect");
    if (modSelect) {
      modSelect.onchange = () => {
        arenaRuntime.aiConfig.model = modSelect.value;
        const customModInp = document.getElementById("arenaCustomModelInput");
        if (customModInp) customModInp.value = modSelect.value;
      };
    }

    const saveProvBtn = document.getElementById("arenaSaveProviderBtn");
    if (saveProvBtn) {
      saveProvBtn.onclick = () => {
        const baseInp = document.getElementById("arenaBaseUrlInput");
        const keyInp = document.getElementById("arenaApiKeyInput");
        const customModInp = document.getElementById("arenaCustomModelInput");
        if (baseInp) arenaRuntime.aiConfig.baseUrl = baseInp.value.trim();
        if (keyInp) arenaRuntime.aiConfig.apiKey = keyInp.value.trim();
        if (customModInp && customModInp.value.trim()) {
          arenaRuntime.aiConfig.model = customModInp.value.trim();
        }
        arenaRuntime.activeModal = null;
        saveArenaPersistence();
        renderArenaView();
        if (typeof showToast === "function") {
          showToast(arenaTr(`Đã kích hoạt ${arenaRuntime.aiConfig.providerId} (${arenaRuntime.aiConfig.model})`, `Activated ${arenaRuntime.aiConfig.providerId} (${arenaRuntime.aiConfig.model})`));
        }
      };
    }

    // Account switching & virtual account creation
    document.querySelectorAll("[data-switch-acc]").forEach((btn) => {
      btn.onclick = () => {
        const targetId = btn.getAttribute("data-switch-acc");
        if (arenaRuntime.accounts[targetId]) {
          arenaRuntime.activeAccountId = targetId;
          arenaRuntime.isLoggedIn = true;
          arenaRuntime.activeModal = null;
          saveArenaPersistence();
          renderArenaView();
        }
      };
    });

    document.querySelectorAll("[data-reset-acc]").forEach((btn) => {
      btn.onclick = () => {
        const targetId = btn.getAttribute("data-reset-acc");
        const old = arenaRuntime.accounts[targetId];
        if (old) {
          const fresh = createBlankAccount(old.accountId, old.displayName, old.githubHandle, old.roleTrack, old.presetType);
          arenaRuntime.accounts[targetId] = seedPresetAccountData(fresh);
          saveArenaPersistence();
          renderArenaView();
        }
      };
    });

    const createAccBtn = document.getElementById("arenaCreateAccBtn");
    if (createAccBtn) {
      createAccBtn.onclick = async () => {
        const nameInp = document.getElementById("arenaNewAccName");
        const ghInp = document.getElementById("arenaNewAccGithub");
        const roleInp = document.getElementById("arenaNewAccRole");
        const tokenInp = document.getElementById("arenaGithubTokenInput");
        const gistInp = document.getElementById("arenaGithubGistIdInput");
        const name = (nameInp && nameInp.value.trim()) || ("Virtual Dev #" + (Object.keys(arenaRuntime.accounts).length + 1));
        const gh = (ghInp && ghInp.value.trim()) || ("dev-virtual-" + (Object.keys(arenaRuntime.accounts).length + 1));
        const role = (roleInp && roleInp.value) || "DE";
        const ghToken = (tokenInp && tokenInp.value.trim()) || "";
        const gistId = (gistInp && gistInp.value.trim()) || "";

        createAccBtn.disabled = true;
        createAccBtn.textContent = arenaTr("Đang xác thực GitHub...", "Verifying GitHub...");
        const res = await verifyAndFetchGitHubIdentity(gh, name, role, ghToken);
        if (res && res.account && gistId) {
          ensureAccountProfileMemory(res.account).gistId = gistId;
        }
        arenaRuntime.isLoggedIn = true;
        arenaRuntime.activeModal = null;
        saveArenaPersistence();
        renderArenaView();
      };
    }

    const gistPushBtn = document.getElementById("arenaGistPushBtn");
    if (gistPushBtn) {
      gistPushBtn.onclick = async () => {
        const tokenInp = document.getElementById("arenaGithubTokenInput");
        const gistInp = document.getElementById("arenaGithubGistIdInput");
        const pm = ensureAccountProfileMemory(acc);
        if (tokenInp) pm.githubToken = tokenInp.value.trim();
        if (gistInp) pm.gistId = gistInp.value.trim();
        gistPushBtn.disabled = true;
        gistPushBtn.textContent = "Pushing Gist...";
        await syncAccountWithGitHubGist("push");
        renderArenaView();
      };
    }

    const gistPullBtn = document.getElementById("arenaGistPullBtn");
    if (gistPullBtn) {
      gistPullBtn.onclick = async () => {
        const tokenInp = document.getElementById("arenaGithubTokenInput");
        const gistInp = document.getElementById("arenaGithubGistIdInput");
        const pm = ensureAccountProfileMemory(acc);
        if (tokenInp) pm.githubToken = tokenInp.value.trim();
        if (gistInp) pm.gistId = gistInp.value.trim();
        gistPullBtn.disabled = true;
        gistPullBtn.textContent = "Pulling Gist...";
        await syncAccountWithGitHubGist("pull");
        renderArenaView();
      };
    }

    const sbPushBtn = document.getElementById("arenaSupabasePushBtn");
    if (sbPushBtn) {
      sbPushBtn.onclick = async () => {
        const urlInp = document.getElementById("arenaSupabaseUrlInput");
        const keyInp = document.getElementById("arenaSupabaseKeyInput");
        if (urlInp) arenaRuntime.supabaseConfig.url = urlInp.value.trim();
        if (keyInp) arenaRuntime.supabaseConfig.anonKey = keyInp.value.trim();
        sbPushBtn.disabled = true;
        sbPushBtn.textContent = "Pushing Supabase...";
        await syncAccountWithSupabase("push");
        renderArenaView();
      };
    }

    const sbPullBtn = document.getElementById("arenaSupabasePullBtn");
    if (sbPullBtn) {
      sbPullBtn.onclick = async () => {
        const urlInp = document.getElementById("arenaSupabaseUrlInput");
        const keyInp = document.getElementById("arenaSupabaseKeyInput");
        if (urlInp) arenaRuntime.supabaseConfig.url = urlInp.value.trim();
        if (keyInp) arenaRuntime.supabaseConfig.anonKey = keyInp.value.trim();
        sbPullBtn.disabled = true;
        sbPullBtn.textContent = "Pulling Team DB...";
        await syncAccountWithSupabase("pull_all");
        renderArenaView();
      };
    }

    const exportJsonBtn = document.getElementById("arenaExportJsonBtn");
    if (exportJsonBtn) {
      exportJsonBtn.onclick = () => {
        const jsonStr = exportActiveAccountJson();
        try {
          const blob = new Blob([jsonStr], { type: "application/json" });
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = `fsds_arena_profile_${acc.githubHandle || acc.accountId}.json`;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(url);
        } catch (e) {
          // Fallback if Blob download restricted
        }
        if (typeof showToast === "function") {
          showToast(arenaTr("Đã xuất file JSON Hồ sơ & Bộ nhớ AI!", "Exported Profile & AI Memory JSON!"));
        }
      };
    }

    const toggleImportBtn = document.getElementById("arenaToggleImportJsonBtn");
    if (toggleImportBtn) {
      toggleImportBtn.onclick = () => {
        const box = document.getElementById("arenaImportJsonCollapse");
        if (box) {
          box.style.display = (box.style.display === "none") ? "flex" : "none";
        }
      };
    }

    const confirmImportBtn = document.getElementById("arenaConfirmImportJsonBtn");
    if (confirmImportBtn) {
      confirmImportBtn.onclick = () => {
        const ta = document.getElementById("arenaImportJsonTextarea");
        if (ta && ta.value.trim()) {
          try {
            importAccountJsonString(ta.value.trim());
            arenaRuntime.isLoggedIn = true;
            arenaRuntime.activeModal = null;
            saveArenaPersistence();
            renderArenaView();
            if (typeof showToast === "function") {
              showToast(arenaTr("Đã khôi phục Hồ sơ & Bộ nhớ AI thành công!", "Restored Profile & AI Memory successfully!"));
            }
          } catch (err) {
            if (typeof showToast === "function") {
              showToast(arenaTr("File JSON không hợp lệ!", "Invalid Profile JSON!"));
            }
          }
        }
      };
    }
  }

  /* --------------------------------------------------------------------------
     12. PROGRAMMATIC SANDBOX & E2E DEV TEST HARNESS API (window.FSDSArena)
     -------------------------------------------------------------------------- */
  window.FSDSArena = {
    open: openPracticeView,
    getRuntime: () => arenaRuntime,
    getActiveAccount: getActiveArenaAccount,
    readHotDigest: readHotCognitiveDigest,
    buildProfileContextPacket: buildUnifiedProfileContextPacket,
    logout: logoutArenaSession,
    switchAccount: (accountId) => {
      initArenaPersistence();
      if (arenaRuntime.accounts[accountId]) {
        arenaRuntime.activeAccountId = accountId;
        arenaRuntime.isLoggedIn = true;
        saveArenaPersistence();
        if (typeof activeTopic !== "undefined" && activeTopic === "PRACTICE") renderArenaView();
        return true;
      }
      return false;
    },
    createVirtualAccount: (displayName, githubHandle, roleTrack) => {
      initArenaPersistence();
      const id = "virt_test_" + Date.now() + "_" + Math.floor(Math.random() * 1000);
      arenaRuntime.accounts[id] = createBlankAccount(id, displayName, githubHandle, roleTrack, "custom");
      arenaRuntime.activeAccountId = id;
      arenaRuntime.isLoggedIn = true;
      saveArenaPersistence();
      if (typeof activeTopic !== "undefined" && activeTopic === "PRACTICE") renderArenaView();
      return id;
    },
    verifyGitHubIdentity: verifyAndFetchGitHubIdentity,
    syncGitHubGist: syncAccountWithGitHubGist,
    syncSupabase: syncAccountWithSupabase,
    exportProfileJson: exportActiveAccountJson,
    importProfileJson: importAccountJsonString,
    fetchProviderModels: fetchArenaProviderModels,
    mutateQuestion: () => {
      const acc = getActiveArenaAccount();
      const inst = generatePolymorphicInstance(acc, true);
      if (typeof activeTopic !== "undefined" && activeTopic === "PRACTICE") renderArenaView();
      return inst;
    },
    sendChat: sendArenaContextualChat
  };
"""
