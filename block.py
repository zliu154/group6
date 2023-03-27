"""
An implementation of a block in a blockchain, which stores the semesters and courses of a student.

Group Members:
    - Name1/Yunmo xie 135856201
    - Name2 Edward Liu 126558196
"""

from random import randint
from typing import List

DATA_FILE = 'sampleData.txt'


class Block:
    """
    A block represents a single unit of storage in a blockchain.

    === Class Attributes ===
    PREVIOUS_BLOCK_HASH:
        The hash of the previous block in the blockchain.
    FULL_PREVIOUS_BLOCK:
        The full previous block in the blockchain, which is the str representation
        of the previous block.
    ALL_BLOCKS_LIST:
        A list of all the blocks in the blockchain.

    === Public Attributes ===
    previousBlockHash:
        The hash of the previous block in the blockchain.
    fullPreviousBlock:
        The full previous block in the blockchain, which is the str representation
        of the previous block.
    data:
        The data stored in the block.
    randomNumber:
        5-digit random number converted to string.
        Note: randomNumber is needed to generate hash codes that meet certain conditions,
        in our case we want hash code to have all the digits of this random number, if
        not then you will generate a new random number and regenerate hash.
    currentBlockHash:
        hash(previousBlockHash+data+randomNumber) + is the concatenation operation.
        Requirement: currentBlockhash will be considered valid if and only if each digit
        in the randomNumber can be found in the generated currentBlockhash
    """
    PREVIOUS_BLOCK_HASH = ""
    FULL_PREVIOUS_BLOCK = ""

    def __init__(self, data: str):
        """
        Initialize a new block with the given data.
        :param data: data to be stored in the block
        """
        self.previousBlockHash = Block.PREVIOUS_BLOCK_HASH
        self.fullPreviousBlock = Block.FULL_PREVIOUS_BLOCK

        self.data = data
        self.randomNumber = None
        self.currentBlockHash = None

        # Generate random number and hash
        self._generateRandomNumber()

        # Update the static variable PREVIOUS_BLOCK_HASH and FULL_PREVIOUS_BLOCK
        Block.PREVIOUS_BLOCK_HASH = self.currentBlockHash
        Block.FULL_PREVIOUS_BLOCK = self.__str__()

    def _generateRandomNumber(self) -> None:
        """
        5-digit random number converted to string
        Note: randomNumber is needed to generate hash codes that meet certain conditions,
        in our case we want hash code to have all the digits of this random number,
        if not then you will generate a new random number and regenerate hash.
        :return: a random number
        """
        # Continue loop until every digit of randomNumber is in currentBlockHash
        while True:
            self.randomNumber = str(randint(10000, 99999))
            self.currentBlockHash = str(hash(str(self.previousBlockHash) + self.data + self.randomNumber))

            # Check if every digit of randomNumber is in currentBlockHash
            all_in_hash = True
            for digit in self.randomNumber:
                if digit not in self.currentBlockHash:
                    all_in_hash = False
                    break

            if all_in_hash:
                break

    def __str__(self):
        """
        Return the string representation of the block, which is concatenation of
        all public attributes.
        :return:
        """
        return f'{self.previousBlockHash}{self.data}{self.randomNumber}{self.currentBlockHash}'


class BlockChain:
    """
    A blockchain is a list of blocks.

    === Public Attributes ===
    blocks:
        A list of blocks.
    """

    def __init__(self, name):
        """
        Initialize a new blockchain with the given name.
        :param name: the blockchain name
        """
        Block.FULL_PREVIOUS_BLOCK = ""
        Block.PREVIOUS_BLOCK_HASH = ""
        self.name = name
        self.blocks = []
        self.size = 0

    def add_block(self, data: str) -> None:
        """
        Add a block to the blockchain.
        :param data: 50-character long string.
        :return: None
        """
        self.blocks.append(Block(data))
        self.size += 1

    def __str__(self):
        """
        Return the string representation of the blockchain use the specific format.
        :return: the string representation
        """
        res = f'{self.name} blockchain ({self.size} blocks)\n'
        for block in self.blocks:
            res += f'PH: {block.previousBlockHash}\n'
            res += f'D: {block.data}\n'
            res += f'RN: {block.randomNumber}\n'
            res += f'CH: {block.currentBlockHash}\n'
            res += '\n'
        return res


def create_blockchain(semester: str) -> BlockChain:
    """
    Create a blockchain with a given semester data.
    :param semester: 50-character long string.
    :return: None
    """
    if len(semester) != 50:
        print("Invalid semester data, the length must be 50.")
        return None

    # S1,5,COM111|075,OPS110098,ULI101076ENG100055MTH10108700
    # S1, 5, COM111
    semester_number = semester[:2]
    number_of_course = int(semester[2])

    # Create a blockchain
    blockchain = BlockChain(semester_number)
    for i in range(3, 3 + number_of_course * 9, 9):
        course = semester[i:i + 9]
        blockchain.add_block(course)
    return blockchain


def get_blockchains(file: str) -> List[BlockChain]:
    """
    Create blockchains from a given file, and return a list of blockchains.
    :param file: the file name
    :return: a list of blockchains
    """
    chains = []
    with open('sampleData.txt') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            chain = create_blockchain(line)
            chains.append(chain)
    return chains


if __name__ == '__main__':
    chains = get_blockchains(DATA_FILE)

    # print the blockchains
    for chain in chains:
        print(chain)
        print('=' * 36)
