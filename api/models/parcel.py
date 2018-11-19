from api.models.database import DatabaseConnection
from api.utils import encrypt_password


database = DatabaseConnection()
class Parcel:
    def __init__(self, data={}):
        self.parcelId = data.get('parcelId')
        self.placedby = data.get('placedby')
        self.weight = data.get('weight')
        self.weightmetric = data.get('weightmetric')
        self.senton = data.get('senton')
        self.status = data.get('status')
        self.from_ = data.get('from')
        self.to = data.get('to')
        self.deliveredon = data.get('deliveredon')
        self.currentlocation = data.get('currentlocation')
        self.isCanceled = data.get('isCanceled')

    def creat_parcel_delivery_order(self):
        get_parcel_command = """
        INSERT INTO parcels (placedby, weight, weightmetric, senton, status, "from", "to")
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        RETURNING id, placedby, weight, weightmetric, senton, status, "from", "to"
        """
        database.cursor.execute(get_parcel_command, (
            self.placedby, self.weight, 
            self.weightmetric, self.senton, 
            "PLACED", 
            self.from_, self.to
        ))
        parcel = database.cursor.fetchone()
        return parcel

    def get_all_parcel_order(self):
        get_parcel_orders_command = """
        SELECT id, placedby, weight, weightmetric, senton, deliveredon,status, "from", "to", currentlocation
        from parcels 
        """
        database.cursor.execute(get_parcel_orders_command)
        columns = [col[0] for col in database.cursor.description]
        parcels = [dict(zip(columns, parcel)) for parcel in database.cursor.fetchall()]        
        return parcels

    def get_specific_parcel_order(self):
        get_parcel_orders_command = """
        SELECT * from parcels WHERE id = {}
        """.format(self.parcelId)
        database.cursor.execute(get_parcel_orders_command)
        columns = [col[0] for col in database.cursor.description]
        parcels = [dict(zip(columns, parcel)) for parcel in database.cursor.fetchall()]        
        return parcels

    def get_parcel_orders_by_user(self):
        get_parcel_orders_command = """
        SELECT id, placedby, weight, weightmetric, senton, deliveredon,status, "from", "to", currentlocation
        from parcels WHERE placedby = {}
        """.format(self.placedby)
        database.cursor.execute(get_parcel_orders_command)
        columns = [col[0] for col in database.cursor.description]
        parcels = [dict(zip(columns, parcel)) for parcel in database.cursor.fetchall()]        
        return parcels

    def cancel_delivery_order(self):
        cancel_parcel_order = """
        UPDATE parcels SET iscanceled = True WHERE id = {}
        """.format(self.parcelId)
        database.cursor.execute(cancel_parcel_order)   
        return 

    def change_order_destination(self):
        change_destination_commnd = """
        UPDATE parcels SET "to" = '{}' WHERE id = {}
        """.format(self.to, self.parcelId)
        database.cursor.execute(change_destination_commnd)   
        return 

    def change_order_status(self):
        change_status_commnd = """
        UPDATE parcels SET "status" = '{}' WHERE id = {}
        """.format(self.status, self.parcelId)
        database.cursor.execute(change_status_commnd)   
        return 
    
    def check_order_status(self):
        status_commnd = """
        select status from parcels WHERE id = {}
        """.format(self.parcelId)
        database.cursor.execute(status_commnd)   
        order = database.cursor.fetchone()
        return order[0]