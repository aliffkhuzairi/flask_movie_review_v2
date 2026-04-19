from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
app = Flask(__name__)
app.secret_key = "dev_secret_key"

def get_db_connection():
    return psycopg2.connect(
        dbname='term_project',
        user='postgres',
        password='@100pluS',
        host='localhost',
        port='5432'
    )

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    user_id = request.form.get('user_id').strip()
    password = request.form.get('password').strip()
    action = request.form.get('action').strip()

    if not user_id or not password:
        return render_template('login.html', message="ID and password are required.")

    conn = get_db_connection()
    cur = conn.cursor()

    if action == "signup":
        try:
            cur.execute(
                "insert into users(id, password, role) values(%s, %s, %s)",
                (user_id, password, "user")
            )
            cur.execute(
                "insert into user_info(id, reg_date) values(%s, now());",
                (user_id,)
            )
            conn.commit()
            cur.close()
            conn.close()
            return render_template('login.html', message="Sign up successful. Please sign in.")

        except:
            conn.rollback()
            cur.close()
            conn.close()
            return render_template('login.html', message="Sign up failed. ID may already exists.")

    elif action == "signin":
        cur.execute("""
            select id, role from users where id = %s and password = %s;
        """, (user_id, password)
        )
        user = cur.fetchone()
        print(user)
        cur.close()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['role'] = user[1]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message="Invalid ID or password")

    cur.close()
    conn.close()
    return render_template('login.html', message="Invalid action")
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    conn = get_db_connection()
    cur = conn.cursor()

    movie_sort = request.args.get('movie_sort', 'latest')
    review_sort = request.args.get('review_sort', 'latest')

    # Movies sorting
    if movie_sort == "latest":
        cur.execute("""
            select id, title, director, genre, rel_date
            from movies
            order by rel_date desc;
        """)
    elif movie_sort == "genre":
        cur.execute("""
            select id, title, director, genre, rel_date
            from movies
                order by genre desc;
        """)

    movies = cur.fetchall()

    if review_sort == "latest":
        cur.execute("""
            select r.ratings, r.uid, m.title, r.review, r.rev_time
            from reviews r
            join movies m on r.mid = m.id
            order by r.rev_time desc;
        """)
    elif review_sort == "title":
        cur.execute("""
            select r.ratings, r.uid, m.title, r.review, r.rev_time
            from reviews r
            join movies m on r.mid = m.id
            order by m.title desc;
        """)

    reviews = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("home.html", movies=movies, reviews=reviews, user_id=session['user_id'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)