#### Nested Queries

The naive way is to just put lazy="joined" on every relationship, but even that doesn't cover every case e.g: 
```
query {
	job(id: 1) {
		employer {
			jobs {
				id
			}
		}
	}
}
```
.. and it also gets more data from the DB than it needs, since the query may not even be interested in the relationships.

My original plan was to make possible a nested query like:
user -> applications -> jobs -> employer aka for a given user, get all the employers that posted jobs. Maybe this is my inexperience talking but doing this efficiently seems to be highly non-trivial even in this small example. My idea was to limit the recursion depth of a query to 3, then recursively parse the query with the Info object to find out what "joinedload" to add to the SQL query.  From this initial query parsing, I would also extract useful information to help transform the result into the corresponding Strawberry type (which must also be done recursively). 

This query parsing is complicated by the fact that you have to somehow map every Strawberry type's relevant fields to their corresponding SQL class (e.g: job -> Job, jobs -> Job, applications -> Application and so on...) and also you'd have to call the appropriate "joinedload" afterwards (again, converting to the appropriate SQLAlchemy class field from a string you extract from info.selected_fields). The solution I came up with was extremely flaky and would break on any field/class rename and would have also been annoying to test.

I also found **[strawberry-sqlalchemy](https://github.com/strawberry-graphql/strawberry-sqlalchemy)**, but it doesn't seem to offer the freedom you need.

Since this is a toy example I'll just limit the query depth to 1 and use "joinedload" naively.

Today's lesson: with GraphQL (and the current backend stack at least) prefer breadth over depth in queries. I think deeply nested queries are ill suited for SQL backends anyway and would be better suited for graph / NoSQL DBs.

If parsing the query were easier, I could also ban certain nested queries from happening (similar to complexity score) - e.g: two one-to-many joins in the same query.

Didn't find a natural way to handle them with SQLAlchemy + Strawberry. Maybe Django has better integration? 

Making only certain nested queries available - doable when the endpoint is private and used within a team but if public?

#### Class duplication
Every entity has two classes which are tightly coupled  - the sql version used by SQLA and the gql version used by Strawberry. I don't see how they couldn't be tightly coupled - they basically need to have the same fields even though they serve different purposes 

This creates a lot of extra headaches (e.g: circular reference errors) and extra clutter. Since they are tightly coupled anyway, I imported the gql types in db.models; in all the other files that required the gql types I imported them from db.models (since I would also import the sqla types anyway in most cases).

#### Queries at the same level
You get a separate info object for each query.

### SQLAlchemy

#### FK Deletions
Setting ondelete="CASCADE" on Foreign Key => how deletions are handled at the DB level.
Setting cascade="all, delete-orphan" on relationship => how deletions are handled at the ORM level (e.g: You have a Job object and remove its Employer => Job should be deleted).
So - use either the first one or both depending on the use case.

Confusingly, FK ondelete -> on the object to be deleted (e.g: Job).
cascade="all, delete-orphan" -> on the parent (Employer -> Job is a 1-to-many, put it on the relationship there).
