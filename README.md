# routerPWN

A tool for exploiting home routers. Needs python 3. Released under GPL v3 license.

### Disclaimer:
This software is designed **only** for testing purposes and POC. It contains no 0-day, only vulnerabilities/exploits  that have been submitted to vendors and fixed.

`Usage of RouterPWN for attacking targets without prior mutual consent is illegal. It is the responsibility of end user to obey all applicable local, state and federal laws.
Developer assumes no liability and are not responsible for any misuse or damage caused by this program
`

I'm not a developer as you can see inside my code. I developed this tools as a PoC for a friend and to improve a little bit my developer skills.

### Description:
This tool takes advantage of known vulnerabilities that allow you to recover the admin password for various routers and modems that expose a web administration interface. 
The tool also performs tests to check whether it is set to default password.

### Installation:
Simply clone the repo and install the dependencies:
```bash
pip install -r requirements
```

### Usage:
```bash
usage: routerPwn.py [-h] (-i INPUT_IP | -l INPUT_FILE) [-o OUTPUT_FILE]

Two operational modes: Signle IP\IP List

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_IP, --ip INPUT_IP
                        Single ip to test. No protocol or port
  -l INPUT_FILE, --list INPUT_FILE
                        List of ip to test. No protocol or port
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        Output credentials found to file

Examples:
Single ip check and output to file:
	routerPwn.py -i 192.168.0.1 -o out.txt
Check list of ip and write results on the test.out file
	routerPwn.py -l ip_list.txt -o test.out

You have to specify -i OR -l. Output use is optional
```

### Affected brand/model
See Vulnerabilities and History files