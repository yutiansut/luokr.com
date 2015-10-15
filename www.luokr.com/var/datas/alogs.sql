
-- Table: alogs
CREATE TABLE alogs ( 
    alog_id   INTEGER        PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER        DEFAULT ( 0 ),
    user_ip   VARCHAR( 39 ),
    user_name VARCHAR( 64 )  COLLATE 'NOCASE',
    alog_text TEXT,
    alog_data TEXT,
    alog_ctms INT( 10 )      NOT NULL 
);


-- Index: idx_userId_alogId
CREATE INDEX idx_userId_alogId ON alogs ( 
    user_id DESC,
    alog_id DESC 
);

