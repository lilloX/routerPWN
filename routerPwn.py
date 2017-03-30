import argparse
import classes
import aux
import sys

global __version__
__version__ = '0.5 alpha'
__author__ = 'Domenico "LilloX" Malorni'

script_name = sys.argv[0]

parser = argparse.ArgumentParser(description = 'Two operational modes: Signle IP\IP List',
                                 usage = aux.banner(__version__),
                                 epilog = 'Examples:\nSingle ip check and output to file:\n\t' + script_name + ' -i 192.168.0.1 -o out.txt\nCheck list of ip and write results on the test.out file' +
                                          '\n\t' + script_name + ' -l ip_list.txt -o test.out\n\nYou have to specify -i OR -l. Output use is optional',
                                 formatter_class = argparse.RawTextHelpFormatter)
group = parser.add_mutually_exclusive_group(required = True)
group.add_argument("-i", '--ip', help = "Single ip to test. No protocol or port", dest = "input_ip")
group.add_argument("-l", '--list', help = "List of ip to test. No protocol or port", dest = "input_file")
parser.add_argument("-o", "--output", help = "Output credentials found to file ", dest = "output_file")
args = parser.parse_args()

opt = classes.Options

if args.input_ip:
	opt.single_ip = True
	opt.list_mode = False
	opt.ip = args.input_ip

if args.input_file:
	opt.single_ip = False
	opt.list_mode = True
	opt.list_file = args.input_file

if args.output_file:
	opt.o_file = True
	opt.o_file_name = args.output_file

aux.banner(__version__)
if opt.single_ip:
	router = classes.Router(opt)
	del router
else:
	i = 0
	with open(opt.list_file, 'r') as ip_list:
		for line in ip_list:
			i += 1
			line = line.replace("\n", "")
			opt.ip = line
			aux.ex_print("info", "Processing IP number " + str(i) + " of " + str(aux.file_len(opt.list_file)), 1)
			router = classes.Router(opt)
			router.open_ports = []
			# Write to outfile the results even the router is not exploitable
			if opt.o_file:
				output = open(opt.o_file_name, 'a')
				if router.vulnerable:
					output.writelines(router.model + ',' + router.ip + ',' + router.port + ',' + str(
							router.vulnerable) + ',' + router.exploit + ',' + router.username + ',' + router.password + '\n')
				else:
					if router.model != '':
						output.writelines(
								router.model + ',' + router.ip + ',' + router.port + ',' + router.exploit + '\n')
			del router
	output.close()
	ip_list.close()
