from twisted.internet import reactor
from twisted.python import log
from ConfigParser import ConfigParser
import server
import logging
import os



if __name__ == "__main__":
    config = ConfigParser()
    config.read("server.cfg")
    if not os.path.exists("logs"):
        os.mkdir("logs")
    observer = log.PythonLoggingObserver()
    observer.start()
    if config.getboolean("logs", "debug"):
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    log_path = config.get("logs", "log_path")
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    
    logging.basicConfig(
        filename="/".join([log_path, "server.log"]), 
        level=log_level, 
        format="%(asctime)s%(levelname)s:%(message)s", 
        datefmt="[%d/%m/%y %H:%M]")
    console = logging.StreamHandler()
    console.setLevel(log_level)
    formatter = logging.Formatter('%(name)-10s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    port = config.getint("network", "port")
    reactor.listenTCP(port, server.Factory())
    reactor.run()
