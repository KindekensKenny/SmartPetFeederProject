from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    # LDR
    @staticmethod
    def read_LDR():
        sql = "SELECT * FROM .historiek where DeviceID = 1"
        return Database.get_rows(sql)

    @staticmethod
    def read_LDR_by_id(id):
        sql = "SELECT * FROM historiek where ActieID = 1 and DeviceID = 1 and id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def add_LDR(Datum, Waarde):
        sql = "INSERT INTO historiek(DeviceID, ActieID, Datum, Waarde) VALUES(1, 1, %s, %s)"
        params = [Datum, Waarde]
        return Database.execute_sql(sql, params)

    # MOTOR
    @staticmethod
    def read_Status_Motor():
        sql = "SELECT * FROM historiek where DeviceID = 4"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_Motor_by_id(id):
        sql = "SELECT * FROM smartpetfeederdb.historiek where DeviceID = 4 and id = %s"
        params = [id]
        return Database.get_one_row(sql, params)
    
    @staticmethod
    def add_Motor(Datum):
        sql = "INSERT INTO historiek(DeviceID, ActieID, Datum, Waarde) VALUES(4, 3, %s, NULL)"
        params = [Datum]
        return Database.execute_sql(sql, params)

    # PIR
    @staticmethod
    def read_Status_PIR():
        sql = "SELECT * FROM historiek where DeviceID = 2"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_PIR_by_id(id):
        sql = "SELECT * FROM smartpetfeederdb.historiek where DeviceID = 2 and id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def add_PIR(Datum, Waarde):
        sql = "INSERT INTO historiek(DeviceID, ActieID, Datum, Waarde) VALUES(2, 2, %s, %s)"
        params = [Datum, Waarde]
        return Database.execute_sql(sql, params)

    #HX711
    @staticmethod
    def read_Status_HX711():
        sql = "SELECT * FROM historiek where DeviceID = 3"
        return Database.get_rows(sql)
    
    def read_HX711_by_id(id):
        sql = "SELECT * FROM smartpetfeederdb.historiek where DeviceID = 3 and id = %s"
        params = [id]
        return Database.get_one_row(sql, params)
    
    @staticmethod
    def add_HX711(Datum, Waarde):
        sql = "INSERT INTO historiek(DeviceID, ActieID, Datum, Waarde) VALUES(3, 4, %s, %s)"
        params = [Datum, Waarde]
        return Database.execute_sql(sql, params)

    # History
    @staticmethod
    def read_History():
        sql = "SELECT DeviceID, ActieID, Datum, Waarde FROM historiek"
        return Database.get_rows(sql)

    @staticmethod
    def reset_History():
        sql = "DELETE FROM historiek"
        return Database.get_rows(sql)
