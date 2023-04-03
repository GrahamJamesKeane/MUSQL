DO $$ 
BEGIN 
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'role') THEN 
    CREATE TYPE role AS ENUM ('user', 'admin');
  END IF; 
END $$;

DROP TABLE IF EXISTS accounts CASCADE;
CREATE TABLE accounts (
	id serial4 NOT NULL,
	user_id varchar(8) NOT NULL,
	"password" varchar(200) NOT NULL,
	email varchar(50) NOT NULL,
	user_role role DEFAULT 'user' NOT NULL,
	CONSTRAINT accounts_pkey PRIMARY KEY (id),
	CONSTRAINT unique_email UNIQUE (email),
	CONSTRAINT unique_student_id UNIQUE (student_id)
);

INSERT INTO accounts (student_id, password, email, user_role)
VALUES 
('user', 'pbkdf2:sha256:260000$iMcSWKANGhYdBRZG$551627a5398cddeabfd92b96388d01afbeb2a7ff0a799afca4f40c53e10ed043', 'user@mumail.ie', 'user'), 
('admin', 'pbkdf2:sha256:260000$odyMbOEotgjnF4Ae$e7490d435bace4a540cfe9f6813cc758d3cc53fb4b5d8bbedfce8fb301308df8', 'admin@mu.ie', 'admin');

DROP TABLE IF EXISTS assignments CASCADE;
CREATE TABLE assignments (
	id serial4 NOT NULL,
	assignment_name varchar(50) NOT NULL,
	max_attempts int4 NULL,
	due_date date NOT NULL,
	duration_mins int4 NOT NULL,
	CONSTRAINT assignments_pkey PRIMARY KEY (id),
	CONSTRAINT unique_assignment_name UNIQUE (assignment_name)
);

INSERT INTO assignments (assignment_name, max_attempts, due_date, duration_mins)
VALUES
('assignment 1', 2, '2023-03-24', 90),
('assignment 2', 2, '2023-04-24', 90),
('assignment 3', 2, '2023-05-24', 90),
('assignment 4', 2, '2023-06-24', 90),
('assignment 5', 2, '2023-07-24', 90);

DROP TABLE IF EXISTS results CASCADE;
CREATE TABLE results (
	id serial4 NOT NULL,
	account_id int4 NOT NULL,
	assignment_id int4 NOT NULL,
	num_attempts int4 NOT NULL DEFAULT 0,
	grade int4 NOT NULL DEFAULT 0,
	submission_data jsonb NULL,
	CONSTRAINT results_pkey PRIMARY KEY (id),
    CONSTRAINT results_account_id_fkey FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    CONSTRAINT results_assignment_id_fkey FOREIGN KEY (assignment_id) REFERENCES assignments(id) ON DELETE CASCADE
);

INSERT INTO results (account_id, assignment_id)
SELECT accounts.id, assignments.id
FROM accounts, assignments
WHERE accounts.student_id = 'user';