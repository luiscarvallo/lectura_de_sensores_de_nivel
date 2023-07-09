from pyModbusTCP import ModbusClient
from models.controller import Controller as ControllerModel
from schemas.controller import Controller

# Set up the serial port. Terminales 10 (GND), 11 (data -), 12 (data +).
# Manual ITC-650: Z:\Sistema de Gestión de Calidad\SGC\Coordinación del SGC\Documentos externos\Información técnica\Manual ITC-650

class ControllerService():
    def __init__(self, db) -> None:
        self.db = db

    def get_controllers(self):
        result = self.db.query(ControllerModel).all()

        return result

    def get_controller(self, id: int):
        result = self.db.query(ControllerModel).filter(ControllerModel.id == id).first()

        return result

    def create_controller(self, controller: Controller) -> None:
        new_controller = ControllerModel(**controller.dict())

        self.db.add(new_controller)
        self.db.commit()

        return

    def modify_controller(self, id: int, controller: Controller) -> None:
        result = self.db.query(ControllerModel).filter(ControllerModel.id == id).first()

        result.id = controller.id
        result.host = controller.host
        result.port = controller.port

        self.db.commit()

        return

    def delete_controller(self, id) -> None:
        result = self.db.query(ControllerModel).filter(ControllerModel.id == id).first()

        self.db.delete(result)
        self.db.commit()

        return