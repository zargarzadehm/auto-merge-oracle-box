# Auto merger box with ergo node

This code developed for merge reward oracle box with [ergo node](http://github.com/ergoplatform).

## Setup
### Prerequisite
  * python:3.+
### Getting Started

First clone the repository from Github and switch to the new directory:
```
$ git clone https://github.com/zargarzadehm/reward-oracle-merger-ergo
$ cd reward-oracle-merger-ergo
```

Install project dependencies:
```
$ pip3 install -r requirements.txt
```

Use `--help` or `-h` for see options:
```
$ python3 mergeOracle.py --help
```
```
usage: mergeOracle.py [-h] --ip 127.0.0.1:9053 --apiKey hello --oracleAddress
                      9fzRcctiWfzoJyqGtPWqoXPuxSmFw6zpnjtsQ1B6jSN514XqH4q
                      [--mergeToAddress 9fzRcctiWfzoJyqGtPWqoXPuxSmFw6zpnjtsQ1B6jSN514XqH4q]
                      [--fee 0.0011] [--maxValue 0.18] [--maxBox 50]
                      [--minBox 30] [--check]

Merge oracle box.

optional arguments:
  -h, --help            show this help message and exit
  --ip, -i 127.0.0.1:9053   Your node ip
  --apiKey, -k hello    Your node api-key
  --oracleAddress, -o 9fzRcctiWfzoJyqGtPWqoXPuxSmFw6zpnjtsQ1B6jSN514XqH4q Your oracle address
  --mergeToAddress, -m 9fzRcctiWfzoJyqGtPWqoXPuxSmFw6zpnjtsQ1B6jSN514XqH4q  your destination address (optional: default is your 'oracleAddress')
  --fee, -f 0.0011      Fee for send transaction (optional: default is 0.0011)
  --maxValue, -b 0.18   The box must have a maximum of 'maxValue' erg enough to participate in the transaction (optional: default
                        is 0.02)
  --maxBox, -bx 50      The maximum number of boxes that can be present in a transaction (optional: default is 50)
  --minBox, -bn 30      The minimum number of boxes that can be present in a transaction (optional: default is 30)
  --check, -c           This parameter help to check information of tx before send it and question for send or no TX (optional: default is False)
```

For start service with best practice options using this:

Note: Tokens are not handled in this source code, so `Don't run` this code on the addresses where you keep your tokens, it will be possible to burn tokens.
```
$ python3 auto_merge_oracle_box.py -i YOUR_NODE_ADDRESS -k YOUR_API_KEY -o YOUR_ORACLE_ADDRESS
```
Example:
```
$ python3 auto_merge_oracle_box.py -i 127.0.0.1:9053 -k hello -o 9fzRcctiWfzoJyqGtPWqoXPuxSmFw6zpnjtsQ1B6jSN514XqH4q
```
