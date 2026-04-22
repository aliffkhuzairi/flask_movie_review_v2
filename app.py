from encodings import cp437

from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2, re
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
    user_id = request.form.get('user_id', '').strip()
    password = request.form.get('password', '').strip()

    if not user_id or not password:
        flash("ID and password are required.")
        return render_template('login.html')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        select id, role 
        from users 
        where id = %s and password = %s;
    """, (user_id, password)
    )

    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        session['user_id'] = user[0]
        session['user_role'] = user[1]
        return redirect(url_for('home'))

    flash("ID or password are invalid.")
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    user_id = request.form.get('user_id', '').strip()
    password = request.form.get('password', '').strip()

    if not user_id or not password:
        flash("ID and password are required.")
        return render_template('signup.html')

    conn = get_db_connection()
    cur = conn.cursor()

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

        flash("Account created. Please sign in.")
        return redirect(url_for('index'))

    except:
        conn.rollback()
        cur.close()
        conn.close()
        flash("Sign up failed. ID may already exists.")
        return render_template('signup.html')


@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    conn = get_db_connection()
    cur = conn.cursor()

    movie_sort = request.args.get('movie_sort', 'latest')
    movie_sort_dir = request.args.get('movie_sort_dir', 'desc').lower()

    review_sort = request.args.get('review_sort', 'latest')
    review_sort_dir = request.args.get('review_sort_dir', 'desc').lower()

    if movie_sort_dir not in ['asc', 'desc']:
        movie_sort_dir = 'desc'
    if review_sort_dir not in ['asc', 'desc']:
        review_sort_dir = 'desc'

    # Movies sorting
    if movie_sort == "latest":
        cur.execute(f"""
            select id, title, director, genre, rel_date
            from movies
            order by rel_date {movie_sort_dir};
        """)
    elif movie_sort == "genre":
        cur.execute(f"""
            select id, title, director, genre, rel_date
            from movies
            order by genre {movie_sort_dir};
        """)

    else:
        cur.execute("""
            select id, title, director, genre, rel_date
            from movies
            order by rel_date desc;
        """)

    movies = cur.fetchall()

    # Review sort
    if review_sort == "latest":
        cur.execute(f"""
            select r.ratings, r.uid, m.title, r.review, r.rev_time
            from reviews r
            join movies m on r.mid = m.id
            where r.uid not in (
                select opid from ties where id = %s and tie = 'mute'
                )
            order by r.rev_time {review_sort_dir};
        """,(session['user_id'],))
    elif review_sort == "title":
        cur.execute(f"""
            select r.ratings, r.uid, m.title, r.review, r.rev_time
            from reviews r
            join movies m on r.mid = m.id
            where r.uid not in (
                select opid from ties where id = %s and tie = 'mute'
                )
            order by m.title {review_sort_dir};
        """,(session['user_id'],))

    else:
        cur.execute("""
            select r.ratings, r.uid, m.title, r.review, r.rev_time
            from reviews r
                     join movies m on r.mid = m.id
            where r.uid not in (select opid
                                from ties
                                where id = %s and tie = 'mute')
            order by r.rev_time desc;
        """, (session['user_id'],))

    reviews = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "home.html",
        movies=movies,
        reviews=reviews,
        user_id=session['user_id'],
        movie_sort=movie_sort,
        movie_sort_dir=movie_sort_dir,
        review_sort=review_sort,
        review_sort_dir=review_sort_dir
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/movie/<movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        review = request.form.get('review', '').strip()
        rating = request.form.get('rating', '').strip()

        if review and rating.isdigit():
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

                flash("Review updated!")

            else:
                cur.execute("""
                    insert into reviews(mid, uid, ratings, review, rev_time)
                    values(%s, %s, %s, %s, now());
                """,(movie_id, session['user_id'], rating, review))

                flash("Review added!")
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
        where r.mid = %s and r.uid not in (
            select opid from ties where id = %s and tie = 'mute' 
            )
        order by r.rev_time desc
    """, (movie_id, session['user_id'],))

    reviews = cur.fetchall()

    cur.execute("""
        select trunc(avg(r.ratings), 2) 
        from reviews r 
        where r.mid = %s and r.uid not in (
            select opid from ties where id = %s and tie = 'mute'
            )
    """, (movie_id, session['user_id'],))

    avg_rating = cur.fetchone()[0]

    cur.execute("""
        select ratings, review
        from reviews
        where mid = %s and uid = %s;
    """,(movie_id, session['user_id'],))

    user_review = cur.fetchone()
    cur.close()
    conn.close()


    return render_template("movie.html", movie=movie, reviews=reviews, avg_rating=avg_rating, user_review=user_review, user_id=session['user_id'])

