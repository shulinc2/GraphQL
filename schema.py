from flask import Flask, request
from flask_graphql import GraphQLView
import graphene
import pymysql


# GraphQL Types
class PostingType(graphene.ObjectType):
    postingID = graphene.Int()
    company_name = graphene.String()
    category = graphene.String()
    description = graphene.String()
    employerID = graphene.String()
    experience = graphene.String()
    location = graphene.String()
    package = graphene.String()
    title = graphene.String()
    type = graphene.String()

# GraphQL Query
class Query(graphene.ObjectType):
    all_postings = graphene.List(PostingType,
                                 page=graphene.Int(default_value=1),
                                 limit=graphene.Int(default_value=10),
                                 category=graphene.String(),
                                 location=graphene.String())

    def resolve_all_postings(self, info, page, limit, category=None, location=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        offset = (page - 1) * limit

        query = "SELECT * FROM posting WHERE 1=1"
        query_params = []

        if category:
            query += " AND category = %s"
            query_params.append(category)

        if location:
            query += " AND location = %s"
            query_params.append(location)

        query += " LIMIT %s OFFSET %s"
        query_params.extend([limit, offset])

        cursor.execute(query, query_params)
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return [PostingType(**posting) for posting in result]



def get_db_connection():
    return pymysql.connect(host='mysql-database.czrn9xpuxd4a.us-east-2.rds.amazonaws.com',
                           user='admin',
                           password='Ea12345678!',
                           db='6156service',
                           cursorclass=pymysql.cursors.DictCursor)



# Setting up Flask app and GraphQL endpoint
app = Flask(__name__)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=graphene.Schema(query=Query), graphiql=True))

if __name__ == '__main__':
    app.run(host="localhost", port=8012, debug=True)
