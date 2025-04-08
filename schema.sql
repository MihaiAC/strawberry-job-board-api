Table employers {
  id integer [pk]
  name varchar(40) [not null]
  contact_email varchar(254) [not null]
  industry varchar(254) [not null]
}

Table users {
  id integer [pk]
  username varchar(30) [not null]
  email varchar(254) [not null]
  password_hash varchar(128) [not null]
  role varchar [not null]
}

Table jobs {
  id integer [pk]
  title varchar(150) [not null]
  description varchar(1000) [not null]
  employer_id integer [not null, ref: > employers.id]
}

Table applications {
  id integer [pk]
  user_id integer [not null, ref: > users.id]
  job_id integer [not null, ref: > jobs.id]
}