create_query = """
    CREATE TABLE
    IF NOT EXISTS
    `user_info`
    (
        `id` varchar(32) primary key,
        `password` varchar(32) not null,
        `name` varchar(16)
    )
"""

login_query = """
    SELECT * FROM
    `user_info`
    WHERE `id` = %s AND `password` = %s
"""

signup_query = """
    INSERT INTO
    `user_info`
    VALUES (%s, %s, %s)
"""

check_query = """
    SELECT * FROM
    `user_info`
    WHERE `id` = %s
"""