use stats;
create table users(
    roll_number VARCHAR(60) PRIMARY KEY NOT NULL,
    pass CHAR(64) NOT NULL,    
    cf_handle VARCHAR(60) DEFAULT "",
    cc_handle VARCHAR(60) DEFAULT "",
    hr_handle VARCHAR(60) DEFAULT "",
    he_handle VARCHAR(60) DEFAULT "",
    ib_handle VARCHAR(60) DEFAULT "",
    lc_handle VARCHAR(60) DEFAULT "",
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
create table tags(
    id INT PRIMARY KEY NOT NULL,
    roll_number VARCHAR(60),
    
)