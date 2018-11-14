import unittest
import json
from api import app
from random import randint
from .base import BaseTestCase


class ParcelDeliveryApiTestCase(BaseTestCase):

    def test_with_inexistent_user(self):
        order = dict(
                placedby="0",
                weight="4",
                weightmetric="Kg",
                senton= "2018-11-13 02:05:13.344624+03",
                deliveredon= "2018-11-13 02:05:13.344624+03",
                to="ntinda",
                currentlocation="ntinda"
            )
        order['from'] ="Nitnda"
        response = self.client.post(
            'api/v1/parcels',
            content_type='application/json',
            data=json.dumps(order)
        )
        self.assertEqual(response.status_code, 404)

    def test_send_no_destination(self):
        order = dict(
                placedby="0",
                weight="4",
                weightmetric="Kg",
                senton= "2018-11-13 02:05:13.344624+03",
                deliveredon= "2018-11-13 02:05:13.344624+03",
                to="",
                currentlocation="ntinda"
            )
        order['from'] ="Nitnda"
        response = self.client.post(
            'api/v1/parcels',
            content_type='application/json',
            data=json.dumps(order)
        )
        self.assertEqual(response.status_code, 404)

    def test_send_no_source(self):
        order = dict(
                placedby="0",
                weight="4",
                weightmetric="Kg",
                senton= "2018-11-13 02:05:13.344624+03",
                deliveredon= "2018-11-13 02:05:13.344624+03",
                to="ntinda",
                currentlocation="ntinda"
            )
        order['from'] =""
        response = self.client.post(
            'api/v1/parcels',
            content_type='application/json',
            data=json.dumps(order)
        )
        self.assertEqual(response.status_code, 404)

    def test_invalid_weight(self):
        order = dict(
            placedby="87",
            weight="jkl",
            weightmetric="Kg",
            senton= "2018-11-13 02:05:13.344624+03",
            deliveredon= "2018-11-13 02:05:13.344624+03",
            to="ntinda",
            currentlocation="ntinda"
        )
        order['from'] ="Nitnda"
        response = self.client.post(
            'api/v1/parcels',
            content_type='application/json',
            data=json.dumps(order)
        )
        self.assertEqual(response.status_code, 404)

    def test_empty_senton_date(self):
        order = dict(
                placedby="0",
                weight="4",
                weightmetric="Kg",
                senton= "",
                deliveredon= "2018-11-13 02:05:13.344624+03",
                to="ntinda",
                currentlocation="ntinda"
            )
        order['from'] ="Nitnda"
        response = self.client.post(
            'api/v1/parcels',
            content_type='application/json',
            data=json.dumps(order)
        )
        self.assertEqual(response.status_code, 404)


    # def test_send_unexpected_order_data(self):
    #     order = dict(
    #         randomStuff = dict(data = 'random')
    #     )
    #     response = self.client.post(
    #         'api/v1/parcels',
    #         content_type='application/json',
    #         data=json.dumps(order)
    #     )
    #     self.assertEqual(response.status_code, 404)


    def test_that_get_all_parcels(self):

        response = self.client.get('api/v1/parcels')

        self.assertEqual(response.status_code, 200)


    def test_fetch_specific_delivery_order_invalid_id(self):

        response = self.client.get('api/v1/parcels/p')

        self.assertEqual(response.status_code, 404)


    def test_fetch_orders_by_wrong_user(self):

        response = self.client.get('api/v1/users/0/parcels')

        self.assertEqual(response.status_code, 404)


    # def test_fetch_orders_with_wrong_user(self):

    #     response = self.client.get('api/v1/users/90/parcels')

    #     self.assertEqual(response.status_code, 404)

    
    # def test_can_cancel_delivery_order(self):

    #     response = self.client.patch('api/v1/parcels/2/cancel')

    #     self.assertEqual(response.status_code, 204)


    # def test_can_cancel_unavailable_order(self):

    #     response = self.client.patch('api/v1/parcels/100/cancel')

    #     self.assertEqual(response.status_code, 404)


    # def test_can_change_destination_of_delivery_order(self):

    #     response = self.client.patch('api/v1/parcels/2/destination')

    #     self.assertEqual(response.status_code, 204)


    # def test_can_change_status_of_delivery_order(self):

    #     response = self.client.patch('api/v1/parcels/2/status')

    #     self.assertEqual(response.status_code, 204)


    # def test_can_change_order_current_location(self):

    #     response = self.client.patch('/parcels/2/currentlocation')

    #     self.assertEqual(response.status_code, 204)