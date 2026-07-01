-- Run this once in Supabase SQL Editor (supabase.com → your project → SQL Editor)

create table if not exists trades (
    id           text primary key,
    created_at   timestamptz default now(),
    symbol       text,
    timeframe    text,
    model        text,
    direction    text,
    confidence   text,
    rr_ratio     float,
    entry_zone   text,
    stop         text,
    pt1          text,
    pt2          text,
    call         jsonb,
    outcome      text default 'pending',
    notes        text default ''
);

-- Index for fast feedback lookups
create index if not exists trades_outcome_idx on trades (outcome);
create index if not exists trades_created_at_idx on trades (created_at desc);
