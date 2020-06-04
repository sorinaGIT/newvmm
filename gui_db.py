""" gui_db.py """


from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime

Base = declarative_base()

class Record(Base):
    __tablename__ = "RECORDS"

    empty = True

    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    create_date = Column("CREATE_DATE", DateTime, nullable=False,
                         default=datetime.utcnow().replace(microsecond=0))

    # PINS
    pin1u = Column("PIN1U", Float)
    pin1r = Column("PIN1R", Float)
    pin1r_units = Column("PIN1R_UNITS", String)

    pin2u = Column("PIN2U", Float)
    pin2r = Column("PIN2R", Float)
    pin2r_units = Column("PIN2R_UNITS", String)

    pin3u = Column("PIN3U", Float)
    pin3r = Column("PIN3R", Float)
    pin3r_units = Column("PIN3R_UNITS", String)

    pin4u = Column("PIN4U", Float)
    pin4r = Column("PIN4R", Float)
    pin4r_units = Column("PIN4R_UNITS", String)

    pin5u = Column("PIN5U", Float)
    pin5r = Column("PIN5R", Float)
    pin5r_units = Column("PIN5R_UNITS", String)

    pin6u = Column("PIN6U", Float)
    pin6r = Column("PIN6R", Float)
    pin6r_units = Column("PIN6R_UNITS", String)

    pin7u = Column("PIN7U", Float)
    pin7r = Column("PIN7R", Float)
    pin7r_units = Column("PIN7R_UNITS", String)

    pin8u = Column("PIN8U", Float)
    pin8r = Column("PIN8R", Float)
    pin8r_units = Column("PIN8R_UNITS", String)

    pin9u = Column("PIN9U", Float)
    pin9r = Column("PIN9R", Float)
    pin9r_units = Column("PIN9R_UNITS", String)

    pin10u = Column("PIN10U", Float)
    pin10r = Column("PIN10R", Float)
    pin10r_units = Column("PIN10R_UNITS", String)

    pin11u = Column("PIN11U", Float)
    pin11r = Column("PIN11R", Float)
    pin11r_units = Column("PIN11R_UNITS", String)

    pin12u = Column("PIN12U", Float)
    pin12r = Column("PIN12R", Float)
    pin12r_units = Column("PIN12R_UNITS", String)

    pin13u = Column("PIN13U", Float)
    pin13r = Column("PIN13R", Float)
    pin13r_units = Column("PIN13R_UNITS", String)

    pin14u = Column("PIN14U", Float)
    pin14r = Column("PIN14R", Float)
    pin14r_units = Column("PIN14R_UNITS", String)

    pin15u = Column("PIN15U", Float)
    pin15r = Column("PIN15R", Float)
    pin15r_units = Column("PIN15R_UNITS", String)

    pin16u = Column("PIN16U", Float)
    pin16r = Column("PIN16R", Float)
    pin16r_units = Column("PIN16R_UNITS", String)

    pin17u = Column("PIN17U", Float)
    pin17r = Column("PIN17R", Float)
    pin17r_units = Column("PIN17R_UNITS", String)

    pin18u = Column("PIN18U", Float)
    pin18r = Column("PIN18R", Float)
    pin18r_units = Column("PIN18R_UNITS", String)

    pin19u = Column("PIN19U", Float)
    pin19r = Column("PIN19R", Float)
    pin19r_units = Column("PIN19R_UNITS", String)

    auxu = Column("AUXU", Float)
    auxr = Column("AUXR", Float)
    auxr_units = Column("AUXR_UNITS", String)

    # Power
    p1 = Column("P1", Float)
    p1a = Column("P1A", Float)
    p1b = Column("P1B", Float)
    p2 = Column("P2", Float)
    p2a = Column("P2A", Float)
    p2b = Column("P2B", Float)
    p2vmm = Column("P2VMM", Float)

    # I2C
    chip_id = Column("CHIP_ID", String)
    chip_number = Column("CHIP_NUMBER", Integer)
    chip_address = Column("CHIP_ADDRESS", Integer)
    eeprom = Column("EEPROM", Integer)
    uadc1 = Column("UADC1", Integer)
    uadc2 = Column("UADC2", Integer)

    def __repr__(self):
        return "Records ({} {})".format(self.id, self.create_date)

    def fill_data(self, data):
        """ Fill record with (partial) data coming from VMM chip

            Parameters:
            -----------
            data (dict) - data from VMM (p1p2id, mux1, mux3 scripts)
        """
        #
        # Pins
        #
        def get_pin_values(pin):
            """ Helper function to extract pin data from VMM readings"""
            u = data[pin].get("U", None)
            r = data[pin].get("R", None)
            r_units = data[pin].get("Runits", None)
            return u, r, r_units

        def set_pin_values(pin, u, r, r_units):
            """ Helper function to set pin values into Record object"""
            setattr(self, "{pin}u".format(pin=pin), u)
            setattr(self, "{pin}r".format(pin=pin), r)
            setattr(self, "{pin}r_units".format(pin=pin), r_units)

            self.empty = False

        # Fill pin data
        for i in range(1, 20):
            pin = "pin{i}".format(i=i)
            if pin in data:
                u, r, r_units = get_pin_values(pin)
                set_pin_values(pin, u, r, r_units)

        # Exceptional pins
        if "aux" in data:
            u, r, r_units = get_pin_values("aux")
            set_pin_values("aux", u, r, r_units)

        # Power
        power_keys = ["p1", "p1a", "p1b", "p2", "p2a", "p2b", "p2vmm"]

        # I2C
        i2c_keys = ["chip_id", "chip_number",
                    "chip_address", "eeprom", "uadc1", "uadc2"]

        for key in power_keys+i2c_keys:
            if key in data:
                # set attribute of an Record object by key
                setattr(self, key, data[key])
                self.empty = False

    def save(self):
        try:
            engine = create_engine("sqlite:///vmm.sqlite")
            # Create database table(s) if not exists
            Base.metadata.create_all(engine)

            # Prepare for writing
            Session = sessionmaker(bind=engine)
            session = Session()

            # Save
            session.add(self)
            session.commit()

            # Review
            print(self)

        except Exception as e:
            print("Problem writing into database")
            print(e)
