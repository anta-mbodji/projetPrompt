import psycopg2
from faker import Faker

def connect():
    try:
        conn = psycopg2.connect(
            database="prompt_projet",
            user="postgres",
            password="improvise",
            host="localhost"
        )
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

def populate_notes(conn, num_notes=97):
    fake = Faker()
    notes = []

    # Assuming you have at least 100 prompts and 100 users in your database
    for _ in range(num_notes):
        id_note = _
        id_prompt = fake.random_int(min=3, max=97)  # Adjust max according to the number of prompts
        id_user = fake.random_int(min=3, max=97)    # Adjust max according to the number of users
        valeur = fake.random_int(min=-10, max=10)
        notes.append((id_note, id_user, valeur, id_prompt))

    query = "INSERT INTO note (id_note,  id_user, valeur, id_prompt) OVERRIDING SYSTEM VALUE VALUES (%s,%s, %s, %s)"
    try:
        cur = conn.cursor()
        cur.executemany(query, notes)
        conn.commit()
        cur.close()
        print(f"{num_notes} notes populated successfully")
    except Exception as e:
        print(f"Error while populating notes: {e}")
        conn.rollback()

def main():
    conn = connect()
    if conn:
        populate_notes(conn, num_notes=97)
        conn.close()

if __name__ == "__main__":
    main()
