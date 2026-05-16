-- ============================================================
-- SEED: Fake reviews for flask_movie_review_v2
-- All (mid, uid) pairs verified against existing reviews
-- Dates are after each movie's release date
-- ============================================================

-- INCEPTION (mid=7, release: 2010-07-16)
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(7, 'admin', 5, 'A masterpiece of storytelling and visual effects. Nolan at his absolute best. The dream-within-a-dream concept is executed flawlessly.', '2010-09-12 14:23:45.123456+00'),
(7, 'andy', 5, 'The rotating corridor fight scene alone is worth five stars. Mind-blowing cinema that rewards repeat viewings.', '2010-08-02 20:11:30.654321+00'),
(7, 'khuzairi', 4, 'Complex but deeply rewarding. Had to watch it twice to fully appreciate what Nolan was doing.', '2012-03-15 08:45:22.789012+00'),
(7, 'lisa', 4, 'Loved the concept but the ending is deliberately ambiguous. Still a must-watch for any film lover.', '2015-06-20 16:30:00.345678+00'),
(7, 'cai', 5, 'One of the most original films ever made. Absolutely gripping from the first frame to the last.', '2011-02-28 21:05:10.901234+00'),
(7, 'admin2', 3, 'Visually stunning but the plot gets too convoluted at times. Still an impressive achievement.', '2013-11-05 10:00:00.111111+00');

-- THE DARK KNIGHT (mid=11, release: 2008-07-18)
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(11, 'admin', 5, 'Heath Ledger''s Joker is one of the greatest villain performances in cinema history. A film that transcends its genre.', '2008-08-01 19:30:00.222222+00'),
(11, 'andy', 5, 'Not just a superhero film — a genuinely great crime thriller. Ledger is unforgettable. Nolan''s best work.', '2008-09-14 22:45:33.333333+00'),
(11, 'aliff', 5, 'Rewatched this for the tenth time and it still holds up perfectly. The interrogation scene is pure cinema.', '2020-04-10 14:20:00.444444+00'),
(11, 'lisa', 4, 'Brilliant film. Ledger deserved every award he received. Dark, intense, and completely gripping.', '2009-01-22 11:15:00.555555+00'),
(11, 'cai', 5, 'The interrogation scene between Batman and Joker is one of the best scenes ever filmed.', '2010-05-05 17:00:00.666666+00'),
(11, 'admin2', 4, 'A rare superhero film that transcends the genre entirely. Dark, intelligent, and brilliantly acted.', '2011-08-19 09:30:00.777777+00');

-- WHIPLASH (mid=14, release: 2014-10-10)
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(14, 'admin', 5, 'One of the most intense films I have ever seen. J.K. Simmons is terrifying and compelling in equal measure.', '2014-12-03 20:00:00.888888+00'),
(14, 'andy', 5, 'The final performance scene is one of the best endings in recent cinema. Absolutely electric.', '2015-02-14 18:30:00.999999+00'),
(14, 'khuzairi', 4, 'Intense and gripping. Makes you question what it truly takes to be great at something.', '2015-05-20 15:45:00.101010+00'),
(14, 'aliff', 5, 'Every scene with Fletcher is electric. An absolute masterclass in screen performance.', '2016-01-08 12:00:00.202020+00'),
(14, 'lisa', 4, 'Uncomfortable to watch at times, which is exactly the point. A powerful and important film.', '2015-08-30 21:15:00.303030+00'),
(14, 'cai', 3, 'Technically impressive but I found it hard to emotionally connect with the characters.', '2016-03-12 10:30:00.404040+00');

