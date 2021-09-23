from tools import money
import asyncio


users = asyncio.run(money.get_bank_data())

bruh = "sup"

try:
  amount = int(bruh)
except ValueError:
  print("not int bruh")