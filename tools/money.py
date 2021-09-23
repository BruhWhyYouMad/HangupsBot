import sys
import random
import asyncio
import json
import time

sys.path.insert(0, '/home/runner/HangupsBot/')
import get_name
sys.path.insert(0, '/home/runner/HangupsBot/tools')

bank = sys.path[0].replace('/tools', '/data/bank.json')
bank_names = sys.path[0].replace("/tools", "/data/bank_names.json")
name_path = sys.path[0].replace('/tools', '/data/name.dat')

admin_id = 102354775178282432346
conv_id = 'UgxkokYg7g_hO0vpO654AaABAQ'

mainshop = [{"name":"Watch","price":100,"description":"Time"},
            {"name":"Laptop","price":1000,"description":"Work"},
            {"name":"PC","price":10000,"description":"Gaming"},
            {"name":"Tesla","price":75000,"description":"Elon Musk Not Included"},
            {"name":"Ferrari","price":99999,"description":"Sports Car"}]
async def get_name_from_id(id):
  await get_name.main(str(id))
  await asyncio.sleep(1.5)
  name = open(name_path, 'r').read()
  print(name)
  return name
async def balance(id):
    await open_account(id)
    name = await get_name_from_id(str(id))
    users = await get_bank_data()
    wallet_amt = users[str(id)]["wallet"]
    bank_amt = users[str(id)]["bank"]
    response = "{name}'s Balance\nWallet Balance: {wallet}\nBank Balance: {bank}".format(name=name, wallet=wallet_amt, bank=bank_amt)
    return response
async def beg(id):
    await open_account(id)
    users = await get_bank_data()
    current_time = time.time()
    last_beg_time = users[str(id)]["time"]
    print(type(last_beg_time))
    if last_beg_time + 10 >= current_time:
      print("ok")
      response = "You have to wait for 10 seconds till you can use this command again"
      return response
    else:
      earnings = random.randrange(101)
      name = await get_name_from_id(id)
      response = f"{name} Got {earnings} coins!!"
      print(response)
      users[str(id)]["wallet"] += earnings
      users[str(id)]["time"] = current_time
      with open(bank,'w') as f:
        json.dump(users,f,indent=4)
      return response
async def withdraw(message, id, amount):
    await open_account(id)
    bal = await update_bank(id)
    if amount == "/money withdraw":
        return "Please enter the amount"
    if amount == "all":
        amount = bal[1]
    try:
      amount = int(amount)
    except ValueError:
      return "Value Not Proper\n/money withdraw <amount>"

    if amount > bal[1]:
        return 'You do not have sufficient balance'
    if amount < 0:
        return 'Amount must be positive!'
    name = await get_name_from_id(id)
    await update_bank(id,amount)
    await update_bank(id,-1*amount,'bank')
    return f'{name} You withdrew {amount} coins'

async def deposit(message, id, amount):
    await open_account(id)
    bal = await update_bank(id)
    if amount == "/money depo":
        return "Please enter the amount"
    if amount == "all":
        amount = bal[0]
    try:
      amount = int(amount)
    except ValueError:
      return "Value Not Proper\n/money depo <amount>"

    if amount > bal[0]:
        return 'You do not have sufficient balance'
    if amount < 0:
        return 'Amount must be positive!'
    
    await update_bank(id,-1*amount)
    await update_bank(id,amount,'bank')
    name = await get_name_from_id(id)
    return f'{name} You deposited {amount} coins'

async def send(author_id,reciever_name,amount):
    users = await get_bank_data()
    users = json.dumps(users)
    users = eval(users)
    reciever_id = None
    for i in users:
      if users[i]["name"] == reciever_name:
        reciever_id = i
    if reciever_id == None:
      return "Name is invalid, Please check all the captilization\nType /money name for a full list of Bank Registered Names"
    await open_account(author_id)
    await open_account(reciever_id)
    if amount == "":
        return "Please enter the amount"

    bal = await update_bank(author_id)
    if amount == 'all':
        amount = bal[0]
    try:
      amount = int(amount)
    except ValueError:
      return "Value Not Proper\n/money send <person>-<amount>"
    if amount > bal[0]:
        return 'You do not have sufficient balance'
    if amount < 0:
        return 'Amount must be positive!'

    await update_bank(author_id,-1*amount,'bank')
    await update_bank(reciever_id,amount,'bank')
    author_name = await get_name_from_id(id)
    return f'{author_name} You gave {reciever_name} {amount} coins'

async def name(id):
  msg = ""
  users = await get_bank_data()
  for i in users:
    msg = f'{msg} {users[i]["name"]}\n'
  response = f"The Full List of Registered Bank Names are:\n{msg}"
  return response

async def all_bal():
  msg = ""
  users = await get_bank_data()
  for i in users:
    msg = f'{msg} {users[i]["name"]}\n Wallet: {users[i]["wallet"]}\n Bank: {users[i]["bank"]}'
  response = f"The Full List of Registered Bank Names are:\n{msg}"

async def rob(author_id,reciever_name):
    users = await get_bank_data()
    reciever_id = None
    for i in users:
      if users[i]["name"] == reciever_name:
        reciever_id = i
    if reciever_id == None:
      return "Name is invalid, Please check all the captilization\nType /money name for a full list of Bank Registered Names"
    await open_account(author_id)
    await open_account(reciever_id)
    bal = await update_bank(reciever_id)


    if bal[0]<100:
      return 'It is useless to rob him :('

    earning = random.randrange(0,bal[0])

    await update_bank(author_id,earning)
    await update_bank(reciever_id,-1*earning)
    name = await get_name_from_id(author_id)
    return f'{name} You robbed {reciever_name} and got {earning} coins'





async def update_bank(id,change=0,mode = 'wallet'):
    users = await get_bank_data()

    users[str(id)][mode] += change

    with open('data/bank.json','w') as f:
        json.dump(users,f,indent=4)
    bal = users[str(id)]['wallet'],users[str(id)]['bank']
    return bal
async def get_bank_data():
    with open(bank,'r') as f:
        users = json.load(f)
    return users
async def open_account(id):
    users = await get_bank_data()
    if str(id) in users:
      return False
    else:
      name = await get_name_from_id(str(id))
      users[str(id)] = {}
      users[str(id)]["wallet"] = 0
      users[str(id)]["bank"] = 0
      users[str(id)]["name"] = name
      users[str(id)]["time"] = 100
    with open(bank,'w') as f:
        json.dump(users,f,indent=4)
    return True
    
asyncio.run(balance(admin_id))
