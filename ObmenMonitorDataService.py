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

class ObmenCurrentErrorItem(Base):
     __tablename__ = u'obmen_current_error'

     client_id = Column(String, primary_key=True)
     period = Column(DateTime, primary_key=True)
     uzelib = Column(String, primary_key=True)

     Data_posl_zagr = Column(DateTime)
     Data_posl_vigr = Column(DateTime)
     Rezult_posl_zagr = Column(String)
     Rezult_posl_vigr = Column(String)

     Comment_zagruzka = Column(String)
     Comment_vigruzka = Column(String)

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
                    Comment_vigruzka=self.Comment_vigruzka)

class ObmenCurrentStatusItem(Base):
     __tablename__ = u'obmen_current_status'

     client_id = Column(String, primary_key=True)
     uzelib = Column(String, primary_key=True)

     Data_posl_zagr = Column(DateTime)
     Data_posl_vigr = Column(DateTime)
     Rezult_posl_zagr = Column(String)
     Rezult_posl_vigr = Column(String)

     Comment_zagruzka = Column(String)
     Comment_vigruzka = Column(String)

     Last_exchange = Column(DateTime)

     def __init__(self, client_id, uzelib):
         self.client_id = client_id
         self.uzelib = uzelib

     def __repr__(self):
        return "<ObmenStatusItem id='%s'('%s')>" % (self.client_id, self.Last_exchange)

     def getDictonary(self):
        return dict(client_id=self.client_id, uzelib=self.uzelib, Data_posl_zagr=self.Data_posl_zagr,
                    Data_posl_vigr=self.Data_posl_vigr, Rezult_posl_zagr=self.Rezult_posl_zagr,
                    Rezult_posl_vigr=self.Rezult_posl_vigr, Comment_zagruzka=self.Comment_zagruzka,
                    Comment_vigruzka=self.Comment_vigruzka, Last_exchange=self.Last_exchange)

     def getJSData(self):
         return {'client_id':      self.client_id,
                 'uzelib':         self.uzelib,
                 'Data_posl_zagr': self.Data_posl_zagr.strftime('%Y-%m-%d %H:%M:%S'),
                 'Data_posl_vigr': self.Data_posl_vigr.strftime('%Y-%m-%d %H:%M:%S'),
                 'Rezult_posl_zagr':self.Rezult_posl_zagr,
                 'Rezult_posl_vigr':self.Rezult_posl_vigr,
                 'Comment_zagruzka':self.Comment_zagruzka,
                 'Comment_vigruzka':self.Comment_vigruzka,
                 'Last_exchange'   :self.Last_exchange.strftime('%Y-%m-%d %H:%M:%S')}


class ObmenLogClient(Base):
     __tablename__ = u'obmen_client'

     client_id = Column(String, primary_key=True)
     client_name = Column(String)
     client_has_error = Column(Integer)

     def __init__(self, client_id, name):
         self.client_id = client_id
         self.client_name = name
         self.client_has_error = 0

     def __repr__(self):
        return "<Client id='%s'('%s')>" % (self.client_id, self.client_name)

     def getDictonary(self):
        return dict(client_id=self.client_id, client_name=self.client_name, client_has_error=self.client_has_error)

class ObmenMonitorService():

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self):
        self.session.close()

    def getObmenLogItems(self):
        #log_items = self.session.query(ObmenLogItem).order_by(ObmenLogItem.period.desc()).all()
        #log_items = self.session.query(ObmenLogItem, ObmenLogClient).outerjoin(ObmenLogClient, ObmenLogClient.client_id==ObmenLogItem.client_id).order_by(ObmenLogItem.period.desc()).slice(0,30)
        log_items = self.session.query(ObmenLogItem).order_by(ObmenLogItem.period.desc()).slice(0,30)
        #log_items = ObmenLogItem.query.order_by(ObmenLogItem.period.desc()).all()
        entries = [s.getDictonary() for s in log_items]
        return entries

    def addObmenLogItem(self,log_item):

        #self.session.add(log_item)
        self.session.merge(log_item)
        self.session.commit()

    def addObmenErrorItem(self,error_item):

        #self.session.add(log_item)
        self.session.merge(error_item)
        self.session.commit()

    def addClientItem(self,client_item):

        instance = self.session.query(ObmenLogClient).filter_by(client_id=client_item.client_id).first()

        if instance:
            return instance
        else:
            self.session.add(client_item)
            self.session.commit()
            return instance

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

    def updateCurrentStatus(self,status_item):
        self.session.merge(status_item)
        self.session.commit()

    def getObmenCurrentStatus(self, client_id, uzelib):
        current_status = self.session.query(ObmenCurrentStatusItem).filter_by(client_id=client_id, uzelib=uzelib).one()
        return current_status

    def getObmenStatusForClient(self, client_id):
        current_status_items = self.session.query(ObmenCurrentStatusItem).filter_by(client_id=client_id)
        entries = [s.getJSData() for s in current_status_items]
        return entries


def main():
    #metadata.drop_all()
    metadata.create_all()

    obmenMonitorService= ObmenMonitorService()
    #obmenMonitorService.updateClient(ObmenLogClient('123123','First client'))
    #current_status = obmenMonitorService.getObmenStatusForClient('5d857ac7-e265-446b-aa40-6741b17873fe')
    #print current_status

if __name__ == '__main__':
    main()