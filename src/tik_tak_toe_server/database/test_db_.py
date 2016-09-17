import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Panel


class TestQuery(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = Session(engine)
        Base.metadata.create_all(self.engine)
        self.panel = Panel(1, 'ion torrent', 'start')
        self.session.add(self.panel)
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_query_panel(self):
        expected = [self.panel]
        result = self.session.query(Panel).all()
        self.assertEqual(result, expected)