@app.route('/user/<user_id>', methods=['GET', 'POST'])
def user_detail(user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    current_user_role = session.get('user_role')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
                select u.id, u.role, ui.name, ui.email, ui.reg_date
                from users u
                         join user_info ui on u.id = ui.id
                where u.id = %s;
                """, (user_id,))

    user_info = cur.fetchone()

    if user_info is None:
        cur.close()
        conn.close()
        return "User not found", 404

    cur.execute("""
                select m.id, m.title, r.ratings, r.review, r.rev_time
                from reviews r
                join movies m on r.mid = m.id
                where r.uid = %s
                order by r.rev_time desc;
                """, (user_id,))

    user_reviews = cur.fetchall()

    relationship = None

    is_self = (user_id == session['user_id'])
    is_admin_profile = (user_info[1] == 'admin')
    is_current_user_admin = (current_user_role == 'admin')
    followed_users = []
    muted_users = []
    if is_self:
        cur.execute("""
            select ui.id, ui.name 
            from ties t 
            join user_info ui on t.opid = ui.id
            where t.id = %s and t.tie = 'follow'
            order by ui.id;
        """,(user_id,))

        followed_users = cur.fetchall()

        cur.execute("""
                    select ui.id, ui.name
                    from ties t
                    join user_info ui on t.opid = ui.id
                    where t.id = %s
                    and t.tie = 'mute'
                    order by ui.id;
        """, (user_id,))

        muted_users = cur.fetchall()

    elif not is_self and not is_admin_profile and not is_current_user_admin:
        cur.execute("""
            select tie
            from ties
            where id = %s and opid = %s;
        """,(session['user_id'], user_id))

        relation_row = cur.fetchone()

        if relation_row:
            relationship =  relation_row[0]

    cur.close()
    conn.close()
    clear_form = session.pop('clear_form', False)

    return render_template("user_info.html",
                           user_info=user_info,
                           user_reviews=user_reviews,
                           user_id=session['user_id'],
                           is_self=is_self,
                           is_admin_profile=is_admin_profile,
                           is_current_user_admin=is_current_user_admin,
                           relationship=relationship,
                           followed_users=followed_users,
                           muted_users=muted_users,
                           clear_form=clear_form)

@app.route('/user/<user_id>/edit', methods=['POST'])
def edit_user_profile(user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    if session['user_id'] != user_id:
        return redirect(url_for('user_detail', user_id=user_id))

    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()

    if not name and not email:
        flash('Please enter at least one field to update.')
        return redirect(url_for('user_detail', user_id=user_id))

    if name and len(name) < 2:
        flash('Name must be at least 2 characters.')
        return redirect(url_for('user_detail', user_id=user_id))

    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        flash('Please enter a valid email address.')
        return redirect(url_for('user_detail', user_id=user_id))


    conn = get_db_connection()
    cur = conn.cursor()

    if name:
        cur.execute("""
                    update user_info
                    set name  = %s
                    where id = %s;
                    """, (name, user_id))
    if email:
        cur.execute("""
                    update user_info
                    set email = %s
                    where id = %s;
                    """, (email, user_id))


    conn.commit()
    cur.close()
    conn.close()
    flash('Profile updated successfully.')
    session['clear_form'] = True
    return redirect(url_for('user_detail', user_id=user_id))

@app.route('/follow/<target_user_id>', methods=['POST'])
def follow_user(target_user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    if session.get('user_role') == 'admin':
        return redirect(url_for('user_detail', user_id=target_user_id))

    current_user_id = session['user_id']

    if current_user_id == target_user_id:
        return redirect(url_for('user_detail', user_id=target_user_id))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        select role from users where id = %s;
    """,(target_user_id,))
    target_user = cur.fetchone()

    if target_user is None:
        cur.close()
        conn.close()
        return "User not found", 404

    if target_user[0] == "admin":
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

@app.route('/mute/<target_user_id>', methods=['POST'])
def mute_user(target_user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    if session.get('user_role') == 'admin':
        return redirect(url_for('user_detail', user_id=target_user_id))

    current_user_id = session['user_id']

    if current_user_id == target_user_id:
        return redirect(url_for('user_detail', user_id=target_user_id))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
                select role
                from users
                where id = %s;
                """, (target_user_id,))
    target_user = cur.fetchone()

    if target_user is None:
        cur.close()
        conn.close()
        return "User not found", 404

    if target_user[0] == "admin":
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


@app.route('/unmute/<target_user_id>', methods=['POST'])
def unmute_user(target_user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        delete from ties
        where id = %s and opid = %s and tie = 'mute';
    """,(session['user_id'], target_user_id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('user_detail', user_id=target_user_id))

@app.route('/add-movie', methods=['POST'])
def add_movie():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    if session.get('user_role') != 'admin':
        return redirect(url_for('home'))

    movie_id = request.form.get('movie_id', '').strip()
    title = request.form.get('movie_title', '').strip()
    director = request.form.get('director', '').strip()
    genre = request.form.get('genre', '').strip()
    rel_date = request.form.get('rel_date', '').strip()

    if not movie_id or not title or not director or not genre or not rel_date:
        flash("All fields are required.")
        return redirect(url_for('user_detail', user_id=session['user_id']))

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            insert into movies(id, title, director, genre, rel_date)
            values(%s, %s, %s, %s, %s)
        """,(movie_id, title, director, genre, rel_date))

        conn.commit()
        flash("Movie added successfully!")

    except Exception as e:
        conn.rollback()
        flash(f"Failed: {e}")

    cur.close()
    conn.close()

    return redirect(url_for('user_detail', user_id=session['user_id']))

@app.route('/review/<movie_id>/delete', methods=['POST'])
def delete_review(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        delete from reviews where mid = %s and uid = %s;
    """,(movie_id, session['user_id']))

    conn.commit()
    cur.close()
    conn.close()

    flash("Review deleted successfully.")
    return redirect(url_for('user_detail', user_id=session['user_id']))
if __name__ == '__main__':
    app.run(debug=True)