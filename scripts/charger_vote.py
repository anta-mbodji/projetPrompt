import psycopg2
from faker import Faker 



def connect():
    try:
        conn = psycopg2.connect(
            database = "prompt_projet",
            user = "postgres",
            password = "improvise",
            host = "localhost",
    
        )
        return conn 
    except Exception as e:
        print(f"Error: {e}")
        return None
    



def populate_vote(conn , num_vote= 100):
    fake = Faker()
    votes = []


    cur = conn.cursor()


    cur.execute("SELECT id_user FROM utilisateur")
    user_ids = [row[0] for row in cur.fetchall()]
    
    cur.execute("SELECT id_prompt FROM prompt")
    prompt_ids = [row[0] for row in cur.fetchall()]
    # print(prompt_ids)


    for _ in range(num_vote):
        id_vote = _  
        valeur_vote = fake.random_int(min=-10,max=10)
        id_prompt= fake.random.choice(prompt_ids)
        id_user= fake.random.choice(user_ids)
        votes.append((id_vote, valeur_vote, id_prompt, id_user))

    query = "INSERT INTO vote (id_vote, valeur_vote, id_prompt, id_user) VALUES (%s, %s, %s, %s)"
    cur.executemany(query, votes)
    conn.commit()
    cur.close()
    print(f"{num_vote} votes populated successfully")


def main ():
    conn = connect()
    if conn:
        populate_vote(conn, num_vote= 100)
        conn.close()

if __name__ == "__main__":
    main()