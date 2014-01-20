from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.python import log
from sql_interface import SQLInterface

import logging


class Handler(LineReceiver):    
    delimiter = b'\n'
    def __init__(self):
        self.sql = SQLInterface("access.sqlite3")
        self.alarm_state = False


    def connectionMade(self):
        peer = self.transport.getPeer()
        self.peer_sock = ":".join([peer.host, str(peer.port)])

    def lineReceived(self, data):
        data_list = data.split(" ")
        log.msg("line recieved: '{}'".format(data),  logLevel=logging.DEBUG)
        if data_list[0].lower() == "request":
            if data_list[1] in self.sql.ls_users():
                log.msg("{} recognised".format(data_list[1]))
                self.alarm_state = not self.alarm_state
                self.sendLine("1")
                self.sql.log_access(data_list[1], self.alarm_state.conjugate())
        else:
            log.msg("ignored command from {}".format(self.peer_sock), logLevel=logging.WARNING)
            self.sendLine("0")
            self.transport.loseConnection()

    def connectionLost(self, reason):
        self.sql.db_connection.commit()


class Factory(Factory):
    def buildProtocol(self, addr):
        return Handler()