CREATE DATABASE IF NOT EXISTS ajiqhords_db;
USE ajiqhords_db;

CREATE TABLE IF NOT EXISTS songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    key_signature VARCHAR(10) NOT NULL,
    content TEXT NOT NULL
);

-- Insert the mock song for testing
INSERT INTO songs (title, artist, key_signature, content) 
VALUES (
    'It Will Rain', 
    'Bruno Mars', 
    'C', 
    '[C]If you ever leave me, baby\nLeave some morphological [Em]water at my door\n[C]Cause it would take a whole lot of medication\nTo realize what we [Em]used to have, we don''t have it anymore\n\n[F]There''s no religion that could save me\nNo matter how [Em]long my knees are on the floor (Ooh)\n[Dm]So keep in mind all the sacrifices I''m makin''\n[G]To keep you by my side\n[G]To keep you from walkin'' out the door\n\nChorus:\nCause there''ll be no [F]sunlight\n[G]If I lose [C]you, baby\nThere''ll be no [F]clear skies\n[G]If I lose [C]you, baby\nJust like the [F]clouds\nMy [G]eyes will do the [E7]same, if you walk a[Am]way\n[Am]Everyday it will [Dm]rain\n[G]Rain, [C]ra-a-a-ain'
);
