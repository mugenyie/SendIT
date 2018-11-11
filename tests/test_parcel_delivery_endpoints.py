import unittest
import json
from api import app
from random import randint
from .base import BaseTestCase


class ParcelDeliveryApiTestCase(BaseTestCase):

    def test_that_can_create_new_order(self):
        order = dict(
            weight = self.default_weight,
            weightmetric = self.default_weightmetric,
            senton = self.default_senton,
            deliveredon = self.default_deliveredon,
            status = self.default_status,
            from_ = self.default_from,
            to = self.default_to,
            currentlocation = self.default_currentlocation
        )

        response = self.client.post(
            'api/v1/parcels',
            content_type='application/json',
            data=json.dumps(order)
        )

        self.assertEqual(response.status_code, 201)


    def test_send_unexpected_order_data(self):
        order = dict(
            randomStuff = [{},{}]
        )

        response = self.client.post(
            'api/v1/parcels',
            content_type='application/json',
            data=json.dumps(order)
        )

        self.assertEqual(response.status_code, 400)


    def test_that_get_all_parcels(self):

        response = self.client.get('api/v1/parcels')

        self.assertEqual(response.status_code, 200)


    def test_that_can_fetch_specific_delivery_order(self):

        response = self.client.get('api/v1/parcels/1')

        self.assertEqual(response.status_code, 200)


    def test_with_unavailable_delivery_order(self):

        response = self.client.get('api/v1/parcels/1')

        self.assertEqual(response.status_code, 404)


    def test_fetch_orders_by_user(self):

        response = self.client.get('api/v1/users/1/parcels')

        self.assertEqual(response.status_code, 200)


    def test_fetch_orders_with_wrong_user(self):

        response = self.client.get('api/v1/users/90/parcels')

        self.assertEqual(response.status_code, 404)

    
    def test_can_cancel_delivery_order(self):

        response = self.client.patch('api/v1/parcels/2/cancel')

        self.assertEqual(response.status_code, 204)


    def test_can_cancel_unavailable_order(self):

        response = self.client.patch('api/v1/parcels/100/cancel')

        self.assertEqual(response.status_code, 404)


    def test_can_change_destination_of_delivery_order(self):

        response = self.client.patch('api/v1/parcels/2/destination')

        self.assertEqual(response.status_code, 204)


    def test_can_change_status_of_delivery_order(self):

        response = self.client.patch('api/v1/parcels/2/status')

        self.assertEqual(response.status_code, 204)


    def test_can_change_order_current_location(self):

        response = self.client.patch('/parcels/2/currentlocation')

        self.assertEqual(response.status_code, 204)