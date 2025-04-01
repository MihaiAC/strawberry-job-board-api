
### SQLAlchemy

#### FK Deletions
Setting ondelete="CASCADE" on Foreign Key => how deletions are handled at the DB level.
Setting cascade="all, delete-orphan" on relationship => how deletions are handled at the ORM level (e.g: You have a Job object and remove its Employer => Job should be deleted).
So - use either the first one or both depending on the use case.

Confusingly, FK ondelete -> on the object to be deleted (e.g: Job).
cascade="all, delete-orphan" -> on the parent (Employer -> Job is a 1-to-many, put it on the relationship there).
