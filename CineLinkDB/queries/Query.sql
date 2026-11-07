CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE media (
    id SERIAL PRIMARY KEY,
    tmdb_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(20) CHECK (type IN ('movie', 'series')) NOT NULL,
    --the combination between ID and TYPE must me ubique, because TMDB has same id for movies and shows
    UNIQUE (tmdb_id, type)
);

CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    tmdb_id INT UNIQUE,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE user_media_ratings (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    media_id INT REFERENCES media(id) ON DELETE CASCADE,
    rating INT CHECK (rating >= 1 AND rating <= 10),
    PRIMARY KEY (user_id, media_id)
);

CREATE TABLE user_character_favorites (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    character_id INT REFERENCES characters(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, character_id)
);

CREATE TABLE communities (
    id SERIAL PRIMARY KEY,
    media_id INT REFERENCES media(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE community_members (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    community_id INT REFERENCES communities(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, community_id)
);

CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    community_id INT REFERENCES communities(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    room_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
