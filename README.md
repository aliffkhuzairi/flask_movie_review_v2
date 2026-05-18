# MovieReview — Flask Movie Review Web App

MovieReview is a full-stack Flask web app where users can browse movies, post reviews, manage their profile, and interact with other users through follow and mute features.
 
The project focuses on backend CRUD, PostgreSQL relationships, authentication, responsive UI, and user-focused features.
 
**Live demo:** https://flask-movie-review-v2.onrender.com
---

### Home Page
![Home Page](screenshots/homepage.png)
![Home Page](screenshots/homepage2.png)

### All Movies Page
![All Movies Page](screenshots/movie_list_page.png)

### Movie Details Page
![Movie Details Page](screenshots/movie_detail.png)

### User Profile Page
![User Profile Page](screenshots/user_profile_page.png)
![User Profile Page](screenshots/user_profile_page2.png)
![User Profile Page](screenshots/visit_user.png)

### Admin Panel
![Admin Panel](screenshots/admin_panel.png)
![Admin Panel](screenshots/admin_panel2.png)

---

## Features

### Authentication
- User sign up and login
- Password hashing for new accounts
- Session-based authentication
- Protected route for logged-in users
- Role-based admin access

### Movies
- Browse all movies with poster cards
- Search movies by title, director, or genre
- Sort movies by latest, title, and genre
- Paginated movie list
- Result summary such as `Showing 1 – 15 of 21 movies`
- Movie posters seeded using the OMDB API
- Movie trailers embedded via YouTube
- Admin can add new movies with poster upload, poster URL, and trailer URL
- Admin can update movie details including poster and trailer
- Admin can delete movies
- Duplicate movie handling
- Live poster preview in admin add movie form
- Average rating displayed on movie cards

### Reviews
- Add, update, and delete reviews
- Star-based rating input UI
- Rating validation from 1 to 5
- Average rating display on movie detail pages
- Vertical bar rating breakdown chart for each movie
- Relative time display such as `5m`, `1h`, and `2d`
- Sort reviews by latest, highest rating, and lowest rating
- Paginated reviews on user profile pages
- Paginated reviews on movie detail pages
- Review count summary such as `Showing 1 – 5 of 12 reviews`
- Movie poster thumbnails on review cards

### Home Page
- Latest movie cards with poster backgrounds and average ratings
- Recent Reviews feed with movie poster thumbnails
- Top Rated Movies section ranked by community ratings
- Most Active Reviewers section based on review count
- Muted users excluded from all home page feeds

### Global Search
- Header search for movies and users
- Search result page with filter tabs for all results, movies, and people
- Movie search results include poster thumbnails
- People search results include user avatars
- Search layout is responsive across desktop, tablet, and mobile

### User Profiles
- View user profile information
- Profile hero with avatar, display name, and stats in a single card
- Profile stats including total reviews, average rating given, top genre, and last review date
- Profile tabs for overview, reviews, connections, and account settings
- Recent Activity section showing last 4 reviewed movies
- Upload and crop profile avatar using Cropper.js
- Remove uploaded avatar and fall back to default icon avatar
- Edit name and email
- Change password from account settings
- Delete own account with double confirmation
- Account deletion removes profile data, reviews, avatar, and social connections
- View review history with movie posters
- Sort user reviews by latest, highest, and lowest
- View followed and muted users in connections tab


### Social Features
- Follow users
- Mute users to hide their reviews
- Prevent users from following or muting themselves
- Prevent follow/mute actions on admin profiles
- Hide reviews from muted users on home and movie detail pages
- Muted users list is private to the current user

### Admin Features
- Add new movies with poster and trailer
- Live poster preview when entering URL or uploading file
- Update existing movies including poster and trailer
- Delete movies and related reviews
- Admin-only role checks
- Admin profile protection from follow/mute actions

### UI/UX
- Dark theme with dark navy color palette
- Responsive layout for desktop, tablet, and mobile
- Mobile navigation toggle
- Header search toggle
- Font Awesome icons
- Poster-style movie cards with gradient overlay
- Movie detail page with trailer embed and rating breakdown
- Global review card component reused across all pages
- Clickable review cards while keeping inner links and buttons usable
- Password visibility toggle for login, signup, and password change forms
- Custom confirmation modals instead of browser default confirmation dialogs
- Anchor navigation for review sorting
- Reusable pagination styling
- Subtle delete actions with hover-reveal danger color

---

## Tech Stack

### Backend
- Python (Flask)
- PostgreSQL
- psycopg2
- Werkzeug password hashing
- Gunicorn (production server)

### Frontend
- HTML5
- CSS3 (Flexbox + responsive design)
- JavaScript (vanilla)
- Font Awesome (icons)
- Cropper.js for avatar cropping

### Cloud & Deployment
- Render (app hosting)
- Neon (managed PostgreSQL)
- AWS S3 (avatar and movie poster storage)

