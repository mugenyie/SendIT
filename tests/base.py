import json
import unittest
from api import app
from api.models.database import DatabaseConnection


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

        self.user = dict(
            email = self.default_email,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        """
        Create default user and get auth token
        """
        self.client.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(self.user)
        )
        response = self.client.post(self.default_login_endpoint, json=self.user)
        data = response.get_json(force=True).get('data')
        self.token = data[0].get('token')

        """
        Create deafault order
        """
        order = dict(
                placedby="1",
                weight="4",
                weightmetric="Kg",
                senton= "2018-11-13 02:05:13.344624+03",
                to="ntinda",
            )
        order['from'] ="Nitnda"
        response = self.client.post(
            'api/v1/parcels',
            headers={'Authorization': self.token},
            content_type='application/json',
            data=json.dumps(order)
        )

    def tearDown(self):
        pass