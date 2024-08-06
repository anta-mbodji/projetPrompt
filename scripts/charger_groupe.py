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

def populate_users(conn, num_users=100):
    fake = Faker()
    users = []
    roles = ['admin', 'S_user', 'visiteur']
    
    for _ in range(num_users):
        if _ > 2:
            id_user = _
            nom = fake.name()
            email = fake.email()
            mot_de_pass = fake.password(length=10)
            role = fake.random.choice(roles)
            users.append((id_user, nom, email, mot_de_pass, role))
        else:
            continue

    query = "INSERT INTO utilisateur (id_user, nom, email, mot_de_pass, role) VALUES (%s, %s, %s, %s, %s)"
    cur = conn.cursor()
    cur.executemany(query, users)
    conn.commit()
    cur.close()
    print(f"{num_users} users populated successfully")

def populate_groups(conn, num_groups=10):
    fake = Faker()
    groups = []
    
    for _ in range(num_groups):
        id_groupe = _
        name_groupe = fake.company()
        nomb_membres = fake.random_int(min=1, max=50)
        groups.append((id_groupe, name_groupe, nomb_membres))

    query = "INSERT INTO groupe (id_groupe, name_groupe, nomb_membres) VALUES (%s, %s, %s)"
    cur = conn.cursor()
    cur.executemany(query, groups)
    conn.commit()
    cur.close()
    print(f"{num_groups} groups populated successfully")

def main():
    conn = connect()
    if conn:
        populate_users(conn, num_users=100)
        populate_groups(conn, num_groups=10)
        conn.close()

if __name__ == "__main__":
    main()
