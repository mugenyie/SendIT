import unittest
from api import app
from api.database import DatabaseConnection


database = DatabaseConnection()
database.create_database_relations() #create relations if ttey dont exist

class BaseTestCase(unittest.TestCase):

    # Default User information
    default_login_endpoint = 'api/v1/auth/login'
    default_signup_endpoint = 'api/v1/auth/signup'
    default_email = 'ecmugenyi@gmail.com'
    default_username = 'columbus'
    default_password = '1234'
    default_firstname = 'Emmanuel'
    default_lastname = 'Mugenyi'
    default_othernames = 'Columbus'

    # Default Parcel Information
    default_weight = 4.34
    default_weightmetric = 'Kg'
    default_senton = '2018-01-08 04:05:06 +3:00'
    default_deliveredon = '2018-01-20 12:05:06 +3:00'
    default_status = 'PLACED'                               # PLACED, TRANSITING, DELIVERED 
    default_from = 'Ntinda Complex, Ntinda - Kisaasi road'
    default_to = 'Fort-portal Town'
    default_currentlocation = 'Ntinda Shopping Centre'
    
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        # method to invoke after each test.
        pass