### External APIs
- OMDB API for movie poster seeding
- YouTube embed for movie trailers

---

## Database

The app uses PostgreSQL with relational tables for:

- users
- user_info
- movies
- reviews
- ties

Key relationships:
- A user can review a movie once.
- A user can follow or mute another user.
- Muted users’ reviews are hidden from the current user.
- Movies use auto-generated integer IDs.

---

## Project Structure

```bash
.
├── app.py
├── db.py
├── utils.py
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── movie_routes.py
│   ├── search_routes.py
│   └── user_routes.py
├── templates/
│   ├── partials/
│   │   └── header.html
│   ├── macros.html
│   ├── home.html
│   ├── movies.html
│   ├── movie.html
│   ├── search.html
│   ├── user_info.html
│   ├── login.html
│   └── signup.html
├── static/
│   ├── style.css
│   ├── script.js
│   └── uploads/
│       ├── avatars/
│       │   └── .gitkeep
│       └── posters/
│           └── .gitkeep
├── screenshots/
├── movie_db.sql
├── .gitignore
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/aliffkhuzairi/flask_movie_review_v2.git
cd flask_movie_review_v2
```

---

### 2. Create virtual environment

```bash
python -m venv .venv
```

Activate:

**Windows**

```bash
.venv\Scripts\activate
```

**Mac/Linux**

```bash
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup PostgreSQL

Create database:

```bash
CREATE DATABASE movie_review;
```

Import schema:

```bash
psql -U postgres -d movie_review -f movie_db.sql
```

---

### 5. Configure environment variable

Create a `.env` file in the project root:
 
```env
DATABASE_NAME=movie_review
DATABASE_USER=postgres
DATABASE_PASSWORD=yourpassword
DATABASE_HOST=localhost
DATABASE_PORT=5432
FLASK_SECRET_KEY=your_secret_key
 
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your_bucket_name
AWS_REGION=your_region
```

AWS S3 credentials are required for avatar and movie poster uploads. Without them, file uploads will fail.

---

### 6. Run the application

```bash
python app.py
```

Open in browser:

```bash
http://127.0.0.1:5000
```

---

## Test Accounts
 
| Username | Password | Role  |
|----------|----------|-------|
| admin    | 00000000 | admin |
| andy     | 1234     | user  |
| marco    | 1234     | user  |

---

## Responsive Design

- Desktop → multi-column layout
- Tablet → 2-column layout
- Mobile → stacked layout
- Navigation menu with toggle icon
- Review and movie cards resize across screen widths

---

## Security Notes
 
- Database credentials are loaded from environment variables
- Passwords are hashed using Werkzeug scrypt
- SQL queries use parameterized values
- Dynamic sort values are restricted through allowlists
- Admin-only features are protected by role checks
- User actions are guarded with session checks
- Delete actions use POST requests instead of GET links
- Uploaded avatar files are ignored by Git and stored locally during development
- Avatar uploads are processed as cropped image data before saving
- Password change requires the current password
- Account deletion requires password confirmation and `DELETE` text confirmation
- Admin accounts cannot be deleted from the settings page
- Destructive actions use custom confirmation modals before submitting POST requests
- SSL is enforced for cloud database connections

---

## What I Learned
 
- Building Flask routes with blueprints
- Registering route modules through `routes/__init__.py`
- Handling authentication and user sessions
- Designing PostgreSQL relationships and constraints
- Writing SQL queries with joins, filters, sorting, pagination, and NOT EXISTS
- Implementing role-based access for admin features
- Building reusable Jinja2 macros and template components
- Building interactive form inputs with vanilla JavaScript
- Refactoring pagination logic into helper functions
- Improving mobile layout with responsive CSS
- Managing UI growth through CSS restructuring
- Handling account deletion with related database cleanup
- Storing and serving user-uploaded files via AWS S3
- Deploying a Flask app to Render with Gunicorn
- Connecting a production app to a cloud PostgreSQL database (Neon)
- Managing environment-specific configuration (local vs production)
- Debugging encoding issues between local PostgreSQL and cloud imports
- Building modal confirmation flows with JavaScript
- Creating reusable custom confirmation modals
- Replacing inline click handlers with JavaScript event listeners
- Managing clickable cards with overlay links while preserving inner button and link behavior
- Adding password visibility toggles for authentication forms
- Integrating external APIs (OMDB) for data seeding
- Embedding YouTube trailers via iframe
- Building a global CSS component system for review cards
- Using CSS Grid and Flexbox together for complex layouts
- Implementing live image preview with FileReader API

---

## Future Improvements

- Add automated tests
- Add CSRF protection for forms
- Add movie synopsis or description field
- Add user watchlist feature

---

## Author

**Aliff Khuzairi bin Jamaludin**  
Computer Science & Engineering Graduate  
Korea University, Seoul

---

## License

This project is for educational purposes.
