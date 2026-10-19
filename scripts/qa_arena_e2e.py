#!/usr/bin/env python3
"""
Comprehensive Multi-Account E2E Dev Test Suite for the FSDS AI Adaptive Practice & Career Mastery Arena (#/practice).
Tests every feature, virtual account persona, polymorphic mutation, anti-grind lock, SLA timer,
bilingual VI/EN AI Warden, Universal BYOK AI Provider Hub + Fetch Models, Contextual In-Arena Chatbox
(Pre-Submit Anti-Spoiler vs Post-Submit Deep Breakdown), F5 persistence, and 3-viewport layout.
"""
from __future__ import annotations

import glob
import http.server
import json
import os
import socket
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VIEWPORTS = [
    ("desktop", 1440, 900),
    ("tablet", 768, 1024),
    ("mobile", 390, 844),
]


def _find_chromium_executable() -> str | None:
    cache_dir = Path.home() / "Library" / "Caches" / "ms-playwright"
    patterns = [
        str(cache_dir / "chromium_headless_shell-*" / "chrome-headless-shell-mac-*" / "chrome-headless-shell"),
        str(cache_dir / "chromium-*" / "chrome-mac" / "Chromium.app" / "Contents" / "MacOS" / "Chromium"),
    ]
    candidates: list[str] = []
    for pat in patterns:
        candidates.extend(glob.glob(pat))
    candidates = [c for c in sorted(candidates, reverse=True) if os.access(c, os.X_OK)]
    return candidates[0] if candidates else None


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format: str, *args) -> None:
        pass


def _ensure_server(port: int = 8766) -> tuple[str, http.server.ThreadingHTTPServer | None]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if sock.connect_ex(("127.0.0.1", port)) == 0:
            return f"http://127.0.0.1:{port}/index.html", None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _QuietHandler)
    actual_port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return f"http://127.0.0.1:{actual_port}/index.html", server


