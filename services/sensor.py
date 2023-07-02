from minimalmodbus import Instrument # Documentation: https://minimalmodbus.readthedocs.io/en/stable/readme.html
from models.instrument import Instrument as InstrumentModel
from schemas.instrument import Instrument

# Set up the serial port. Terminales 10 (GND), 11 (data -), 12 (data +).
# Manual ITC-650: Z:\Sistema de Gestión de Calidad\SGC\Coordinación del SGC\Documentos externos\Información técnica\Manual ITC-650

itc_650 = Instrument('COM5', slaveaddress=1, mode='rtu') # Device port, slave address and mode
itc_650.serial.baudrate = 115200
itc_650.serial.bytesize = 8
itc_650.serial.parity = minimalmodbus.serial.PARITY_NONE
itc_650.serial.timeout = 0.05 # I'm not sure if i'ts necessary.

y = [register/100 for register in itc_650.read_registers(registeraddress=1, number_of_registers=len(x))] # Lectura de los registros, iniciando desde el 01h hasta la longitud de la lista x, agregando los puntos decimales.
                                                                                # 01h--> y[0]: P-ACID-1095. Terminales 23 (+) y 35 (-).
                                                                                # 02h--> y[1]: P-ACID-1095 M. Terminales 22 (+) y 34 (-).
                                                                                # 03h--> y[2]: ÁCIDO NÍTRICO. Termiales 21 (+) y 33 (-).

class InstrumentService():
    def __init__(self, db) -> None:
        self.db = db

    def get_instruments(self):
        result = self.db.query(InstrumentModel).all()

        return result

    def get_instrument(self, slaveaddress: int):
        result = self.db.query(InstrumentModel).filter(InstrumentModel.slaveaddress == slaveaddress).first()

        return result

    def create_instrument(self, instrument: Instrument) -> None:
        new_instrument = InstrumentModel(**instrument.dict())

        self.db.add(new_instrument)
        self.db.commit()

        return

    def modify_instrument(self, slaveaddress: int, instrument: Instrument) -> None:
        result = self.db.query(InstrumentModel).filter(InstrumentModel.slaveaddress == slaveaddress).first()

        
        result.instrument_name = instrument.instrument_name
        result.port = instrument.port
        result.mode = instrument.mode
        result.baudrate = instrument.baudrate
        result.bytesize = instrument.bytesize
        result.parity = instrument.parity

        self.db.commit()

        return

    def delete_instrument(self, slaveaddress) -> None:
        result = self.db.query(InstrumentModel).filter(nstrumentModel.slaveaddress == slaveaddress).first()

        self.db.delete(result)
        self.db.commit()

        return

    def connect_instrument(self, slaveaddress) -> None:
        result = self.db.query(InstrumentModel).filter(nstrumentModel.slaveaddress == slaveaddress).first()

        itc_650 = Instrument('COM5', slaveaddress=1, mode='rtu') # Device port, slave address and mode
        itc_650.serial.baudrate = 115200
        itc_650.serial.bytesize = 8
        itc_650.serial.parity = minimalmodbus.serial.PARITY_NONE
        itc_650.serial.timeout = 0.05 # I'm not sure if i'ts necessary.
        
        return