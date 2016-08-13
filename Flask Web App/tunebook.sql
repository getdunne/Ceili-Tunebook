CREATE TYPE tune_types AS ENUM ('reel', 'jig', 'hornpipe', 'waltz', 'march', 'polka', 'other');

CREATE TABLE tunes
(
    id serial PRIMARY KEY,  -- also used as image ID
    title text,
    composer text,
    tune_type tune_types,
    timesig integer,    -- 4/4 stored as 44, 6/8 as 68, etc.
    key text,           -- e.g. G Major, A Minor
    file_ext text,      -- e.g. png, jpg; tune_id is file name
    url text,           -- optional reference to source
    abc text            -- optional ABC code (multi-line)
);

CREATE TABLE sets
(
    id serial PRIMARY KEY,
    book_name text,     -- name of original source book, e.g. "KCB Big Book"
    set_name text,      -- title for this set
    wrap boolean,       -- true if set wraps from last tune to first
    wrap_to integer,    -- 0-based offset of tune to wrap to
    tune_list text      -- JSON list of 2-element lists "[[tune_id, "(2A,2B)x2"], ... ]"
);

CREATE TABLE books
(
    id serial PRIMARY KEY,
    name text,
    url text,           -- URL for cover image, if any
    content text        -- JSON nested-list structure, "[]" if empty
);
