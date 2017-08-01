#!/usr/bin/python3
"""Classes Module"""
import aux
import socket
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup
import sys
import exploit


# definition of the options object
class Options:
	single_ip = True
	ip = ''
	list_mode = False
	list_file = ''
	o_file = False
	o_file_name = ''


# definition of the router object
class Router:
	brand = ''
	model = ''
	ip = ''
	port = ''
	url = ''
	vulnerable = False
	exploit = ''
	default_login = False
	username = ''
	password = ''
	open_ports = []
	body = ''
	header = ''
	__default_ports = ['8443', '8080', '7547', '8181', '9000', '8888', '80', '443', '8081', '8001']
	found = False
	__is_linksys = False
	__ssl = False

	# This function check if the given port is or not open
	def __is_open (self, port):
		s = socket.socket()
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(1)
			r = s.connect_ex((self.ip, int(port)))
			if r == 0:
				s.close()
				return 1
			s.close()
			return 0
		except:
			s.close()
			return 0

	# Check if there is a running a webserver and if it is know
	def __check_webserver (self, opt):
		for t in self.__default_ports:
			if self.__is_open(t) == 1:
				self.open_ports.append(t)
		if not len(self.open_ports) > 0:
			aux.ex_print('error', '\t[-] Web server not found', '1')
			return 1
		aux.ex_print('positive', '\t[+] Found open ports: ' + str(self.open_ports), '1')
		protocol = ["http://", "https://"]
		# Try every combination of port/protocol to find an usable web server
		for port in self.open_ports:
			for prot in protocol:
				try:
					url_to_test = prot + self.ip + ':' + port
					r = requests.get(url_to_test, verify = False, timeout = 3)
				except requests.exceptions.RequestException as e:
					aux.ex_print('error', 'DEBUG: Error in request', 1)
					pass
				else:
					self.body = BeautifulSoup(r.text, 'lxml')
					self.header = r.headers
					# we have found a webserver on the open port
					aux.ex_print('positive', '\t[+] Found web server: ' + url_to_test, '1')
					self.url = url_to_test
					# try to detect if is a netgear, a dlink...
					aux.ex_print('action', '[*] Try to identify brand/model...', 1)
					if aux.is_netgear(self.header) != '':
						self.netgear = True
						self.model = aux.is_netgear(self.header)
						self.port = port
						aux.ex_print('positive', '\t[+] Found Brand/Model : ' + self.model, '1')
						aux.ex_print('action', '[*] Check default creds ...', '1')
						if exploit.login_act(self) == 1:
							r.close()
							return 1
						else:
							aux.ex_print('action', '[*] Search for exploit ...', '1')
							exploit.exploit_act(self)
							r.close()
						return 1
					elif aux.is_dlink(self.body):
						self.dlink = True
						self.model = aux.model
						r.close()
						return 1
					r.close()
		return 0

	# When the router object is initialized we check for brand/model
	def __init__ (self, opt):
		self.ip = opt.ip
		self.open_ports = []
		aux.ex_print('info', '\nTesting: ' + self.ip, 1)
		aux.ex_print('action', '[*] Try to detect web server on default ports...', 1)
		if self.__check_webserver(opt) == 0:
			aux.ex_print('error', '\t[-] Brand/Model not found! ', '1')
