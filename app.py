from flask import Flask
import psycopg2
app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname='term_project',
        user='postgres',
        password='@100pluS',
        host='localhost',
        port='5432'
    )
@app.route('/')
def home():
    return "Flask is working"

@app.route("/test_db")
def test_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, director, genre, rel_date FROM movies ORDER BY rel_date DESC;")
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return "<br>".join([f"{m[0]} | {m[1]} | {m[2]} | {m[3]} | {m[4]}" for m in movies])

if __name__ == '__main__':
    app.run(debug=True)