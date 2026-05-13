import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Parse the database URL
# DATABASE_URL=mysql+pymysql://root:Katalaluanadmin@localhost:3306/ajiqhords_db
db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("DATABASE_URL not found in .env")
    exit(1)

# Basic parsing for mysql+pymysql://user:password@host:port/dbname
try:
    parts = db_url.split("://")[1]
    user_pass, host_port_db = parts.split("@")
    user, password = user_pass.split(":")
    host_port, dbname = host_port_db.split("/")
    host, port = host_port.split(":")
    port = int(port)
except Exception as e:
    print(f"Error parsing database URL: {e}")
    exit(1)

def seed_songs():
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=dbname,
        port=port
    )

    try:
        with connection.cursor() as cursor:
            # Check if songs already exist to avoid duplicates if rerun
            songs_to_add = [
                # Anime
                ("Unravel", "TK from凛として時雨", "Anime", "Bm", "Hard", "C G Am Em\n[Intro]\nOshiete oshiete yo sono shikumi wo\n..."),
                ("Gurenge", "LiSA", "Anime", "Em", "Medium", "Em C D G\n[Intro]\nTsuyoku nareru riyuu wo shitta\n..."),
                
                # Raya
                ("Suasana Hari Raya", "Anuar & Elina", "Raya", "C", "Easy", "C F G C\nBerlalulah sudah ramadan mulia\n..."),
                ("Balik Kampung", "Sudirman", "Raya", "G", "Medium", "G D C G\nPerjalanan jauh tak ku rasa\n..."),
                
                # Rock Kapak
                ("Suci Dalam Debu", "Iklim", "Rock Kapak", "Am", "Medium", "Am Dm G C\nEngkau bagai air yang jernih\n..."),
                ("Isabella", "Search", "Rock Kapak", "Em", "Medium", "Em Am D G\nIsabella adalah kisah cinta dua dunia\n...")
            ]

            sql = "INSERT INTO songs (title, artist, playlist, original_key, difficulty, content) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, songs_to_add)
        
        connection.commit()
        print(f"Successfully seeded {len(songs_to_add)} songs.")
    finally:
        connection.close()

if __name__ == "__main__":
    seed_songs()
