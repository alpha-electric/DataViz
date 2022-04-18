from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Battery(Base):
    __tablename__ = "battery"
    battery_id = Column(Integer, primary_key=True)
    location = Column(Integer, ForeignKey("location.location_id"))
    mico_con_id = Column(Integer, ForeignKey("microController.microcontroller_id"))
    battery_infos = relationship("BatteryInfo", backref=backref("battery"))
    serial_num = Column(String)
    name = Column(String)
    dalyBMSSerial = Column(String)
    isOn = Column(Boolean)
    isPinned = Column(Boolean)


class Location(Base):
    __tablename__ = "location"
    location_id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    lat = Column(Float)
    long = Column(Float)
    isPinned = Column(Boolean)


class MicroController(Base):
    __tablename__ = "microController"
    microcontroller_id = Column(Integer, primary_key=True)
    name = Column(String)
    mac_address = Column(String)
    model = Column(String)


class BatteryInfo(Base):
    __tablename__ = "battery_info"
    battery_info_id = Column(Integer, primary_key=True)
    battery_id = Column(Integer, ForeignKey("battery.battery_id"))
    unix_timestamp = Column(Integer)
    current = Column(Float)
    voltage = Column(Float)
    charge = Column(Float)
    t1 = Column(Integer)
    t2 = Column(Integer)
    t3 = Column(Integer)
    charge_mos = Column(Boolean)
    discharge_mos = Column(Boolean)
    v1 = Column(Float)
    v2 = Column(Float)
    v3 = Column(Float)
    v4 = Column(Float)
    v5 = Column(Float)
    v6 = Column(Float)
    v7 = Column(Float)
    v8 = Column(Float)
    v9 = Column(Float)
    v10 = Column(Float)
    v11 = Column(Float)
    v12 = Column(Float)
    v13 = Column(Float)
    max_cell_diff = Column(Float)