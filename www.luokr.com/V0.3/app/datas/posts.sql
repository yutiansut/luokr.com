
-- Table: posts
CREATE TABLE posts ( 
    post_id      INTEGER          PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER          DEFAULT ( 0 ),
    post_title   VARCHAR( 120 ),
    post_descp   VARCHAR( 200 ),
    post_author  VARCHAR( 80 ),
    post_source  VARCHAR( 1000 ),
    post_summary TEXT,
    post_content TEXT,
    post_ctms    INT( 10 )        NOT NULL,
    post_utms    INT( 10 )        NOT NULL,
    post_ptms    INT( 10 )        NOT NULL,
    post_remc    INT( 10 )        DEFAULT ( 0 ),
    post_rank    INT( 10 )        DEFAULT ( 99 ),
    post_stat    INT( 1 )         NOT NULL
                                  DEFAULT ( 0 ) 
);

-- Table: post_terms
CREATE TABLE post_terms ( 
    post_id INTEGER,
    term_id INTEGER 
);

-- Index: idx_postId_termId
CREATE UNIQUE INDEX idx_postId_termId ON post_terms ( 
    post_id,
    term_id 
);


-- Index: idx_postPtms_postStat
CREATE INDEX idx_postPtms_postStat ON posts ( 
    post_ptms,
    post_stat 
);


-- Index: idx_postPtms_postStat_postRank
CREATE INDEX idx_postPtms_postStat_postRank ON posts ( 
    post_ptms,
    post_stat,
    post_rank 
);


-- Index: idx_postPtms_postStat_postRemc
CREATE INDEX idx_postPtms_postStat_postRemc ON posts ( 
    post_ptms,
    post_stat,
    post_remc 
);

