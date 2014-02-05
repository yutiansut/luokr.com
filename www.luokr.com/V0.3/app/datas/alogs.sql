
-- Table: alogs
CREATE TABLE alogs ( 
    alog_id   INTEGER        PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER        DEFAULT ( 0 ),
    user_ip   VARCHAR( 39 )  DEFAULT ( '' ),
    user_name VARCHAR( 80 ),
    alog_text TEXT,
    alog_ctms INT( 10 )      NOT NULL
);

