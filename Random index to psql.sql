
Random index to psql


CREATE TABLE data_loaad (
    rn INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_type TEXT,
    id INTEGER,
    job_name TEXT,
    host_name TEXT,
    collection TEXT,
    action VARCHAR(2),
    purpose TEXT DEFAULT 'analyst-etl',
    created_at TIMESTAMP NOT NULL DEFAULT clock_timestamp()
) ;



INSERT INTO data_loaad (id_type, id, job_name, host_name, collection, action, purpose, created_at)
SELECT
    'type_' || (random() * 1000)::int AS id_type,
    (random() * 1000)::int AS id,
    'job_' || (random() * 1000)::int AS job_name,
    'host_' || (random() * 1000)::int AS host_name,
    'collection_' || (random() * 1000)::int AS collection,
    substr('abcdefghijklmnopqrstuvwxyz', floor(random() * 26)::int + 1, 1) || substr('abcdefghijklmnopqrstuvwxyz', floor(random() * 26)::int + 1, 1) AS action,
    'purpose_' || (random() * 1000)::int AS purpose,
    NOW() - (random() * 365 * INTERVAL '1 day') AS created_at
FROM generate_series(1, 1000);
