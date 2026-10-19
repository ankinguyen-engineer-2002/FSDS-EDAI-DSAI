-- ==============================================================================
-- FSDS · EDAI · DSAI — AI ADAPTIVE PRACTICE & CAREER MASTERY ARENA
-- Supabase PostgreSQL Schema, Row-Level Security (RLS) & Adjudication RPCs
-- Compatible with GitHub OAuth PKCE + Dual-Persistence IndexedDB Outbox Sync
-- ==============================================================================

create extension if not exists "pgcrypto";

-- 1. ARENA PROFILES (1:1 with auth.users or synced virtual/GitHub profiles)
create table if not exists public.arena_profiles (
    user_id uuid primary key references auth.users(id) on delete cascade,
    github_username text,
    github_id bigint,
    display_name text,
    role_track text not null default 'DE' check (role_track in ('DE', 'AIE', 'MLE')),
    verified_rank_tier smallint not null default 1 check (verified_rank_tier between 1 and 7),
    verified_rank_id text not null default 'student',
    total_xp integer not null default 0 check (total_xp >= 0),
    breadth_pct numeric(5,2) not null default 0.00,
    weighted_depth_pct numeric(5,2) not null default 0.00,
    unassisted_accuracy_pct numeric(5,2) not null default 0.00,
    sla_breach_count integer not null default 0,
    anti_grind_flags integer not null default 0,
    cognitive_digest jsonb not null default '{}'::jsonb,
    last_warden_verdict jsonb not null default '{}'::jsonb,
    updated_at timestamptz not null default now(),
    created_at timestamptz not null default now()
);

-- 2. ARENA TOPIC MASTERY MATRIX (Breadth x Depth x Anti-Grind per Topic & Level)
create table if not exists public.arena_topic_mastery (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.arena_profiles(user_id) on delete cascade,
    topic_code text not null,
    blueprint_id text not null,
    l1_best_score numeric(5,2) not null default 0,
    l2_best_score numeric(5,2) not null default 0,
    l3_best_score numeric(5,2) not null default 0,
    l1_unassisted_passes integer not null default 0,
    l2_unassisted_passes integer not null default 0,
    l3_unassisted_passes integer not null default 0,
    total_attempts integer not null default 0,
    effective_mastery_pct numeric(5,2) not null default 0,
    best_tier_cleared smallint not null default 0,
    avg_active_ms integer not null default 0,
    sla_breaches integer not null default 0,
    seen_fingerprints jsonb not null default '[]'::jsonb,
    last_practiced_at timestamptz not null default now(),
    unique (user_id, blueprint_id)
);

-- 3. ARENA ACTIVE SESSIONS (Preserves exact in-flight question & L3 draft across F5/devices)
create table if not exists public.arena_active_sessions (
    user_id uuid primary key references public.arena_profiles(user_id) on delete cascade,
    topic_code text not null,
    blueprint_id text not null,
    practice_level smallint not null check (practice_level between 1 and 3),
    rank_tier smallint not null check (rank_tier between 1 and 7),
    instance_id text not null,
    question_fingerprint text not null,
    question_payload jsonb not null,
    selected_option smallint,
    l3_open_draft text not null default '',
    assisted boolean not null default false,
    submitted boolean not null default false,
    active_elapsed_ms integer not null default 0,
    updated_at timestamptz not null default now()
);

-- 4. ARENA ATTEMPT HISTORY (Immutable Event Ledger for Warden Adjudication)
create table if not exists public.arena_attempt_history (
    attempt_id uuid primary key default gen_random_uuid(),
    client_event_id text unique,
    user_id uuid not null references public.arena_profiles(user_id) on delete cascade,
    topic_code text not null,
    blueprint_id text not null,
    practice_level smallint not null check (practice_level between 1 and 3),
    rank_tier smallint not null check (rank_tier between 1 and 7),
    question_fingerprint text not null,
    selected_option smallint,
    is_correct boolean not null,
    score_pct numeric(5,2) not null,
    xp_awarded integer not null default 0,
    assisted boolean not null default false,
    anti_grind_capped boolean not null default false,
    active_answer_ms integer not null default 0,
    sla_target_ms integer not null default 45000,
    sla_breached boolean not null default false,
    l3_open_answer text,
    l3_ai_evaluation jsonb,
    warden_comment_vi text,
    warden_comment_en text,
    created_at timestamptz not null default now()
);

