'''Group Members:
    - Name1/Yunmo xie 135856201
    - Name2 Edward Liu 126558196
'''

from block import DATA_FILE, get_blockchains, BlockChain
from typing import List


def validate_blockchain(blockchain: BlockChain, line: str) -> bool:
    """
    Validate a blockchain.
    :param blockchain: a blockchain
    :return: true if the blockchain is valid, false otherwise
    """
    previous_block = None
    for i, block in enumerate(blockchain.blocks):
        # 1. check if the current block hash is valid
        if block.previousBlockHash != "":
            expected = str(
                hash(f'{previous_block.previousBlockHash}{previous_block.data}{previous_block.randomNumber}'))
            if expected != block.previousBlockHash:
                print("Invalid previous block hash!")
                return False

        # 2. Check randomNumber all digits are in currentBlockHash
        for digit in block.randomNumber:
            if digit not in block.currentBlockHash:
                print("Invalid randomNumber!")
                return False

        # 3. Check current block hash is valid
        # extract data from the line
        data = line[3 + i * 9:3 + i * 9 + 9]
        if previous_block is None:
            expected = str(hash(f'{data}{block.randomNumber}'))
        else:
            expected = str(hash(f'{previous_block.currentBlockHash}{data}{block.randomNumber}'))

        if expected != block.currentBlockHash:
            print("Invalid current block hash!")
            return False

        previous_block = block

    return True


def validate_chains(chains: List[BlockChain], lines: List[str]) -> bool:
    """
    Validate a list of blockchains.
    :param chains: a list of blockchains
    :param lines: a list of lines from the data file
    :return: true if all blockchains are valid, false otherwise
    """
    if len(chains) != len(lines):
        print("Invalid number of blockchains!")
        return False

    for i in range(len(chains)):
        if not validate_blockchain(chains[i], lines[i]):
            return False
    return True


if __name__ == '__main__':
    chains = get_blockchains(DATA_FILE)
    with open(DATA_FILE) as f:
        lines = f.readlines()
        if validate_chains(chains, lines):
            print("All blockchains are valid!")
        f.close()
