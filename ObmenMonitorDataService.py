# -*- coding: utf-8 -*-
import os
from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, Date, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import backref, relation

ROOT_PATH=os.path.dirname(__file__)

#engine = create_engine('sqlite:///'+ROOT_PATH+'data.db', echo=True)
engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base(engine)
metadata = Base.metadata

class ObmenLogItem(Base):
     __tablename__ = u'obmen_log'

     client_id = Column(String, primary_key=True)
     period = Column(DateTime, primary_key=True)
     uzelib = Column(String, primary_key=True)

     Data_posl_zagr = Column(DateTime)
     Data_posl_vigr = Column(DateTime)
     Rezult_posl_zagr = Column(String)
     Rezult_posl_vigr = Column(String)

     Comment_zagruzka = Column(String)
     Comment_vigruzka = Column(String)

     Data_nachala_posl_zagr = Column(DateTime)
     Data_nachala_posl_vigr = Column(DateTime)

     def __init__(self, client_id, period, uzelib):
         self.client_id = client_id
         self.period = period
         self.uzelib = uzelib

     def __repr__(self):
        return "<ObmenLogItem id='%s'('%s','%s')>" % (self.client_id, self.period, self.uzelib)

     def getDictonary(self):
        return dict(client_id=self.client_id, period=self.period, uzelib=self.uzelib, Data_posl_zagr=self.Data_posl_zagr,
                    Data_posl_vigr=self.Data_posl_vigr, Rezult_posl_zagr=self.Rezult_posl_zagr,
                    Rezult_posl_vigr=self.Rezult_posl_vigr, Comment_zagruzka=self.Comment_zagruzka,
                    Comment_vigruzka=self.Comment_vigruzka, Data_nachala_posl_zagr=self.Data_nachala_posl_zagr,
                    Data_nachala_posl_vigr=self.Data_nachala_posl_vigr)

class ObmenLogClient(Base):
     __tablename__ = u'obmen_client'

     client_id = Column(String, primary_key=True)
     client_name = Column(String)

     def __init__(self, client_id, name):
         self.client_id = client_id
         self.client_name = name

     def __repr__(self):
        return "<Client id='%s'('%s')>" % (self.client_id, self.client_name)

     def getDictonary(self):
        return dict(client_id=self.client_id, client_name=self.client_name)


class ObmenMonitorService():

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self):
        self.session.close()

    def getObmenLogItems(self):
        #log_items = self.session.query(ObmenLogItem).order_by(ObmenLogItem.period.desc()).all()
        log_items = self.session.query(ObmenLogItem).order_by(ObmenLogItem.period.desc()).slice(1,30)
        #log_items = ObmenLogItem.query.order_by(ObmenLogItem.period.desc()).all()
        entries = [s.getDictonary() for s in log_items]
        return entries

    def addObmenLogItem(self,log_item):

        #self.session.add(log_item)
        self.session.merge(log_item)
        self.session.commit()

    def addClientItem(self,client_item):

        #self.session.add(log_item)
        self.session.merge(client_item)
        self.session.commit()

    def getObmenClients(self):
        client_items = self.session.query(ObmenLogClient).all()
        #log_items = ObmenLogItem.query.order_by(ObmenLogItem.period.desc()).all()
        entries = [s.getDictonary() for s in client_items]
        return entries

    def getClientByID(self, client_id):
        client = self.session.query(ObmenLogClient).filter_by(client_id=client_id).one()
        return client

    def updateClient(self,client_item):
        self.session.merge(client_item)
        self.session.commit()

def main():

    metadata.create_all()
    obmenMonitorService= ObmenMonitorService()
    #obmenMonitorService.updateClient(ObmenLogClient('123123','First client'))
 
if __name__ == '__main__':
    main()