-- THE MATRIX (mid=15, release: 1999-03-31)
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(15, 'admin', 5, 'Revolutionary filmmaking. Changed action cinema forever. Still looks incredible more than two decades later.', '2000-01-15 14:00:00.505050+00'),
(15, 'andy', 5, 'The bullet-time sequences were groundbreaking. A genuine game-changer in the history of cinema.', '1999-06-20 19:45:00.606060+00'),
(15, 'khuzairi', 4, 'A brilliantly crafted sci-fi thriller. The philosophy running beneath the action adds real depth.', '2005-11-11 16:00:00.707070+00'),
(15, 'aliff', 5, 'Watched this as a kid and it blew my mind completely. Still holds up perfectly decades later.', '2019-07-04 20:30:00.808080+00'),
(15, 'lisa', 4, 'Iconic for a reason. The action, the story, and the visual effects were all ahead of their time.', '2002-04-25 13:15:00.909090+00');

-- JOKER (mid=17, release: 2019-10-04)
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(17, 'admin', 5, 'Joaquin Phoenix disappears into this role completely. One of the greatest performances of the decade.', '2019-11-01 21:00:00.010101+00'),
(17, 'andy', 4, 'Dark and disturbing in all the right ways. A deeply uncomfortable character study that stays with you.', '2019-10-20 18:30:00.020202+00'),
(17, 'khuzairi', 4, 'Uncomfortable viewing but important cinema. Phoenix is absolutely mesmerising throughout.', '2020-02-14 20:00:00.030303+00'),
(17, 'aliff', 5, 'Bold, challenging and brilliantly acted. Not your typical comic book movie by any stretch.', '2020-01-10 22:00:00.040404+00'),
(17, 'lisa', 3, 'Powerful performance but the film walks a fine line between critique and glorification.', '2019-12-25 16:45:00.050505+00');

-- THE GRAND BUDAPEST HOTEL (mid=19, release: 2014-03-07)
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(19, 'admin', 4, 'Wes Anderson''s most accessible film. Charming, witty, and visually stunning in every frame.', '2014-04-18 14:30:00.060606+00'),
(19, 'andy', 5, 'Pure joy from start to finish. Ralph Fiennes is absolutely perfect in every single scene.', '2014-05-22 20:00:00.070707+00'),
(19, 'khuzairi', 4, 'Quirky and delightful. The production design alone deserves its own award category.', '2015-01-01 12:00:00.080808+00'),
(19, 'aliff', 4, 'A beautiful film that works on multiple levels simultaneously. Funny, sad, and utterly unique.', '2016-07-15 19:30:00.090909+00');

-- BEFORE SUNRISE (mid=20, release: 1995-01-27)
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(20, 'admin', 4, 'Simple, honest and surprisingly moving. Hawke and Delpy have extraordinary chemistry together.', '1996-03-10 11:00:00.111222+00'),
(20, 'andy', 5, 'A conversation film that somehow feels more real and more alive than most action blockbusters.', '1997-08-20 15:30:00.222333+00'),
(20, 'khuzairi', 3, 'Beautifully filmed and well-acted but the deliberately slow pace will not be for everyone.', '2010-02-14 18:00:00.333444+00');

-- NUOVO CINEMA PARADISO (mid=6, release: 1988-09-29)
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(6, 'admin', 5, 'A love letter to cinema itself. The ending had me in tears. One of the most beautiful films ever made.', '1995-06-15 20:00:00.444555+00'),
(6, 'aliff', 5, 'One of the most emotionally powerful films I have ever experienced. An absolute masterpiece.', '2018-09-20 21:30:00.555666+00'),
(6, 'lisa', 4, 'Slow-burning but deeply rewarding. The final montage sequence is completely unforgettable.', '2008-05-10 19:00:00.666777+00'),
(6, 'khuzairi', 4, 'Discovered this gem recently. Cannot believe I waited this long to watch it.', '2023-01-28 16:45:00.777888+00');

-- LA LA LAND (mid=13, release: 2016-12-09)
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(13, 'admin', 4, 'Gorgeous to look at and listen to. Gosling and Stone are a genuinely perfect pairing.', '2017-01-15 20:30:00.888999+00'),
(13, 'andy', 5, 'A modern classic. The bittersweet ending is handled with extraordinary emotional intelligence.', '2017-02-28 19:00:00.999000+00'),
(13, 'khuzairi', 4, 'Visually stunning musical with real emotional depth beneath the sparkle. Loved every minute.', '2017-04-10 18:00:00.000111+00'),
(13, 'lisa', 3, 'Beautiful to look at but I expected more from the story. The original music is truly incredible though.', '2018-03-14 21:00:00.111222+00');

