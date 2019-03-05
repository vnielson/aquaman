from project import db
#from datetime import datetime



class Crop_Info(db.Model):
    __tablename__ = 'crop_info'

    crop = db.Column(db.String(64), primary_key=True)
    ideal_kpa = db.Column(db.Integer)
    dry_kpa = db.Column(db.Integer)
    saturated_kpa = db.Column(db.Integer)

    def __init__(self, crop, ideal_kpa, dry_kpa, saturated_kpa):
        self.crop = crop
        self.ideal_kpa = ideal_kpa
        self.dry_kpa = dry_kpa
        self.saturated_kpa = saturated_kpa


#    def __repr__(self):
#        crop_list = {"name": self.crop, "ideal_kpa": self.ideal_kpa, "dry_kpa":self.dry_kpa, "saturated_kpa": self.saturated_kpa}
#        return crop_list


class Sensor_Info(db.Model):
    __tablename__ = 'sensor_info'

    sensor_id = db.Column(db.String(64), primary_key=True)
    configuration = db.Column(db.String(64), nullable=False)
    crop = db.Column(db.String(64), db.ForeignKey('crop_info.crop'))
    valve = db.Column(db.String(64), db.ForeignKey('valve_info.valve_id'))
    bcm_pin = db.Column(db.Integer, nullable=False)

    def __init__(self, sensor_id, configuration, crop, valve, bcm_pin):
        self.sensor_id = sensor_id
        self.configuration = configuration
        self.crop = crop
        self.valve = valve
        self.bcm_pin = bcm_pin



class Valve_Info(db.Model):
    __tablename__ = 'valve_info'

    valve_id = db.Column(db.String(64), primary_key=True)
    bcm_pin = db.Column(db.Integer, nullable=False)

    def __init__(self, valve_id, bcm_pin):
        self.valve_id = valve_id
        self.bcm_pin = bcm_pin



