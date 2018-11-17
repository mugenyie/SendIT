from enum import Enum


class OrderStatus(Enum):
    PLACED = 'PLACED'
    TRANSITING = 'TRANSITING'
    DELIVERED = 'DELIVERED'