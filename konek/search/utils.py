import sqlite3


def search_database(database, query):
    connect = sqlite3.connect(
        '/home/joe/Projects/twitter-clone-v1/konek/twitterclone.db')
    cur = connect.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for tablerow in cur.fetchall():
        # finds all the tables in database
        table = tablerow[0]
        cur.execute(f"SELECT * FROM {table}")
        results = []
        for row in cur:
            for field in row:
                if query in str(field):
                    # TODO: need to get the row[0] name aka the column name of field
                    print(
                        f'found {query}: {field} in row {row[0]} inside the {table} table'
                    )
                    results.append(field)
        return results
