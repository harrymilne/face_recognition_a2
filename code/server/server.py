from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.python import log
from sql_interface import SQLInterface

import logging

class Handler(LineReceiver):    
    delimiter = b'\n'
    def __init__(self, parent):
        self.parent = parent
        self.sql = SQLInterface("access.sqlite3")

    def connectionMade(self):
        peer = self.transport.getPeer()
        self.peer_sock = ":".join([peer.host, str(peer.port)])

    def lineReceived(self, data):
        data_list = data.split(" ")
        log.msg("line recieved: '{}'".format(data),  logLevel=logging.DEBUG)
        if data_list[0].lower() == "request":
            if data_list[1] in self.sql.ls_users():
                log.msg("{} recognised".format(data_list[1]))
                self.parent.STATE = not self.parent.STATE
                log.msg("state toggled to {}".format(self.parent.STATE))
                if self.parent.STATE:
                    self.sendLine("ALARM ON")
                else:
                    self.sendLine("ALARM OFF")
                self.sql.log_access(data_list[1], self.parent.STATE.conjugate())
        elif data_list[0].lower() == "state":
            self.sendLine("{}".format(self.parent.STATE))
        else:
            log.msg("ignored command from {}".format(self.peer_sock), logLevel=logging.WARNING)
            self.sendLine("FAILED")
            self.transport.loseConnection()

    def connectionLost(self, reason):
        self.sql.db_connection.commit()


class Factory(Factory):
    STATE = False
    def buildProtocol(self, addr):
        return Handler(self)
