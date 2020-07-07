from project import db
from datetime import datetime
#import pytz



class Crops(db.Model):
    __tablename__ = 'crops'

    crop_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    crop_name = db.Column(db.String)
    ideal_kpa = db.Column(db.Integer)
    dry_kpa = db.Column(db.Integer)
    saturated_kpa = db.Column(db.Integer)
    sensors = db.relationship('Sensors', backref='crops', lazy=True)

    def __init__(self, crop_name, ideal_kpa, dry_kpa, saturated_kpa):
        self.crop_name = crop_name
        self.ideal_kpa = ideal_kpa
        self.dry_kpa = dry_kpa
        self.saturated_kpa = saturated_kpa


#    def __repr__(self):
#        crop_list = {"name": self.crop, "ideal_kpa": self.ideal_kpa, "dry_kpa":self.dry_kpa, "saturated_kpa": self.saturated_kpa}
#        return crop_list

#asdfsadfsdaf

class Sensors(db.Model):
    __tablename__ = 'sensors'

    sensor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sensor_name = db.Column(db.String)
    configuration = db.Column(db.String(64), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.crop_id'))
    valve_id = db.Column(db.Integer, db.ForeignKey('valves.valve_id'))
    bcm_pin = db.Column(db.Integer, nullable=False)

    def __init__(self, name, configuration, crop_id, valve_id, bcm_pin):
        self.sensor_name = name
        self.configuration = configuration
        self.crop_id = crop_id
        self.valve_id = valve_id
        self.bcm_pin = bcm_pin


class Valves(db.Model):
    __tablename__ = 'valves'

    valve_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valve_name = db.Column(db.String)
    relay_controller = db.Column(db.Integer, nullable=False)
    sensors = db.relationship('Sensors', backref='valves', lazy=True)

    def __init__(self, valve_name, relay_controller):
        self.valve_name = valve_name
        self.relay_controller = relay_controller

    def __str__(self):
        return "ID: {id}  Name: {name} Relay Controller: {rc}".format(id=self.valve_id, name=self.valve_name, rc=self.relay_controller)



class SensorReadings(db.Model):
    __tablename__ = 'sensorreadings'
    p_key = db.Column(db.Integer, primary_key=True)
    recorded_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    sensor_id = db.Column(db.String(64), db.ForeignKey('sensors.sensor_id'))
    kpa_value = db.Column(db.Integer)
    min_frequency = db.Column(db.NUMERIC(10,3))
    max_frequency = db.Column(db.NUMERIC(10,3))
    computed_frequency = db.Column(db.NUMERIC(10,3))
    mean = db.Column(db.NUMERIC(10,3))
    std_dev = db.Column(db.NUMERIC(10,3))

    def __init__(self, sensor_id, reading_data):
        self.sensor_id = sensor_id
        self.kpa_value = reading_data["kpa_value"]
        self.min_frequency = reading_data["min_frequency"]
        self.max_frequency = reading_data["max_frequency"]
        self.computed_frequency = reading_data["computed_frequency"]
        self.mean = reading_data["mean"]
        self.std_dev = reading_data["std_dev"]


class WateringEvent(db.Model):
    __tablename__ = 'wateringevents'
    p_key = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    valve_id = db.Column(db.Integer)
    open_time = db.Column(db.Integer)
    state = db.Column(db.String)
    water_start = db.Column(db.DateTime)
    water_stop = db.Column(db.DateTime)
    trigger_kpa = db.Column(db.Integer)

    def __init__(self, valve_id, water_start, trigger_kpa):
        self.valve_id = valve_id
        self.water_start = water_start
        self.trigger_kpa = trigger_kpa
        self.state = 'IN PROGRESS'


        


