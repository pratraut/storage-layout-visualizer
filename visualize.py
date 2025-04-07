import os, json, argparse, platform, re
from rich.console import Console
from rich.table import Table
from rich.text import Text

COLOR = '\033[32m'
banner_text = f"""{COLOR}                     
             88                                      88  88                         
             ""                                      88  ""                         
                                                     88                             
8b       d8  88  ,adPPYba,  88       88  ,adPPYYba,  88  88  888888888   ,adPPYba,  
`8b     d8'  88  I8[    ""  88       88  ""     `Y8  88  88       a8P"  a8P_____88  
 `8b   d8'   88   `"Y8ba,   88       88  ,adPPPPP88  88  88    ,d8P'    8PP"""""""  
  `8b,d8'    88  aa    ]8I  "8a,   ,a88  88,    ,88  88  88  ,d8"       "8b,   ,aa  
    "8"      88  `"YbbdP"'   `"YbbdP'Y8  `"8bbdP"Y8  88  88  888888888   `"Ybbd8"'  
                                                                                
                              Author: savi0ur

\033[0mHelps in Visualizing storage layout of state variables in solidity
v1.0
"""

console = Console()
text = Text()
banner = text.append(banner_text)

class ContractStorage(object):
    def __init__(self, **kwargs):
        self.contract = kwargs['contract']
        self.name = kwargs['name']
        self.slot = kwargs['slot']
        self.offset = kwargs['offset']
        self.type = kwargs['type']

if(platform.system() == 'Windows'):
    os.system('cls')
if(platform.system().lower() in ['linux', 'darwin']):
    os.system('clear')

console.print(banner)

argp = argparse.ArgumentParser()
argp.add_argument("-f", "--files", help="Path to .sol files (space separated)", nargs='+')
argp.add_argument("-mcn", "--main-contracts", help="Main contract names (space separated, without .sol extension). Default: All Contracts", nargs='+')

parser = vars(argp.parse_args())
# print(parser)

OUTPUT_PATH = "./out.json"
COMPILE_CMD = "solc %s --combined-json storage-layout --pretty-json > " + OUTPUT_PATH

def getCombinedLayout(layouts, mainContractNames):
    if len(layouts) != len(mainContractNames):
        print("ERROR: length is not same!")
        exit(0)

    combinedLayouts = []
    for rec in layouts:
        for sol_file in rec:
            for state in rec[sol_file]:
                combinedLayouts.append(state)
    
    filteredLayouts = []
    for layout in combinedLayouts:
        contract_name = layout.contract.split(":")[-1]
        for contractName in mainContractNames:
            if contract_name == contractName:
                filteredLayouts.append(layout)

    sorted_by_slot = sorted(filteredLayouts, key=lambda x: x.slot, reverse=False)
    # for sorted in sorted_by_slot:    

    return sorted_by_slot

def displayLayout(layouts, mainContractNames=[]):
    if mainContractNames:
        layouts = getCombinedLayout(layouts, mainContractNames)

    console = Console()    
    
    # print(dir(table))
    if not mainContractNames:
        for rec in layouts:
            for sol_file in rec:
                text = Text()
                text.append("\nLayout for ")
                text.append(sol_file, style="bold underline green")
                console.print(text)

                table = Table(show_header=True, header_style="bold magenta")

                for col in ["Contract", "Variable", "Slot", "Offset", "Type"]:
                    table.add_column(col, justify="center", header_style="cyan")
            
                for i in range(len(rec[sol_file])):
                    state = rec[sol_file][i]
                    if i + 1 < len(rec[sol_file]) and state.slot != rec[sol_file][i + 1].slot:
                        table.add_row(state.contract, state.name, state.slot, state.offset, state.type, end_section=True)
                    else:
                        table.add_row(state.contract, state.name, state.slot, state.offset, state.type, end_section=False)
            
                console.print(table)
    else:
        text = Text()
        text.append("Combined layout view of ")
        text.append(",".join(mainContractNames), style="bold underline green")
        console.print(text)
        table = Table(show_header=True, header_style="bold magenta")

        for col in ["Contract", "Variable", "Slot", "Offset", "Type"]:
            table.add_column(col, justify="center", header_style="cyan")
        
        for i in range(len(layouts)):
            state = layouts[i]
            if i + 1 < len(layouts) and state.slot != layouts[i + 1].slot:
                table.add_row(state.contract, state.name, state.slot, state.offset, state.type, end_section=True)
            else:
                table.add_row(state.contract, state.name, state.slot, state.offset, state.type, end_section=False)
        
        console.print(table)

def processFile(file_paths):
    unique_path = []
    all_files = []
    for file_path in file_paths:
        dir_path = os.path.dirname(file_path)
        if not dir_path:
            dir_path = '.'
            # print("Dir path =", dir_path)
        is_present = any([dir_path in u_path for u_path in unique_path])
        if not is_present:
            unique_path.append(dir_path)
            files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(dir_path) for f in filenames if os.path.splitext(f)[1] == '.sol']
            for u_file in files:
                if u_file not in all_files:
                    all_files.append(u_file)
    # files = ['./test.sol']
    # print(unique_path)
    # print(all_files)

    # exit(0)

    for file in all_files:
        # print("File =", file)
        # dir_path = os.path.dirname(file)
        # print("Dir path =", dir_path)
        dir_path = os.path.abspath(os.path.dirname(file))
        # print("Dir path =", dir_path)
        data = None
        with open(file, "rt") as file_handle:
            data = file_handle.read()

        with open(file + ".bak", "wt") as file_handle:
            file_handle.write(data)

        if data:
            data = re.sub(r"pragma solidity .*", "pragma solidity >=0.4.0 <0.9.0;", data)
            all_imports = re.findall(r"import .*", data)
            # filtered_imports = []
            for imp in all_imports:
                # print(imp)
                import_path = re.search("import.*[\'\"](.*)[\'\"];", imp)
                # print("import path =", import_path.group())
                import_file = os.path.basename(import_path.group(1))
                # print(import_file)
                filtered_import = f"import '{dir_path}/{import_file}';"
                # print(filtered_import)
                data = re.sub(imp, filtered_import, data)

            with open(file, "wt") as file_handle:
                file_handle.write(data)

contractLayout = []

processFile(parser.get("files"))
for sol_file in parser.get("files"):    
    os.system(COMPILE_CMD % sol_file)
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, "r") as file:
            layout = []
            json_data = json.loads(file.read())
            print(json_data)
            contracts = json_data['contracts']
            for contract in contracts:
                # print("contract =", contract)
                for storage in contracts[contract]['storage-layout']['storage']:
                    layout.append(ContractStorage(**{
                        'contract': storage['contract'],
                        'name': storage['label'],
                        'slot': storage['slot'],
                        'offset': str(storage['offset']),
                        'type': storage['type']
                    }))
            contractLayout.append({sol_file: layout})

    os.remove(OUTPUT_PATH)

# print(len(contractLayout))
if parser.get("main_contracts", None):
    displayLayout(contractLayout, mainContractNames=parser.get("main_contracts"))
else:
    displayLayout(contractLayout)
