import requests
import json
from datetime import datetime
import argparse


box_ids = list()
headers = {
		'accept': 'application/json',
		'api_key': 'api_key',
		'Content-Type': 'application/json'
	}

def add_box(value, boxes):
	resBox = requests.get('http://{}/utxo/byIdBinary/{}'.format(ip, str(value['box']['boxId'])), headers=headers).json()
	boxes.append(resBox["bytes"])
	box_ids.append(str(value['box']['boxId']))
	return value['box']['value']
		

def check(ip, fee, res, oracle_address, merge_to_address, max_value, max_box, min_box, check_param):
	boxes = list()
	batchs_boxes = list()
	valreq = 0
	for count, value in enumerate(res):
		if len(boxes) < max_box:
			if not (str(value['box']['boxId'])) in box_ids and value['address'] == oracle_address and value['box']['value'] <= max_value:
				valreq += add_box(value, boxes)
		elif len(boxes) >= max_box:
			batchs_boxes.append({
				"boxes": boxes,
				"value": int(valreq - fee)
			})
			boxes = list()
			valreq = 0
			if value['address'] == oracle_address and value['box']['value'] <= max_value:
				valreq += add_box(value, boxes)
	batchs_boxes.append({
		"boxes": boxes,
		"value": int(valreq - fee)
	})

	for batch_boxes in batchs_boxes:
		if not batch_boxes['value'] > (fee * 2) or not len(batch_boxes['boxes']) >= min_box:
			log('There is not enough balance / box according to conditions for merge this group boxes, now there are {} ERG and {} box'.format((batch_boxes['value'] / 1e9), len(batch_boxes['boxes'])))
			exit(0)
		out = {
			"requests": [
				{
					"address": merge_to_address,
					"value": batch_boxes['value']
				}
			],
				"fee": fee,
				"inputsRaw": batch_boxes['boxes']
		}
		log("value of transaction is {} with fee {} number of input is {} to addresss:\n{}".format(batch_boxes['value'] / 1e9, fee / 1e9, len(batch_boxes['boxes']), merge_to_address))
		
		if check_param:
			while True:
				val_in = input('Is ok send transaction (y/n):\n')
				log("input is: {}".format(val_in))
				if str(val_in) in ["y", "Y", "yes", "YES"]:
					res = requests.post('http://{}/wallet/transaction/send'.format(ip), headers=headers, data=json.dumps(out)).json()
					log("sent transaction with id:" + res)
					break
				elif str(val_in) in ["n", "N", "no", "NO"]:
					log("END")
					exit(0)
		else:
			res = requests.post('http://{}/wallet/transaction/send'.format(ip), headers=headers, data=json.dumps(out)).json()
			log("sent transaction with id:" + res)
	exit(0)


class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ', '.join(action.option_strings) + ' ' + args_string

fmt = lambda prog: CustomHelpFormatter(prog)
parser = argparse.ArgumentParser(formatter_class=fmt, description='Merge oracle box.')

parser.add_argument('--ip', '-i', metavar='127.0.0.1:9053', type=str, required=True, help='Your node ip')
parser.add_argument('--apiKey', '-k', metavar='hello', type=str, required=True, help='Your node api-key')
parser.add_argument('--oracleAddress', '-o', metavar='9fzRcctiWfzoJyqGtPWqoXPuxSmFw6zpnjtsQ1B6jSN514XqH4q', type=str, required=True, help='Your oracle address')
parser.add_argument('--mergeToAddress', '-m', metavar='9fzRcctiWfzoJyqGtPWqoXPuxSmFw6zpnjtsQ1B6jSN514XqH4q', type=str, required=False, default='', help='your destination address (optional: default is your \'oracleAddress\')')
parser.add_argument('--fee', '-f', metavar='0.0011', type=float, default=0.0011, required=False, help='Fee for send transaction (optional: default is %(default)s)')
parser.add_argument('--maxValue', '-b', metavar='0.18', type=float, default=0.02, required=False, help='The box must have a maximum of \'maxValue\' erg to participate in the transaction (optional: default is %(default)s)')
parser.add_argument('--maxBox', '-bx', metavar='50', type=int, default=50, required=False, help='The maximum number of boxes that can be present in a transaction (optional: default is %(default)s)')
parser.add_argument('--minBox', '-bn', metavar='30', type=int, default=30, required=False, help='The minimum number of boxes that can be present in a transaction (optional: default is %(default)s)')
parser.add_argument('--check', '-c', default=False, action='store_true', required=False, help='This parameter help to check information of tx before send it and question for send or no TX (optional: default is %(default)s)')

args = parser.parse_args()


ip = args.ip
fee = int(args.fee * 1e9)
max_value = int(args.maxValue * 1e9)
headers['api_key'] = args.apiKey
oracle_address = args.oracleAddress
merge_to_address = oracle_address if args.mergeToAddress == '' else args.mergeToAddress
max_box = args.maxBox
min_box = args.minBox
check_param = args.check

def log(text):
	log_file = open("./merge_oracle_box.log", "a")
	aDict = {"time": str(datetime.now()), "message": text}
	print(text)
	log_file.write(json.dumps(aDict) + "\n")
	log_file.close()
	

try:
	log("START APP:")
	res = requests.get('http://{}/wallet/boxes/unspent'.format(ip), headers=headers).json()
	check(ip, fee, res, oracle_address, merge_to_address, max_value, max_box, min_box, check_param)
except Exception as err:
	log("Unexpected error:" + str(err))
