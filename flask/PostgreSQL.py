
DB_INIT_TABLE_EVENTS = ("""
        CREATE TABLE IF NOT EXISTS events (
            id BIGSERIAL PRIMARY KEY,
            object VARCHAR(255) NOT NULL,
            municipality VARCHAR(255) NOT NULL,
            event_name VARCHAR(255) UNIQUE NOT NULL,
            event_date VARCHAR(255) NOT NULL,
            event_address VARCHAR(255) NOT NULL
);
""")


DB_INSERT_TABLE_EVENTS = ("""
        INSERT INTO events(object, municipality, event_name,  event_date, event_address) 
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT (event_name) DO NOTHING
        RETURNING id;
""")
