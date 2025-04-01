#### Nested Queries
Didn't find a natural way to handle them with SQLAlchemy + Strawberry. Maybe Django has better integration? 

In the future, avoid nested queries if possible (maybe just use a REST API instead).

My original plan was to make possible a nested query like:
user -> applications -> jobs -> employer aka for a given user, get all the employers that posted jobs. Maybe this is my inexperience talking but doing this efficiently seems to be highly non-trivial even in this small example. My idea was to limit the recursion depth of a query to 3, then recursively parse the query with the Info object to find out what "joinedload" to add to the SQL query.  From this initial query parsing, I would also extract useful information to help transform the result into the corresponding Strawberry type (which must also be done recursively). 

This query parsing is complicated by the fact that you have to somehow map every Strawberry type's relevant fields to their corresponding SQL class (e.g: job -> Job, jobs -> Job, applications -> Application and so on...) and also you'd have to call the appropriate "joinedload" afterwards (again, converting to the appropriate SQLAlchemy class field from a string you extract from info.selected_fields). The solution I came up with was extremely flaky and would break on any field/class rename and would have also been a nightmare to test.

I also found **[strawberry-sqlalchemy](https://github.com/strawberry-graphql/strawberry-sqlalchemy)**, but it doesn't seem to offer the freedom you need (maybe I'm wrong).

Anyway, since this is a toy example I'll just limit the query depth to 1 and use "joinedload" naively.

Maybe I just missed something crucial and this is much easier than I think it is.

### SQLAlchemy

#### FK Deletions
Setting ondelete="CASCADE" on Foreign Key => how deletions are handled at the DB level.
Setting cascade="all, delete-orphan" on relationship => how deletions are handled at the ORM level (e.g: You have a Job object and remove its Employer => Job should be deleted).
So - use either the first one or both depending on the use case.

Confusingly, FK ondelete -> on the object to be deleted (e.g: Job).
cascade="all, delete-orphan" -> on the parent (Employer -> Job is a 1-to-many, put it on the relationship there).
