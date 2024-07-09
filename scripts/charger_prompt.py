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
    


def populate_prompts(conn, num_prompt=100):
    fake = Faker()
    prompt = []
    statuses = ['À supprimer','Rappel','À revoir','Activé','En attente ']

    for id_prompt in range(num_prompt):
        content = fake.sentence()
        prix = fake.random.randint(500, 1000)
        note = fake.random.randint(-10 , 10)
        status = fake.random_element(statuses)
        prompt.append((id_prompt, content, prix, note, status))

    query = "INSERT INTO prompt (id_prompt, content, prix, note, status) VALUES (%s, %s, %s, %s, %s)"
    cur = conn.cursor()
    cur.executemany(query, prompt)
    conn.commit()
    cur.close()
    print(f"{num_prompt} prompts populated successfully")




def main():
    conn = connect()
    if conn:
        populate_prompts(conn, num_prompt=100)
        conn.close()

if __name__ == "__main__":
    main()
