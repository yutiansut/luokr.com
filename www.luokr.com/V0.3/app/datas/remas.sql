
-- Table: remas
CREATE TABLE remas ( 
    rema_id   INTEGER         PRIMARY KEY AUTOINCREMENT,
    post_id   INTEGER,
    user_id   INTEGER         DEFAULT ( 0 ),
    user_ip   VARCHAR( 39 ),
    rema_pid  INTEGER         DEFAULT ( 0 ),
    user_name VARCHAR( 80 ),
    user_mail VARCHAR( 500 ),
    rema_cont TEXT,
    rema_rank INT( 10 )       DEFAULT ( 100 ),
    rema_plus INT( 10 )       DEFAULT ( 0 ),
    rema_mins INT( 10 )       DEFAULT ( 0 ),
    rema_ctms INT( 10 )       NOT NULL,
    rema_utms INT( 10 )       NOT NULL 
);


-- Index: idx_remaRank_remaId
CREATE INDEX idx_remaRank_remaId ON remas ( 
    rema_rank,
    rema_id 
);


-- Index: idx_postId_remaRank_remaId
CREATE INDEX idx_postId_remaRank_remaId ON remas ( 
    post_id,
    rema_rank,
    rema_id 
);

