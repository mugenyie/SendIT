import unittest
import json
from api import app
from random import randint
from .base import BaseTestCase
from api.models.user import User


class ParcelDeliveryApiTestCase(BaseTestCase):
    def test_create_order(self):
        order = dict(
                placedby="1",
                weight="4",
                weightmetric="Kg",
                senton= "2018-11-13 02:05:13.344624+03",
                to="ntinda"
            )
        order['from'] ="Nitnda"
        response = self.client.post(
            'api/v1/parcels',
            content_type='application/json',
            data=json.dumps(order)
        )
        self.assertEqual(response.status_code, 201)

    def test_get_parcels(self):
        response = self.client.get('api/v1/parcels')
        self.assertEqual(response.status_code, 200)

    def test_create_order_with_inexistent_user(self):
        order = dict(
                placedby="0",
                weight="4",
                weightmetric="Kg",
                senton= "2018-11-13 02:05:13.344624+03",
                to="ntinda"
            )
        order['from'] ="Nitnda"
        response = self.client.post(
            'api/v1/parcels',
            content_type='application/json',
            data=json.dumps(order)
        )
        self.assertEqual(response.status_code, 404)


    def test_invalid_weight(self):
        order = dict(
            placedby="1",
            weight="jkl",
            weightmetric="Kg",
            senton= "2018-11-13 02:05:13.344624+03",
            to="ntinda",
        )
        order['from'] ="Nitnda"
        response = self.client.post(
            'api/v1/parcels',
            content_type='application/json',
            data=json.dumps(order)
        )
        self.assertEqual(response.status_code, 400)


    def test_that_get_all_parcels(self):
        response = self.client.get('api/v1/parcels')
        self.assertEqual(response.status_code, 200)


    def test_fetch_specific_delivery_order_invalid_id(self):
        response = self.client.get('api/v1/parcels/2569845')
        self.assertEqual(response.status_code, 404)


    def test_fetch_orders_by_unregistered_user(self):
        response = self.client.get('api/v1/users/84684615/parcels')
        self.assertEqual(response.status_code, 404)

    
    def test_cancel_unavailable_delivery_order(self):
        response = self.client.patch('api/v1/parcels/0/cancel')
        self.assertEqual(response.status_code, 404)


    def test_change_destination_with_invalid_order(self):
        response = self.client.patch('api/v1/parcels/0/destination')
        self.assertEqual(response.status_code, 400)

    # def test_change_destination(self):
    #     destination = dict(
    #             to="Kasese"
    #         )
    #     response = self.client.patch(
    #         'api/v1/parcels/1/destination',
    #         content_type='application/json',
    #         data=json.dumps(destination)
    #     )
    #     self.assertEqual(response.status_code, 200)

    # def test_change_destination_with_empty(self):
    #     destination = dict(
    #             to=""
    #         )
    #     response = self.client.patch(
    #         'api/v1/parcels/1/destination',
    #         content_type='application/json',
    #         data=json.dumps(destination)
    #     )
    #     self.assertEqual(response.status_code, 400)

    def test_change_order_status_with_empty(self):
        response = self.client.patch('api/v1/parcels/4/status')
        self.assertEqual(response.status_code, 400)

    def test_change_order_status_with_user_notadmin(self):
        status = dict(
            userid="100",
            status="PLACED"
        )
        response = self.client.patch(
            'api/v1/parcels/87/status',
            content_type='application/json',
            data=json.dumps(status)
        )
        self.assertEqual(response.status_code, 401)


    def test_change_order_current_location_notadmin(self):
        status = dict(
            userid="100",
            status="PLACED"
        )
        response = self.client.patch(
            'api/v1/parcels/87/currentlocation',
            content_type='application/json',
            data=json.dumps(status)
        )
        self.assertEqual(response.status_code, 401)