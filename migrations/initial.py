"""
    This file contains commands for creating/dropping database tables
"""
drop_tables_commands = (
    """
    DROP TABLE IF EXISTS users CASCADE
    """,
    """
    DROP TABLE IF EXISTS parcels CASCADE
    """,
)

drop_users = (
    """
    DROP TABLE IF EXISTS users CASCADE
    """,
)

drop_parcels = (
    """
    DROP TABLE IF EXISTS parcels CASCADE
    """,
)

create_tables_commands = (
    """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        firstname VARCHAR(255) NOT NULL,
        lastname VARCHAR(255) NOT NULL,
        othernames VARCHAR(255),
        email VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(500) NOT NULL,
        registered timestamp with time zone DEFAULT now(),
        isAdmin boolean DEFAULT FALSE,
        updatedOn timestamp with time zone
    )
    """
    ,
    """
    CREATE TABLE IF NOT EXISTS parcels(
        id integer PRIMARY KEY,
        placedBy INTEGER NOT NULL,
        weightmetric INTEGER NOT NULL,
        sentOn timestamp with time zone,
        deliveredOn timestamp with time zone,
        status VARCHAR(15) NOT NULL,
        "from" VARCHAR(255) NOT NULL,
        "to" VARCHAR(255) NOT NULL,
        currentlocation VARCHAR(255) NOT NULL,
        isCanceled boolean NOT NULL,
        updatedOn timestamp with time zone,
        FOREIGN KEY (placedBy)
            REFERENCES users (id)
            ON UPDATE CASCADE ON DELETE CASCADE
    )
    """,
)

migrations = create_tables_commands