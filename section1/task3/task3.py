import etherscan.accounts as accounts
import etherscan.blocks as blocks
import etherscan.contracts as contracts
import etherscan.stats as stats
import etherscan.tokens as tokens
import etherscan.transactions as transactions
import etherscan.proxies as proxies
import json
import pandas as pd

with open('./api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

# play and combine scripts in examples/accounts
address = '0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b'
api = accounts.Account(address=address, api_key=key)
transaction = api.get_transaction_page(page=1, offset=10)
df = pd.DataFrame(transaction)
df['timeStamp'] = pd.to_datetime(df['timeStamp'],unit='ms')
df.to_csv('transaction_data.csv',index=False)
blocks_mined = api.get_blocks_mined_page(page=1, offset=10)
df = pd.DataFrame(blocks_mined)
df['timeStamp'] = pd.to_datetime(df['timeStamp'],unit='ms')
df.to_csv('blocks_mined_data.csv',index=False)

# play and combine scripts in examples/blocks
block = 2165403
api = blocks.Blocks(api_key=key)
reward = api.get_block_reward(block)
df = pd.DataFrame(reward)
df[['uncles_miner','uncles_unclePosition', 'uncles_blockreward']] = pd.DataFrame(df.uncles.tolist(), index= df.index)
df = df[['blockNumber','timeStamp','blockMiner','blockReward',
         'uncleInclusionReward','uncles_miner','uncles_unclePosition','uncles_blockreward']]
df.to_csv('reward_data.csv',index=False)

# play and combine scripts in examples/contracts
address = '0xfb6916095ca1df60bb79ce92ce3ea74c37c5d359'
api = contracts.Contract(address=address, api_key=key)
abi = api.get_abi()
df = pd.DataFrame(json.loads(abi)).fillna(False)
df.to_csv('abi_data.csv',index=False)

# play and combine scripts in examples/proxies
api = proxies.Proxies(api_key=key)
price = api.gas_price()
print('Price: ' + str(int(price,0)))
block = api.get_block_by_number(5747732)
df = pd.DataFrame([block])
df.to_csv('block_data.csv',index=False)
print('Block number: ' + str(int(block['number'],0)))
transaction = api.get_transaction_by_blocknumber_index(block_number='0x57b2cc',
                                                       index='0x2')
df = pd.DataFrame([transaction])
df.to_csv('proxies_transaction_data.csv',index=False)
print('Transaction Index: ' + str(int(transaction['transactionIndex'],0)))

# play and combine scripts in examples/stats
api = stats.Stats(api_key=key)
stats = api.get_ether_last_price()
df = pd.DataFrame([stats])
df['ethbtc_timestamp'] = pd.to_datetime(df['ethbtc_timestamp'],unit='ms')
df['ethusd_timestamp'] = pd.to_datetime(df['ethusd_timestamp'],unit='ms')
df.to_csv('stats_data.csv',index=False)

# play and combine scripts in examples/tokens
contract_address = '0x57d90b64a1a57749b0f932f1a3395792e12e7055'
api = tokens.Tokens(contract_address=contract_address, api_key=key)
address = '0xe04f27eb70e025b78871a2ad7eabe85e61212761'
print('Token balance: ' + api.get_token_balance(address=address))
print('Total supply of tokens: ' + api.get_total_supply())

# play and combine scripts in examples/transactions
api = transactions.Transactions(api_key=key)
TX_HASH = '0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a'
status = api.get_status(tx_hash=TX_HASH)
df = pd.DataFrame([status])
df['isError'] = df['isError'].astype(bool)
df.to_csv('status_data.csv',index=False)
TX_HASH = '0x513c1ba0bebf66436b5fed86ab668452b7805593c05073eb2d51d3a52f480a76'
receipt_status = api.get_tx_receipt_status(tx_hash=TX_HASH)
df = pd.DataFrame([receipt_status])
df.to_csv('receipt_status_data.csv',index=False)

# Optional
"""
1. Unittest can test code by parts for basic function achievement.
2.  
    import unittest
    class ClassNameTestCase(unittest.TestCase):
       def test_function_nam(self):
           self.assertEqual(function(), CONSTANT_RESULTS)
3. I can trigger test discovery at any time using the Python: Discover Tests command in vscode.
"""