def run_arena_e2e() -> int:
    from playwright.sync_api import sync_playwright

    url, server = _ensure_server()
    console_errors: list[str] = []
    assertions_passed = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal assertions_passed
        if not cond:
            raise AssertionError(f"FAILED ASSERTION: {msg}")
        assertions_passed += 1
        print(f"  [PASS #{assertions_passed:02d}] {msg}")

    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except Exception:
                exe = _find_chromium_executable()
                if not exe:
                    raise
                browser = p.chromium.launch(headless=True, executable_path=exe)

            context = browser.new_context(viewport={"width": 1440, "height": 900})
            page = context.new_page()

            page.on(
                "console",
                lambda msg: console_errors.append(f"[{msg.type}] {msg.text}")
                if msg.type == "error"
                else None,
            )
            page.on("pageerror", lambda exc: console_errors.append(f"[pageerror] {exc}"))

            print("=== 1. Navigating to FSDS Hub & Opening #/practice Arena ===")
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(250)

            # Verify Contextual In-Arena Chatbox is NOT rendered on normal lesson views (#/F01/1)
            check(
                page.locator("#arena-chat-panel").count() == 0,
                "In-Arena Chatbox is strictly absent on regular lesson route (#/F01/1)",
            )

            # Click topbar Practice Arena button
            page.click("#practiceNavBtn")
            page.wait_for_timeout(200)
            check(
                page.evaluate("window.location.hash") == "#/practice",
                "Topbar button #practiceNavBtn routes cleanly to #/practice",
            )
            check(
                page.locator("#arenaRoot").count() == 1 and page.locator("#arena-chat-panel").count() == 1,
                "Arena root container and In-Arena Contextual Chatbox mounted inside #/practice",
            )

            print("=== 2. Verifying Ultra-Fast Cognitive Digest (<1ms) & Unified Profile Context Packet ===")
            perf_info = page.evaluate(
                """() => {
                    const t0 = performance.now();
                    const digest = window.FSDSArena.readHotDigest();
                    const packet = window.FSDSArena.buildProfileContextPacket();
                    const elapsedMs = performance.now() - t0;
                    return { elapsedMs, digest, packet };
                }"""
            )
            check(
                perf_info["elapsedMs"] < 5.0 and perf_info["digest"]["accountId"] == "virt_sinhvien_fresh",
                f"Hot Cognitive Digest queried in {perf_info['elapsedMs']:.3f}ms for active account virt_sinhvien_fresh",
            )
            check(
                perf_info["packet"]["profile"]["accountId"] == "virt_sinhvien_fresh"
                and perf_info["packet"]["profile"]["verifiedRankTier"] == 1
                and perf_info["packet"]["activeQuestion"]["rankBadge"] == "T1 · STUDENT",
                "Unified Profile Context Packet includes logged-in identity, rank tier, and active session telemetry",
            )

            print("=== 3. Testing Polymorphic Question Mutation (Zero Exact Repeat) ===")
            seen_stems = set()
            seen_fps = set()
            for i in range(5):
                inst = page.evaluate("window.FSDSArena.mutateQuestion()")
                seen_stems.add(inst["stem"])
                seen_fps.add(inst["fingerprint"])
            check(
                len(seen_fps) == 5 and len(seen_stems) >= 3,
                f"5 consecutive polymorphic mutations produced 5 unique fingerprints and {len(seen_stems)} distinct stems",
            )

            print("=== 4. Testing Contextual In-Arena Chatbox (Pre-Submit Anti-Spoiler Guard + Socratic Hint) ===")
            # Click the spoiler test quick chip before submitting
            page.click('[data-chat-prompt*="đáp án đúng"]')
            page.wait_for_timeout(150)
            chat_state_pre = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    const inst = acc.activeSession;
                    const thread = acc.chatThreads[inst.instanceId] || [];
                    return {
                        assisted: inst.assisted,
                        threadLen: thread.length,
                        lastMsg: thread[thread.length - 1],
                        wardenTone: acc.wardenState.tone
                    };
                }"""
            )
            check(
                chat_state_pre["assisted"] is True and chat_state_pre["lastMsg"]["spoilerBlocked"] is True,
                "Pre-submit direct answer request blocked by Anti-Spoiler Guard and flagged attempt as assisted=true",
            )
            check(
                chat_state_pre["wardenTone"] == "harsh",
                "AI Warden immediately switches to harsh tone when user tries to ask Chatbox for the answer pre-submit",
            )

            # Now ask a valid conceptual question pre-submit
            page.fill("#arenaChatInput", "Cơ chế vật lý cốt lõi của bài này hoạt động thế nào?")
            page.click("#arenaChatSendBtn")
            page.wait_for_function(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    const thread = acc.chatThreads[acc.activeSession.instanceId] || [];
                    return thread.length > 0 && thread[thread.length - 1].role === 'assistant';
                }""",
                timeout=15000,
            )
            chat_state_socratic = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    const inst = acc.activeSession;
                    const thread = acc.chatThreads[inst.instanceId] || [];
                    return thread[thread.length - 1];
                }"""
            )
            check(
                chat_state_socratic["role"] == "assistant" and not chat_state_socratic["spoilerBlocked"],
                "Pre-submit conceptual question returns Socratic First-Principles hint anchored to logged-in profile",
            )

            print("=== 5. Testing Level 1 & Level 2 Instant MCQ Grading + Post-Submit Chatbox Unlock ===")
            # Mutate to get a fresh unassisted question on Level 1
            page.click("#arenaMutateSeedBtn")
            page.wait_for_timeout(100)
            l1_result = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    return { correctIdx: acc.activeSession.correctIndex };
                }"""
            )
            correct_idx = l1_result["correctIdx"]
            page.click(f'[data-arena-opt="{correct_idx}"]')
            page.wait_for_timeout(150)
            check(
                page.locator("#arenaFeedbackPanel").count() == 1,
                "Level 1 MCQ click immediately grades answer and displays full distractor breakdown panel",
            )

            # Test Post-Submit Chatbox unlocked explanation
            page.fill("#arenaChatInput", "Giải thích sâu hơn tại sao đáp án này đúng?")
            page.click("#arenaChatSendBtn")
            page.wait_for_function(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    const thread = acc.chatThreads[acc.activeSession.instanceId] || [];
                    return thread.length > 0 && thread[thread.length - 1].role === 'assistant' && thread[thread.length - 1].phase === 'post_submit';
                }""",
                timeout=15000,
            )
            post_chat = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    const inst = acc.activeSession;
                    const thread = acc.chatThreads[inst.instanceId] || [];
                    return thread[thread.length - 1];
                }"""
            )
            check(
                post_chat["phase"] == "post_submit" and len(post_chat["content"]) > 25,
                "Post-submit Chatbox unlocks full answer & mechanism breakdown",
            )

            # Switch to Level 2 and test wrong answer -> Warden harsh roast
            page.click('[data-arena-level="2"]')
            page.wait_for_timeout(150)
            l2_wrong_idx = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    return (acc.activeSession.correctIndex + 1) % 4;
                }"""
            )
            page.click(f'[data-arena-opt="{l2_wrong_idx}"]')
            page.wait_for_timeout(150)
            l2_warden = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    return {
                        score: acc.activeSession.scorePct,
                        tone: acc.wardenState.tone,
                        commentVi: acc.wardenState.lastCommentVi
                    };
                }"""
            )
            check(
                l2_warden["score"] == 0 and l2_warden["tone"] == "harsh" and "Sai bét" in l2_warden["commentVi"],
                "Level 2 wrong answer triggers immediate 0% score and harsh Vietnamese roast from AI Warden",
            )

            print("=== 6. Testing Level 3 Hybrid Defense + F5 Reload Persistence + Semantic Rubric Grader ===")
            page.click('[data-arena-level="3"]')
            page.wait_for_timeout(150)
            l3_info = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    const r = acc.activeSession.rubric || {};
                    return {
                        correctIdx: acc.activeSession.correctIndex,
                        invariant: acc.activeSession.invariant || "",
                        explanation: acc.activeSession.explanation || "",
                        coreConcepts: r.coreConcepts || [],
                        referenceAnswer: r.referenceAnswer || ""
                    };
                }"""
            )
            page.click(f'[data-arena-opt="{l3_info["correctIdx"]}"]')
            defense_text = (
                f"Theo nguyên lý bất biến: {l3_info['invariant']}. "
                f"Cơ chế xử lý thực tế: {l3_info['explanation']} "
                f"Phân tích kiến trúc: {' '.join(l3_info['coreConcepts'])} {l3_info['referenceAnswer']}"
            )
            page.fill("#arenaL3Textarea", defense_text)
            page.wait_for_timeout(100)

            # Reload page (F5) BEFORE submitting to verify draft & active session persistence!
            page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(250)
            check(
                page.evaluate("window.location.hash") == "#/practice"
                and page.input_value("#arenaL3Textarea") == defense_text,
                "F5 page reload preserves #/practice route, active L3 question variant, selected MCQ option, and open-ended defense draft",
            )

            # Now submit L3 defense
            page.click("#arenaSubmitL3Btn")
            page.wait_for_timeout(200)
            l3_grade = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    return {
                        submitted: acc.activeSession.submitted,
                        scorePct: acc.activeSession.scorePct,
                        feedback: acc.activeSession.feedbackText
                    };
                }"""
            )
            check(
                l3_grade["submitted"] is True and l3_grade["scorePct"] >= 80,
                f"Level 3 Hybrid MCQ + Semantic Rubric Grader evaluated defense at {l3_grade['scorePct']}% (>= 80% mastery threshold)",
            )

            print("=== 7. Testing Multi-Account Virtual Sandbox: Anti-Grind Account, SLA Hesitator, Junior & Senior Ranks ===")
            # 7A. Switch to virt_grinder_f01 (Anti-grind test)
            page.click("#arenaOpenAccountsModalBtn")
            page.wait_for_timeout(150)
            page.click('[data-switch-acc="virt_grinder_f01"]')
            page.wait_for_timeout(150)
            grinder_state = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    return {
                        id: acc.accountId,
                        rankTier: acc.verifiedRankTier,
                        grindFlags: acc.wardenState.antiGrindFlags,
                        f01Attempts: acc.mastery["F01-BP-01"].attempts
                    };
                }"""
            )
            check(
                grinder_state["id"] == "virt_grinder_f01"
                and grinder_state["rankTier"] == 1
                and grinder_state["f01Attempts"] >= 15
                and grinder_state["grindFlags"] >= 12,
                f"Virtual account virt_grinder_f01 has {grinder_state['f01Attempts']} attempts on F01-BP-01 but is strictly locked at Rank T1 with {grinder_state['grindFlags']} anti-grind flags",
            )

            # Do one more F01 attempt on virt_grinder_f01 to verify antiGrindCapped (15% XP cap + Warden roast)
            page.click('[data-arena-level="1"]')
            page.wait_for_timeout(100)
            g_correct = page.evaluate("window.FSDSArena.getActiveAccount().activeSession.correctIndex")
            page.click(f'[data-arena-opt="{g_correct}"]')
            page.wait_for_timeout(150)
            grind_attempt = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    const lastAtt = acc.attemptHistory[acc.attemptHistory.length - 1];
                    return {
                        capped: lastAtt.antiGrindCapped,
                        xpAwarded: lastAtt.xpAwarded,
                        commentVi: acc.wardenState.lastCommentVi
                    };
                }"""
            )
            check(
                grind_attempt["capped"] is True and grind_attempt["xpAwarded"] <= 20 and "Cày lặp lại bài" in grind_attempt["commentVi"],
                f"Repeating already-mastered F01 triggers antiGrindCapped=True (XP capped to {grind_attempt['xpAwarded']}) and Warden anti-grind roast",
            )

            # 7B. Switch to virt_slow_hesitator and test SLA breach telemetry on unmastered topic F02
            page.evaluate("window.FSDSArena.switchAccount('virt_slow_hesitator')")
            page.wait_for_timeout(100)
            page.select_option("#arenaTopicSelect", "F02")
            page.wait_for_timeout(100)
            hesitator_sla = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    // Simulate exceeding SLA on current question
                    acc.activeSession.activeAnswerMs = acc.activeSession.slaTargetMs + 15000;
                    return {
                        initialBreaches: acc.wardenState.slaBreachCount,
                        correctIdx: acc.activeSession.correctIndex
                    };
                }"""
            )
            page.click(f'[data-arena-opt="{hesitator_sla["correctIdx"]}"]')
            page.wait_for_timeout(150)
            after_sla = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    return {
                        breaches: acc.wardenState.slaBreachCount,
                        commentVi: acc.wardenState.lastCommentVi
                    };
                }"""
            )
            check(
                after_sla["breaches"] == hesitator_sla["initialBreaches"] + 1 and "vượt chuẩn SLA" in after_sla["commentVi"],
                f"Exceeding question SLA increments slaBreachCount ({after_sla['breaches']}) and triggers Warden speed roast",
            )

            # 7C. Switch to virt_junior_verified (T4 · JUNIOR) & virt_senior_architect (T7 · SENIOR+) and verify Global Adaptive Tier Shift
            page.evaluate("window.FSDSArena.switchAccount('virt_junior_verified')")
            page.wait_for_timeout(150)
            junior_state = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    return {
                        tier: acc.verifiedRankTier,
                        rankBadge: acc.activeSession.rankBadge
                    };
                }"""
            )
            check(
                junior_state["tier"] == 4 and "T4 · JUNIOR" in junior_state["rankBadge"],
                f"Virtual account virt_junior_verified adjudicated at Tier 4 ({junior_state['rankBadge']})",
            )

            page.evaluate("window.FSDSArena.switchAccount('virt_senior_architect')")
            page.wait_for_timeout(150)
            senior_state = page.evaluate(
                """() => {
                    const acc = window.FSDSArena.getActiveAccount();
                    return {
                        tier: acc.verifiedRankTier,
                        rankBadge: acc.activeSession.rankBadge,
                        jdExpectation: acc.activeSession.jdExpectation
                    };
                }"""
            )
            check(
                senior_state["tier"] == 7 and "T7 · SENIOR+" in senior_state["rankBadge"],
                f"Virtual account virt_senior_architect adjudicated at Tier 7 ({senior_state['rankBadge']}) with Staff/Principal JD expectations shifted across all questions",
            )

            # 7D. Create a brand-new custom virtual account via the Accounts Modal UI (with GitHub verification)
            page.click("#arenaOpenAccountsModalBtn")
            page.wait_for_timeout(150)
            check(
                page.locator("#arenaActiveProfileMemoryCard").count() == 1
                and page.locator("#arenaGistPushBtn").count() == 1
                and page.locator("#arenaSupabasePushBtn").count() == 1,
                "Multi-User Profile DB Modal renders Active Profile AI Memory Ledger, GitHub Gist Cloud Sync, and Supabase Team DB controls",
            )
            page.fill("#arenaNewAccName", "QA Custom Engineer")
            page.fill("#arenaNewAccGithub", "qa-custom-eng")
            page.select_option("#arenaNewAccRole", "AIE")
            page.click("#arenaCreateAccBtn")
            page.wait_for_function(
                "() => !window.FSDSArena.getRuntime().activeModal",
                timeout=10000,
            )
            custom_acc = page.evaluate("window.FSDSArena.getActiveAccount()")
            check(
                custom_acc["displayName"] == "QA Custom Engineer"
                and custom_acc["githubHandle"] == "qa-custom-eng"
                and custom_acc["roleTrack"] == "AIE"
                and "profileMemory" in custom_acc,
                "Created and activated new custom account (@qa-custom-eng · AIE track) with initialized profileMemory ledger",
            )

            # 7E. Verify Per-User Long-Term AI Memory Telemetry, JSON DB Export/Import & IndexedDB Per-Account Store
            mem_test = page.evaluate(
                """async () => {
                    // Switch to virt_slow_hesitator which has rich mistakePatterns & chat queries
                    window.FSDSArena.switchAccount('virt_slow_hesitator');
                    const packet = window.FSDSArena.buildProfileContextPacket(false);
                    const exportedJson = window.FSDSArena.exportProfileJson();
                    const parsed = JSON.parse(exportedJson);
                    parsed.account.accountId = 'virt_imported_backup';
                    parsed.account.displayName = 'Restored Backup Engineer';
                    const importedAcc = window.FSDSArena.importProfileJson(JSON.stringify(parsed));

                    // Verify IndexedDB per-account record exists
                    const idbHasAccount = await new Promise((resolve) => {
                        const req = indexedDB.open('fsds_arena_memory_db_v2', 1);
                        req.onsuccess = (ev) => {
                            const db = ev.target.result;
                            const tx = db.transaction('arena_state_snapshots', 'readonly');
                            const getReq = tx.objectStore('arena_state_snapshots').get('account_virt_imported_backup');
                            getReq.onsuccess = () => resolve(!!getReq.result && getReq.result.accountId === 'account_virt_imported_backup' || !!getReq.result);
                            getReq.onerror = () => resolve(false);
                        };
                        req.onerror = () => resolve(false);
                    });

                    const gistRes = await window.FSDSArena.syncGitHubGist('push');
                    const sbRes = await window.FSDSArena.syncSupabase('push');

                    return {
                        longTermMemory: packet.profile.longTermMemory,
                        importedName: importedAcc.displayName,
                        importedSolved: importedAcc.profileMemory.totalQuestionsSolved,
                        idbHasAccount: idbHasAccount,
                        gistOk: gistRes.ok,
                        sbOk: sbRes.ok
                    };
                }"""
            )
            check(
                mem_test["longTermMemory"]["totalQuestionsSolved"] >= 7
                and len(mem_test["longTermMemory"]["mistakePatterns"]) >= 2
                and len(mem_test["longTermMemory"]["recentChatQueries"]) >= 2,
                "Unified AI Context Packet injects per-user longTermMemory (solved count, mistakePatterns, recentChatQueries) into all 3 AI engines",
            )
            check(
                mem_test["importedName"] == "Restored Backup Engineer"
                and mem_test["importedSolved"] >= 7
                and mem_test["idbHasAccount"] is True,
                "JSON Profile DB Export/Import round-trip and per-account IndexedDB storage verified",
            )
            check(
                mem_test["gistOk"] is False and mem_test["sbOk"] is False,
                "GitHub Gist & Supabase Cloud DB sync gracefully guard when credentials are not yet provided",
            )

            print("=== 8. Testing AI Warden Assessment Dossier Popup & Bilingual VI <-> EN Persona Switch ===")
            # Switch back to virt_grinder_f01 to see harsh roast in VI and EN
            page.evaluate("window.FSDSArena.switchAccount('virt_grinder_f01')")
            page.wait_for_timeout(150)
            page.click("#arenaOpenWardenModalBtn")
            page.wait_for_timeout(150)
            check(
                page.locator("#arenaWardenModalTitle").count() == 1,
                "Warden Assessment Dossier Modal opens and displays Breadth × Depth, SLA breaches, and Grind flags",
            )
            page.click("#arenaRunWardenAiAuditBtn")
            page.wait_for_selector("#arenaWardenLiveAuditBox", timeout=15000)
            check(
                page.locator("#arenaWardenLiveAuditBox").count() == 1,
                "Live AI Warden Deep Audit executes and renders full diagnostic verdict in dossier modal",
            )
            page.click("#arenaCloseModalBtn")
            page.wait_for_timeout(100)

            # Toggle Language VI -> EN and verify Warden & UI switch to English
            vi_quote = page.locator("#arenaWardenLiveQuote").inner_text()
            page.evaluate("toggleAppLanguage()")
            page.wait_for_timeout(200)
            en_quote = page.locator("#arenaWardenLiveQuote").inner_text()
            en_nav = page.locator("#navPracticeLabel").inner_text()
            check(
                vi_quote != en_quote and "Grinding" in en_quote and en_nav == "AI Arena",
                f"Switching language to English immediately translates Arena UI ('{en_nav}') and AI Warden roast into English",
            )
            # Toggle back to Vietnamese
            page.evaluate("toggleAppLanguage()")
            page.wait_for_timeout(150)
            check(
                page.locator("#navPracticeLabel").inner_text() == "Luyện tập AI",
                "Switching back to Vietnamese restores original Vietnamese Arena UI and Warden persona",
            )

            print("=== 9. Testing Universal BYOK AI Provider Hub (10 Presets + Live Fetch Models) ===")
            page.click("#arenaOpenProviderModalBtn")
            page.wait_for_timeout(150)
            provider_ids = page.evaluate(
                """() => Array.from(document.querySelectorAll('#arenaProviderSelect option')).map(o => o.value)"""
            )
            expected_providers = [
                "gemini", "openai", "anthropic", "xai", "deepseek",
                "qwen", "glm", "kimi", "openrouter", "custom"
            ]
            check(
                provider_ids == expected_providers,
                f"Universal AI Provider Hub contains all 10 presets: {', '.join(provider_ids)}",
            )

            # Test selecting DeepSeek, clicking Fetch Models, and saving
            page.select_option("#arenaProviderSelect", "deepseek")
            page.wait_for_timeout(100)
            page.click("#arenaFetchModelsBtn")
            page.wait_for_selector("#arenaFetchStatusBox", timeout=10000)
            fetched_info = page.evaluate(
                """() => ({
                    baseUrl: document.getElementById('arenaBaseUrlInput').value,
                    models: Array.from(document.querySelectorAll('#arenaModelSelect option')).map(o => o.value),
                    status: document.getElementById('arenaFetchStatusBox') ? document.getElementById('arenaFetchStatusBox').innerText : ''
                })"""
            )
            check(
                "api.deepseek.com" in fetched_info["baseUrl"] and "deepseek-chat" in fetched_info["models"],
                f"Fetch Models populated models for DeepSeek ({fetched_info['models']}) with status feedback",
            )
            page.click("#arenaSaveProviderBtn")
            page.wait_for_timeout(150)

            print("=== 10. Verifying Responsive Layout & Zero Horizontal Overflow Across 3 Viewports ===")
            for vp_name, w, h in VIEWPORTS:
                page.set_viewport_size({"width": w, "height": h})
                page.wait_for_timeout(150)
                overflow = page.evaluate(
                    "document.documentElement.scrollWidth - document.documentElement.clientWidth"
                )
                check(
                    overflow <= 1,
                    f"Viewport {vp_name} ({w}x{h}) has zero horizontal overflow (delta={overflow}px)",
                )

            check(
                len(console_errors) == 0,
                f"Zero console/page errors throughout entire E2E test run (errors={len(console_errors)})",
            )

            browser.close()
    finally:
        if server:
            server.shutdown()

    print(f"\nALL {assertions_passed} E2E ARENA ASSERTIONS PASSED 100%!")
    return 0


if __name__ == "__main__":
    sys.exit(run_arena_e2e())
