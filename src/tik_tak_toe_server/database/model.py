from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))


class Board(Base):
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    player_x = Column(Integer, ForeignKey("player.id"))
    player_y = Column(Integer, ForeignKey("player.id"))
    cell_1 = Column(String(1))
    cell_2 = Column(String(1))
    cell_3 = Column(String(1))
    cell_4 = Column(String(1))
    cell_5 = Column(String(1))
    cell_6 = Column(String(1))
    cell_7 = Column(String(1))
    cell_8 = Column(String(1))
    cell_9 = Column(String(1))
    
    def __init__(self, name):
        self.name = name