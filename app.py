from flask import Flask, render_template
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
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
                select id, title, director, genre, rel_date
                from movies
                order by rel_date desc;
                """)
    movies = cur.fetchall()

    cur.execute("""
        select r.ratings. r.uid, m.title, r.review, r.rev_time
        form reviews r
        join movies m on r.mid = m.id
    """)
    reviews = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("home.html", movies=movies, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)