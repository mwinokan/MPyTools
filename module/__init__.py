
# import os
# hostname = os.getenv('HOSTNAME')
import socket
hostname = socket.gethostname()
isEureka = hostname.endswith(".swmgmt.eureka")

from .module import module
