"""Auxiliary module"""
import colorama
from colorama import Fore, Style
import os
import re

"""Aux module"""


# Function ex_print prints a colorized text based on the message type
def ex_print (type, msg, ret):
	colorama.init()
	# Define color and style constants
	c_error = Fore.RED
	c_action = Fore.YELLOW
	c_ok = Fore.GREEN
	c_white = Fore.WHITE
	s_br = Style.BRIGHT
	s_reset = Style.RESET_ALL
	message = {
		"error": c_error + s_br,
		"action": c_action,
		"positive": c_ok + s_br,
		"info": c_white + s_br,
		"reset": s_reset
	}
	style = message.get(type, s_reset)
	if ret == 0:
		print(style + msg, end = "")
	else:
		print(style + msg)


def banner (version):
	os.system('clear')
	ex_print('error', " ____             _            ______        ___   _", 1)
	ex_print('error', "|  _ \ ___  _   _| |_ ___ _ __|  _ \ \      / / \ | |", 0)
	ex_print('action', '\tRouter PWN tool', 1)
	ex_print('error', "| |_) / _ \| | | | __/ _ \ '__| |_) \ \ /\ / /|  \| |", 0)
	ex_print('action', '\t(C) 2017 Domenico "LilloX" Malorni', 1)
	ex_print('error', '|  _ < (_) | |_| | ||  __/ |  |  __/ \ V  V / | |\  |', 0)
	ex_print('action', '\tlillox[at]rebeldia-lab[dot]net', 1)
	ex_print('error', '|_| \_\___/ \__,_|\__\___|_|  |_|     \_/\_/  |_| \_|', 0)
	ex_print('action', '\thttps://www.domenicomalorni.eu', 1)
	ex_print('action', 'Version :' + version, 1)
	ex_print('info',
	         'Legal disclaimer: Usage of RouterPWN for attacking targets without prior mutual consent is illegal. It is the responsibility of end user to obey all applicable local, state and federal laws.\nDevelopers assume no liability and are not responsible for any misuse or damage caused by this program',
	         1)
	ex_print('reset', '', 1)


# Check if is a Netgear router
def is_netgear (header):
	try:
		realm = (header['WWW-Authenticate'])
		model = re.search('Basic realm="(.+?)"', realm).group(1)
	except:
		try:
			realm = (header['WWW-Authenticate'])
			model = re.search('Digest realm="(.+?) Authentication', realm).group(1)
		except:
			try:
				realm = (header['WWW-Authenticate'])
				model = re.search('Basic realm=(.*)', realm).group(1)
			except:
				return ''
	model = str(model).replace(' ', '_')
	model = model.upper()
	return model


# Check if is a D-Link router
def is_dlink (body):
	global model
	try:
		title = body.select("title")
	except:
		return 0
	else:
		if str(title).upper().find("D-LINK") != "-1":
			# First case: the model name is inside a div of class pp
			try:
				temp = body.find("div", attrs = {'class': 'pp'})
				model = re.search(': (.+?)<a', str(temp)).group(1)
				model = 'D-Link ' + model
			except:
				# Second case: the model name is inside a table of class versionTable
				try:
					temp = body.find("table", attrs = {'class': 'versionTable'})
					t2 = temp.find_all("td")
					model = re.search(' : (.+?)<', str(t2[0])).group(1)
					model = 'D-Link ' + model
				except:
					# Third case: model name is in a variable inside a javascript
					try:
						test = str(body)
						model = re.search("ModemVer='(.+?)'", test).group(1)
						model = 'D-Link ' + model
					except:
						return 0
			return 1
		else:
			return 0


def file_len (fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1
