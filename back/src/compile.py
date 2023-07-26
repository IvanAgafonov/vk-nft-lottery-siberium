import os

import solcx

solcx.install_solc(version='0.8.19')

os.chdir(os.path.dirname(__file__))
os.chdir("../data")
temp_file = solcx.compile_files(
    'LotteryNFT.sol',
    output_values=['abi', 'bin'],
    solc_version='0.8.19'
)
os.chdir("../src")

abi = temp_file['LotteryNFT.sol:LotteryNFT']['abi']
bytecode = temp_file['LotteryNFT.sol:LotteryNFT']['bin']