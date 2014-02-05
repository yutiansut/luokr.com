
-- Table: users
CREATE TABLE users ( 
    user_id   INTEGER         PRIMARY KEY AUTOINCREMENT,
    user_name VARCHAR( 80 )   NOT NULL UNIQUE,
    user_sign VARCHAR( 80 )   NOT NULL UNIQUE,
    user_salt CHAR( 8 )       NOT NULL,
    user_pswd CHAR( 32 )      NOT NULL,
    user_mail VARCHAR( 500 ),
    user_ctms INT( 10 ),
    user_utms INT( 10 ) 
);

INSERT INTO [users] ([user_id], [user_sign], [user_name], [user_salt], [user_pswd], [user_mail], [user_ctms], [user_utms]) VALUES (1, 'admin', 'Admin', 'asdflkjh', 'b6ce17f5578131e2997ccfb99dcc3500', 'admin@luokr.com', 1374486660, 1374765138);