-- 5. ARENA CONTEXTUAL CHAT LOGS (Scoped strictly to in-arena question instances)
create table if not exists public.arena_chat_logs (
    message_id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.arena_profiles(user_id) on delete cascade,
    instance_id text not null,
    blueprint_id text not null,
    practice_level smallint not null check (practice_level between 1 and 3),
    phase text not null check (phase in ('pre_submit', 'post_submit')),
    sender_role text not null check (sender_role in ('user', 'assistant', 'warden')),
    content text not null,
    spoiler_blocked boolean not null default false,
    created_at timestamptz not null default now()
);

-- 6. ARENA RANK ADJUDICATION EVENTS (Warden Promotion / Rejection Ledger)
create table if not exists public.arena_rank_events (
    event_id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.arena_profiles(user_id) on delete cascade,
    previous_tier smallint not null,
    adjudicated_tier smallint not null,
    verdict_status text not null check (verdict_status in ('PROMOTED', 'HELD', 'ANTI_GRIND_BLOCKED')),
    breadth_pct numeric(5,2) not null,
    weighted_depth_pct numeric(5,2) not null,
    warden_verdict_vi text not null,
    warden_verdict_en text not null,
    evidence_snapshot jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

-- Enable Row-Level Security (RLS) on all tables
alter table public.arena_profiles enable row level security;
alter table public.arena_topic_mastery enable row level security;
alter table public.arena_active_sessions enable row level security;
alter table public.arena_attempt_history enable row level security;
alter table public.arena_chat_logs enable row level security;
alter table public.arena_rank_events enable row level security;

-- Self-access RLS policies
drop policy if exists "arena_profiles_self_all" on public.arena_profiles;
create policy "arena_profiles_self_all" on public.arena_profiles
    for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "arena_topic_mastery_self_all" on public.arena_topic_mastery;
create policy "arena_topic_mastery_self_all" on public.arena_topic_mastery
    for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "arena_active_sessions_self_all" on public.arena_active_sessions;
create policy "arena_active_sessions_self_all" on public.arena_active_sessions
    for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "arena_attempt_history_self_all" on public.arena_attempt_history;
create policy "arena_attempt_history_self_all" on public.arena_attempt_history
    for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "arena_chat_logs_self_all" on public.arena_chat_logs;
create policy "arena_chat_logs_self_all" on public.arena_chat_logs
    for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "arena_rank_events_self_all" on public.arena_rank_events;
create policy "arena_rank_events_self_all" on public.arena_rank_events
    for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- 7. DIRECT TEAM MULTI-USER MEMORY STORE (Zero-OAuth PostgREST Sync for Static GitHub Pages)
create table if not exists public.arena_user_memory_store (
    account_id text primary key,
    github_handle text not null,
    display_name text not null,
    role_track text not null default 'DE',
    verified_rank_tier smallint not null default 1,
    verified_rank_id text not null default 'student',
    total_xp integer not null default 0,
    topics_mastered_count integer not null default 0,
    breadth_pct numeric(5,2) not null default 0.00,
    avg_depth_pct numeric(5,2) not null default 0.00,
    l3_unassisted_count integer not null default 0,
    sla_breach_count integer not null default 0,
    anti_grind_flags integer not null default 0,
    total_study_time_ms bigint not null default 0,
    cognitive_digest jsonb not null default '{}'::jsonb,
    full_profile_payload jsonb not null default '{}'::jsonb,
    updated_at timestamptz not null default now()
);

create index if not exists idx_arena_user_memory_github on public.arena_user_memory_store(github_handle);
create index if not exists idx_arena_user_memory_rank on public.arena_user_memory_store(verified_rank_tier desc, total_xp desc);

alter table public.arena_user_memory_store enable row level security;
drop policy if exists "arena_user_memory_team_sync" on public.arena_user_memory_store;
create policy "arena_user_memory_team_sync" on public.arena_user_memory_store
    for all using (true) with check (true);

