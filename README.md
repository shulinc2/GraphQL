# GraphQL
GraphQL API I developed using Flask, Graphene, and pymysql. This API allows users to query all job postings. 

# Testing 
- Use the following command in Terminal and localhost for GraphQL query

```
run schema.py
click link: http://localhost:8012/graphql
GraphQL page runs the query  example
{
  allPostings{
    category
    description
    employerID
    experience
    package
    title
    type
    postingID
    companyName
  }
}
```
