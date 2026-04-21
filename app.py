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
            print(redirect(url_for('home')))
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

@app.route('/movie/movie_id=<movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        review = request.form.get('review', '').strip()
        rating = request.form.get('rating', '').strip()

        if review and rating:
            cur.execute("""
                select 1 from reviews where mid = %s and uid = %s;
            """,(movie_id, session['user_id']))

            existing_review = cur.fetchone()

            if existing_review:
                cur.execute("""
                    update reviews
                    set ratings = %s, review = %s, rev_time = now()
                    where mid = %s and uid = %s;
                """, (rating, review, movie_id, session['user_id']))

            else:
                cur.execute("""
                    insert into reviews(mid, uid, ratings, review, rev_time)
                    values(%s, %s, %s, %s, now());
                """,(movie_id, session['user_id'], rating, review))

            conn.commit()

    cur.execute("""
        select id, title, director, genre, rel_date
        from movies
        where id = %s
    """, (movie_id,))

    movie = cur.fetchone()

    cur.execute("""
        select r.ratings, r.uid, r.review, r.rev_time
        from reviews r 
        where r.mid = %s
        order by r.rev_time desc
    """, (movie_id,))

    reviews = cur.fetchall()

    cur.execute("""
        select round(avg(r.ratings), 2) from reviews r where r.mid = %s
    """, (movie_id,))

    avg_rating = cur.fetchone()[0]

    cur.close()
    conn.close()

    return render_template("movie.html", movie=movie, reviews=reviews, avg_rating=avg_rating, user_id=session['user_id'])

@app.route('/user/<user_id>')
def user_detail(user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    is_self = (user_id == session['user_id'])
    conn = get_db_connection()
    cur = conn.cursor()

    relationship = None

    if not is_self:
        cur.execute("""
            select tie
            from ties
            where id = %s and opid = %s;
        """,(session['user_id'], user_id))

        relation_row = cur.fetchone()

        if  relation_row:
            relationship =  relation_row[0]

    cur.execute("""
        select * from user_info where id = %s;
    """, (user_id,))

    user_info = cur.fetchone()

    if user_info is None:
        cur.close()
        conn.close()
        return "User not found", 404

    cur.execute("""
         select m.title, r.ratings, r.review, r.rev_time 
         from reviews r 
         join movies m on r.mid = m.id 
         where r.uid = %s
         order by r.rev_time desc;
    """,(user_id,))

    user_reviews = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("user_info.html", user_info=user_info, user_review=user_reviews, user_id=session['user_id'], is_self=is_self, relationship=relationship)

@app.route('/follow/<target_user_id>', methods=['POST'])
def follow_user(target_user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    current_user_id = session['user_id']

    if current_user_id == target_user_id:
        return redirect(url_for('user_detail', user_id=target_user_id))

    conn = get_db_connection()
    cur = conn.cursor()

    if target_user_id == "admin":
        cur.close()
        conn.close()
        return redirect(url_for('user_detail', user_id=target_user_id))

    cur.execute("""
        delete from ties
        where id = %s and opid = %s and tie = 'mute';
    """, (current_user_id, target_user_id))

    cur.execute("""
        select 1 from ties
        where id = %s and opid = %s and tie = 'follow'
    """,(current_user_id, target_user_id))

    existing_follow = cur.fetchone()

    if not existing_follow:
        cur.execute("""
            insert into ties(id, opid, tie)
            values(%s, %s, 'follow');
        """, (current_user_id, target_user_id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('user_detail', user_id=target_user_id))

@app.route('/unfollow/<target_user_id>', methods=['POST'])
def unfollow_user(target_user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        delete from ties
        where id = %s and opid = %s and tie = 'follow';
    """,(session['user_id'], target_user_id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('user_detail', user_id=target_user_id))
@app.route('/mute/<target_user_id>', methods=['POST'])
def mute_user(target_user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    current_user_id = session['user_id']

    if current_user_id == target_user_id:
        return redirect(url_for('user_detail', user_id=target_user_id))

    conn = get_db_connection()
    cur = conn.cursor()

    if target_user_id == "admin":
        cur.close()
        conn.close()
        return redirect(url_for('user_detail', user_id=target_user_id))

    cur.execute("""
                delete
                from ties
                where id = %s
                  and opid = %s
                  and tie = 'follow';
                """, (current_user_id, target_user_id))

    cur.execute("""
                select 1
                from ties
                where id = %s
                  and opid = %s
                  and tie = 'mute'
                """, (current_user_id, target_user_id))

    existing_follow = cur.fetchone()

    if not existing_follow:
        cur.execute("""
                    insert into ties(id, opid, tie)
                    values (%s, %s, 'mute');
                    """, (current_user_id, target_user_id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('user_detail', user_id=target_user_id))

if __name__ == '__main__':
    app.run(debug=True)