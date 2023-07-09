from schemas.register import Register
from models.register import Register as RegisterModel

class RegisterService():
    def __init__(self, db) -> None:
        self.db = db

    def get_registers(self):
        result = self.db.query(RegisterModel).all()

        return result

    def get_register(self, id: int):
        result = self.db.query(RegisterModel).filter(RegisterModel.id == id).first()

        return result

    def create_register(self, register: Register) -> None:
        new_register = RegisterModel(**register.dict())

        self.db.add(new_register)
        self.db.commit()

        return

    def update_register(self, id: int, meassure: float) -> None:
        result = self.db.query(RegisterModel).filter(RegisterModel.id == id).first()

        result.meassure = meassure

        self.db.commit()

        return

    def update_registers(self, meassures: list) -> None:
        
        for id in range(len(meassures)):
            update_register(id=id, meassure= meassures[id])

        return

    def delete_register(self, id: int) -> None:
        result = self.db.query(RegisterModel).filter(RegisterModel.id == id).first()

        self.db.delete(result)
        self.db.commit()

        return

    def modify_register(self, id: int, register: Register) -> None:
        result = self.db.query(RegisterModel).filter(RegisterModel.id == id).first()

        result.id = register.id
        result.register_name = register.register_name
        result.meassure = register.meassure
        result.meassure_unit = register.meassure_unit

        self.db.commit()

        return





    