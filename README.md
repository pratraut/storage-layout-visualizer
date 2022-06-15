# Visualize
```
             88                                      88  88                         
             ""                                      88  ""                         
                                                     88                             
8b       d8  88  ,adPPYba,  88       88  ,adPPYYba,  88  88  888888888   ,adPPYba,  
`8b     d8'  88  I8[    ""  88       88  ""     `Y8  88  88       a8P"  a8P_____88  
 `8b   d8'   88   `"Y8ba,   88       88  ,adPPPPP88  88  88    ,d8P'    8PP"""""""  
  `8b,d8'    88  aa    ]8I  "8a,   ,a88  88,    ,88  88  88  ,d8"       "8b,   ,aa  
    "8"      88  `"YbbdP"'   `"YbbdP'Y8  `"8bbdP"Y8  88  88  888888888   `"Ybbd8"'  
                                                                                
                              Author: savi0ur

Helps in Visualizing storage layout of state variables in solidity
v1.0
```
Tool to visualize storage layout of a state variables in solidity contracts

## Pre-requisite
* Install all the modules from `requirements.txt` using `pip3 install -r requirements.txt`
* Select solc version between `>=0.4.0 <0.9.0`:
  1. Install solc version using `solc-select install <solc-version>`
  2. Use solc version installed using `solc-select use <solc-version>`
  
## Usage
```
$ visualize.py [-h] [-f FILES [FILES ...]] [-mcn MAIN_CONTRACTS [MAIN_CONTRACTS ...]]

optional arguments:
  -h, --help            show this help message and exit
  -f FILES [FILES ...], --files FILES [FILES ...]
                        Path to .sol files (space separated)
  -mcn MAIN_CONTRACTS [MAIN_CONTRACTS ...], --main-contracts MAIN_CONTRACTS [MAIN_CONTRACTS ...]
                        Main contract names (space separated, without .sol extension). Default: All Contracts
```

## Demo
### With just files (`-f` flag)
```
(venv) master ~/Public/storage-layout-visualizer> python3 visualize.py -f sample1.sol sample2.sol

                     
             88                                      88  88                         
             ""                                      88  ""                         
                                                     88                             
8b       d8  88  ,adPPYba,  88       88  ,adPPYYba,  88  88  888888888   ,adPPYba,  
`8b     d8'  88  I8[    ""  88       88  ""     `Y8  88  88       a8P"  a8P_____88  
 `8b   d8'   88   `"Y8ba,   88       88  ,adPPPPP88  88  88    ,d8P'    8PP"  
  `8b,d8'    88  aa    ]8I  "8a,   ,a88  88,    ,88  88  88  ,d8"       "8b,   ,aa  
    "8"      88  `"YbbdP"'   `"YbbdP'Y8  `"8bbdP"Y8  88  88  888888888   `"Ybbd8"'  
                                                                                
                              Author: savi0ur

Helps in Visualizing storage layout of state variables in solidity
v1.0


Layout for sample1.sol
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
┃        Contract         ┃ Variable  ┃ Slot ┃ Offset ┃   Type    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
│ sample1.sol:LostStorage │ myAddress │  0   │   0    │ t_address │
├─────────────────────────┼───────────┼──────┼────────┼───────────┤
│ sample1.sol:LostStorage │  myUint   │  1   │   0    │ t_uint256 │
└─────────────────────────┴───────────┴──────┴────────┴───────────┘

Layout for sample2.sol
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
┃        Contract        ┃       Variable       ┃ Slot ┃ Offset ┃   Type    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
│ sample2.sol:ProxyClash │ otherContractAddress │  0   │   0    │ t_address │
└────────────────────────┴──────────────────────┴──────┴────────┴───────────┘
(venv) master ~/Public/storage-layout-visualizer> 
```
### With `-mcn` flag
```
(venv) master ~/Public/storage-layout-visualizer> python3 visualize.py -f sample1.sol sample2.sol -mcn LostStorage ProxyClash

                     
             88                                      88  88                         
             ""                                      88  ""                         
                                                     88                             
8b       d8  88  ,adPPYba,  88       88  ,adPPYYba,  88  88  888888888   ,adPPYba,  
`8b     d8'  88  I8[    ""  88       88  ""     `Y8  88  88       a8P"  a8P_____88  
 `8b   d8'   88   `"Y8ba,   88       88  ,adPPPPP88  88  88    ,d8P'    8PP"  
  `8b,d8'    88  aa    ]8I  "8a,   ,a88  88,    ,88  88  88  ,d8"       "8b,   ,aa  
    "8"      88  `"YbbdP"'   `"YbbdP'Y8  `"8bbdP"Y8  88  88  888888888   `"Ybbd8"'  
                                                                                
                              Author: savi0ur

Helps in Visualizing storage layout of state variables in solidity
v1.0

Combined layout view of LostStorage,ProxyClash
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┓
┃        Contract         ┃       Variable       ┃ Slot ┃ Offset ┃   Type    ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━━━━━━━┩
│ sample1.sol:LostStorage │      myAddress       │  0   │   0    │ t_address │
│ sample2.sol:ProxyClash  │ otherContractAddress │  0   │   0    │ t_address │
├─────────────────────────┼──────────────────────┼──────┼────────┼───────────┤
│ sample1.sol:LostStorage │        myUint        │  1   │   0    │ t_uint256 │
└─────────────────────────┴──────────────────────┴──────┴────────┴───────────┘
(venv) master ~/Public/storage-layout-visualizer>
```
