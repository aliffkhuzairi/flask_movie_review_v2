from flask import Blueprint, render_template, redirect, request, session
from db import db_cursor
from utils import login_required

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
@login_required
def global_search():
    query = request.args.get('q', "").strip()
    result_type = request.args.get('type', 'all').strip()

    allowed_type = {"all", "movies", "people"}

    if result_type not in allowed_type:
        result_type = "all"

    search_pattern = f"%{query}%"

    movies = []
    users = []

    if query:
        with db_cursor() as cur:
            if result_type in {"all", "movies"}:
                cur.execute("""
                    select id, title, director, genre, rel_date, poster, poster_url
                    from movies
                    where title ilike %s or director ilike %s or genre ilike %s
                    order by title asc
                        limit 10;
                """, (search_pattern, search_pattern, search_pattern))

                movies = cur.fetchall()

            if result_type in {"all", "people"}:
                cur.execute("""
                    select u.id, u.role, ui.name, ui.avatar
                    from users u
                    join user_info ui on u.id = ui.id
                    where u.id ilike %s or ui.name ilike %s
                    order by u.id asc
                    limit 10;
                """,(search_pattern, search_pattern))

                users = cur.fetchall()


    return render_template('search.html',
                           query=query,
                           result_type=result_type,
                           movies=movies,
                           users=users,
                           user_id=session.get('user_id'))