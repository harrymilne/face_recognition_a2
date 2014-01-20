from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

class Greeter(Protocol):
    def sendMessage(self, msg):
        self.transport.write(msg + "\n")


def gotProtocol(p):
    p.sendMessage("request harry")
    

point = TCP4ClientEndpoint(reactor, "localhost", 25000)
d = connectProtocol(point, Greeter())
d.addCallback(gotProtocol)
reactor.run()