-- SPIRITED AWAY (mid=16, release: 2001-07-20)
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(16, 'andy', 5, 'Miyazaki''s greatest work. A film that works on every imaginable level. Pure magic.', '2002-03-10 14:00:00.222333+00'),
(16, 'khuzairi', 5, 'Magical, emotional and unlike anything else in existence. Perfect animation from start to finish.', '2010-08-15 20:00:00.333444+00'),
(16, 'lisa', 4, 'A stunning visual experience with a surprisingly deep and emotional story. A timeless classic.', '2005-12-20 19:30:00.444555+00'),
(16, 'cai', 4, 'Studio Ghibli at their absolute peak. Every single frame is a genuine work of art.', '2015-07-20 22:00:00.555666+00');

-- MAD MAX: FURY ROAD (mid=18, release: 2015-05-15)
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(18, 'admin', 4, 'Pure adrenaline from start to finish. George Miller is a genius for pulling this off at his age.', '2015-06-01 20:00:00.666777+00'),
(18, 'andy', 5, 'The most impressive action film of the decade. Practical effects used at an extraordinary level.', '2015-07-10 21:30:00.777888+00'),
(18, 'aliff', 4, 'Relentless and spectacular. Furiosa is one of the best action heroes in years of cinema.', '2016-02-20 18:00:00.888999+00'),
(18, 'lisa', 3, 'An incredible spectacle but the constant relentless action gets exhausting after a while.', '2015-09-15 16:30:00.999000+00');

-- INTERSTELLAR (mid=8) — adding more
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(8, 'khuzairi', 5, 'The docking scene set to Hans Zimmer''s score gave me genuine goosebumps. Epic filmmaking.', '2015-01-20 21:00:00.000111+00'),
(8, 'lisa', 4, 'Ambitious and deeply emotional. The time dilation concepts are genuinely mind-bending.', '2015-03-10 19:30:00.111222+00'),
(8, 'cai', 4, 'Visually stunning science fiction with a surprisingly heartfelt human story at its core.', '2016-04-05 20:00:00.222333+00');

-- TITANIC (mid=9) — adding more
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(9, 'admin', 5, 'A technical marvel and an emotional rollercoaster. Still holds up brilliantly after all these years.', '1998-02-14 20:00:00.333444+00'),
(9, 'andy', 4, 'Epic in every possible sense of the word. The scale of the production is truly staggering.', '1998-04-20 19:00:00.444555+00'),
(9, 'cai', 3, 'A spectacle for sure but the romance feels somewhat generic beneath all the impressive spectacle.', '2012-04-10 18:30:00.555666+00');

-- KUNG FU PANDA (mid=10) — adding more
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(10, 'khuzairi', 5, 'Surprisingly deep for an animated film. The message about believing in yourself is genuinely timeless.', '2009-03-14 15:00:00.666777+00'),
(10, 'lisa', 4, 'Hilarious and heartwarming in equal measure. Jack Black is absolutely perfect as Po.', '2010-06-10 17:30:00.777888+00');

-- WALL TO WALL (mid=38, release: 2025-07-18)
INSERT INTO reviews (mid, uid, ratings, review, rev_time) VALUES
(38, 'admin', 4, 'A surprisingly strong debut. The performances carry the film even when the script falters.', '2025-08-10 20:00:00.888999+00'),
(38, 'aliff', 5, 'Completely unexpected gem. Did not know what to expect but came away thoroughly impressed.', '2025-09-22 18:30:00.999000+00'),
(38, 'cai', 3, 'Decent enough but feels like it is trying too hard to be profound. Worth watching once.', '2025-10-15 21:00:00.000111+00');
