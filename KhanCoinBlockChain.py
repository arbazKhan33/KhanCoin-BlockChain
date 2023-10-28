import hashlib
import time

class BlockData:
    def __init__(self, position, proof_val, prev_data_hash, transactions, timestamp=None):
        self.position = position
        self.proof_val = proof_val
        self.prev_data_hash = prev_data_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()

    def calculate_hash(self):
        data_string = f"{self.position}{self.proof_val}{self.prev_data_hash}{self.transactions}{self.timestamp}"
        return hashlib.sha256(data_string.encode()).hexdigest()

    def __repr__(self):
        return f"{self.position}-{self.proof_val}-{self.prev_data_hash}-{self.transactions}-{self.timestamp}"

class KhanKoinChain:

    def __init__(self):
        self.blocks = []
        self.pending_transactions = []
        self.network_nodes = set()
        self.create_genesis_block()

    def create_genesis_block(self):
        self.add_new_block(proof_val=0, prev_data_hash=0)

    def add_new_block(self, proof_val, prev_data_hash):
        block_instance = BlockData(
            position=len(self.blocks),
            proof_val=proof_val,
            prev_data_hash=prev_data_hash,
            transactions=self.pending_transactions
        )
        self.pending_transactions = []
        self.blocks.append(block_instance)

    def validate_block(self, block, prev_block):
        if prev_block.position + 1 != block.position:
            return False
        elif prev_block.calculate_hash() != block.prev_data_hash:
            return False
        elif block.timestamp <= prev_block.timestamp:
            return False
        return True

    def record_transaction(self, sender, receiver, amount):
        self.pending_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

    @staticmethod
    def find_proof(prev_proof):
        current_proof = 0
        while KhanKoinChain.is_proof_valid(prev_proof, current_proof) is False:
            current_proof += 1
        return current_proof

    @staticmethod
    def is_proof_valid(prev_proof, current_proof):
        guess = f"{prev_proof}{current_proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def latest_block(self):
        return self.blocks[-1]

    def mine_block(self, miner_details):

        self.record_transaction(
            sender="0",
            receiver=miner_details,
            amount=1
        )

        recent_block = self.latest_block()
        recent_proof = recent_block.proof_val
        proof = self.find_proof(recent_proof)
        recent_hash = recent_block.calculate_hash()
        new_block = self.add_new_block(proof, recent_hash)
        return vars(new_block)

    def add_node(self, address):
        self.network_nodes.add(address)

    @staticmethod
    def get_block_instance(block_data):
        return BlockData(
            block_data['position'],
            block_data['proof_val'],
            block_data['prev_data_hash'],
            block_data['transactions'],
            timestamp=block_data['timestamp']
        )

# Initializing the blockchain
khan_koin = KhanKoinChain()

print("Starting KhanKoin mining...")
print(khan_koin.blocks)

block_to_mine = khan_koin.latest_block()
recent_proof = block_to_mine.proof_val
proof = khan_koin.find_proof(recent_proof)

khan_koin.record_transaction(
    sender="0",
    receiver="KhanKoinUser",
    amount=1
)

recent_hash = block_to_mine.calculate_hash()
new_block = khan_koin.add_new_block(proof, recent_hash)

print("KhanKoin mining completed!")
print(khan_koin.blocks)
