import ipaddress
import socket

from common_ports import ports_and_services

# check hostname and ipaddress
def checkTarget(target):
  if target.split('.')[-1].isdigit():
    try:
      # check ipaddress
      ipaddress.ip_address(target)
    except:
      return "Invalid IP address"
    try:
      # get hostname
      host = socket.gethostbyaddr(target)[0]
      return (host, target)
    except:
      return target
  elif target.split('.')[-1].isalpha():
    try:
      # get ipaddress
      ip = socket.gethostbyname(target)
      return (target, ip)
    except:
      return "Invalid hostname"

def get_open_ports(target, port_range, verbose=False):

  host_ip = checkTarget(target)

  result = ""
  ports = []
  if verbose == True:
    if len(host_ip) == 2:
      # print hostname and ipaddress
      result += "Open ports for " + host_ip[0] + " (" + host_ip[1] + ")"
    else:
      # print ipaddress
      result += "Open ports for " + host_ip
    result += f"\n{'PORT':<9}SERVICE\n"

  for port in range(port_range[0], port_range[1] + 1):
    if port not in ports_and_services:
      continue
      # print("Invalid port")

    # connect with socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    connect = sock.connect_ex((target, port))
    if connect == 0:
      if verbose == True:
        # print port and service
        service = ports_and_services[port]
        result += f"{port:<9}{service}\n"
      else:
        # print port
        # result += f"{port:<9}\n"
        ports.append(port)
    sock.close()

  if verbose == True:
    return result.rstrip()
  else:
    return ports
