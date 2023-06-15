from database import mydb
from src import User
print(attributes.loc[1]+attributes.loc[17])


class Character(User):
    def __init__(self,id_user,id,class_character,level,xp,race,backgroud,alignment,faction):
        super().__init__(id=id_user)
        self._id=id
        self.class_character=class_character
        self.level=level
        self.xp=xp
        self.race=race
        self.background=backgroud
        self.alignment=alignment
        self.faction=faction