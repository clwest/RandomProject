from dotenv import load_dotenv
import os
import ccxt, time
from web3 import Web3
from flask import Flask, render_template, request, flash, redirect

load_dotenv()


ALCHEMY_URL = os.getenv("ALCHMEY_URL")
MINERS = os.getenv("MINERS")


w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))


def get_ethereum_price():
    binance = ccxt.binance()
    ethereum_price = binance.fetch_ticker('ETH/USDC')

    return ethereum_price


@app.get("/")
def index():
    eth = w3.eth
    ethereum_price = get_ethereum_price()
    
    latest_blocks = []
    for block_number in range(eth.block_number, eth.block_number-10, -1):
        block = eth.getBlock(block_number)
        latest_blocks.append(block)
        
    latest_transactions = []
    for tx in latest_blocks[-1]['transactions'][-10:]:
        transaction = eth.getTransaction(tx)
        latest_transactions.append(transaction)
        
    current_time = time.time()
    
    return render_template("index.html",
        miners = MINERS,
        current_time = current_time,
        eth = eth,
        ethereum_price= ethereum_price,
        latest_blocks = latest_blocks,
        latest_transactions = latest_transactions)
    

@app.get("/address")
def address():
    address = request.args.get('address')
    
    ethereum_price = get_ethereum_price()
    
    try:
        address = w3.toChecksumAddress(address)
    except:
        flash("Invalid address")
        return redirect('/')
    
    balance = w3.eth.get_balance(address)
    balance = w3.fromWei(balance, 'ether')
    
    return render_template("address.html", ethereum_price=ethereum_price, address=address, balance=balance)

@app.get("/block/<block_number>")
def block(block_number):
    block = w3.eth.get_block(int(block_number))
    
    return render_template("block.html", block=block)

@app.get("/transaction/<hash>")
def transaction(hash):
    tx = w3.eth.get_transaction(hash)
    value = w3.fromWei(tx.value, 'ether')
    receipt = w3.eth.get_transaction_receipt(hash)
    ethereum_price = get_ethereum_price()
    
    gas_price = w3.fromWei(tx.gasPrice, 'ether')
    return render_template("transaction.html", tx=tx, value=value, receipt=receipt, ethereum_price=ethereum_price, gas_price=gas_price)



app.run()


