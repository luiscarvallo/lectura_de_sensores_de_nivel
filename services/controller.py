from minimalmodbus import Instrument, serial # Documentation: https://minimalmodbus.readthedocs.io/en/stable/readme.html
from models.controller import Controller as ControllerModel
from schemas.controller import Controller
from models.register import Controller as RegisterModel

# Set up the serial port. Terminales 10 (GND), 11 (data -), 12 (data +).
# Manual ITC-650: Z:\Sistema de Gestión de Calidad\SGC\Coordinación del SGC\Documentos externos\Información técnica\Manual ITC-650

itc_650 = Instrument('COM5', slaveaddress=1, mode='rtu') # Device port, slave address and mode
itc_650.serial.baudrate = 115200
itc_650.serial.bytesize = 8
itc_650.serial.parity = serial.PARITY_NONE
itc_650.serial.timeout = 0.05 # I'm not sure if i'ts necessary.

class ControllerService():
    def __init__(self, db) -> None:
        self.db = db

    def get_controllers(self):
        result = self.db.query(ControllerModel).all()

        return result

    def get_controller(self, slaveaddress: int):
        result = self.db.query(ControllerModel).filter(ControllerModel.slaveaddress == slaveaddress).first()

        return result

    def create_controller(self, controller: Controller) -> None:
        new_controller = ControllerModel(**controller.dict())

        self.db.add(new_controller)
        self.db.commit()

        return

    def modify_controller(self, slaveaddress: int, controller: Controller) -> None:
        result = self.db.query(ControllerModel).filter(ControllerModel.slaveaddress == slaveaddress).first()

        
        result.name = controller.name
        result.port = controller.port
        result.mode = controller.mode
        result.baudrate = controller.baudrate
        result.bytesize = controller.bytesize
        result.parity = controller.parity

        self.db.commit()

        return

    def delete_controller(self, slaveaddress) -> None:
        result = self.db.query(ControllerModel).filter(ControllerModel.slaveaddress == slaveaddress).first()

        self.db.delete(result)
        self.db.commit()

    def read_registers(self):
        y = [register/100 for register in itc_650.read_registers(registeraddress=1, number_of_registers=db.query(RegisterModel).count())] # Lectura de los registros, iniciando desde el 01h hasta la longitud de la lista x, agregando los puntos decimales.
                                                                                                                 # 01h--> y[0]: P-ACID-1095. Terminales 23 (+) y 35 (-).
                                                                                                                 # 02h--> y[1]: P-ACID-1095 M. Terminales 22 (+) y 34 (-).
                                                                                                                 # 03h--> y[2]: ÁCIDO NÍTRICO. Termiales 21 (+) y 33 (-).

        return
    
    def update_register(self, )