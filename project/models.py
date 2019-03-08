from project import db
from datetime import datetime



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




class SensorReadings(db.Model):
    __tablename__ = 'sensorreadings'
    p_key = db.Column(db.Integer, primary_key=True)
    #Column('last_updated', DateTime, onupdate=datetime.datetime.now)
    recorded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow(),onupdate=datetime.utcnow())
    sensor_id = db.Column(db.String(64), db.ForeignKey('sensor_info.sensor_id'))
    kpa_value = db.Column(db.NUMERIC(precision=3))
    min_frequency = db.Column(db.NUMERIC(precision=3))
    max_frequency = db.Column(db.NUMERIC(precision=3))
    computed_frequency = db.Column(db.NUMERIC(precision=3))
    mean = db.Column(db.NUMERIC(precision=3))
    std_dev = db.Column(db.NUMERIC(precision=3))

    def __init__(self, sensor_id, reading_data):
        self.sensor_id = sensor_id
        self.kpa_value = reading_data["kpa_value"]
        self.min_frequency = reading_data["min_frequency"]
        self.max_frequency = reading_data["max_frequency"]
        self.computed_frequency = reading_data["computed_frequency"]
        self.mean = reading_data["mean"]
        self.std_dev = reading_data["std_dev"]
