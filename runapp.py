from api import app
from api.database import DatabaseConnection


database = DatabaseConnection()
database.create_database_relations()

app.run(debug=True)