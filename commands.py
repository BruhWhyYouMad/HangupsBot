import get_name
import send
import image
import asyncio
import random
import sys
from tools import meme as me
from tools import money

classmates = "UgxkokYg7g_hO0vpO654AaABAQ"
admin_id = "102354775178282432346"
#conv_id = os.environ['conv_id']
#conv_id = 'UgxkokYg7g_hO0vpO654AaABAQ'


async def send_msg(message, conv_id):
	await send.main(message, conv_id)

def dev_send(message):
  asyncio.run(send_msg(message, 'UgxkokYg7g_hO0vpO654AaABAQ'))

async def img(image_file, conv_id):
	await image.main(image_file, conv_id)

async def pong(message, conv_id):
	if message == "/ping":
		response = "Pong"
		await send_msg(response, conv_id)
		print("Responded to /hello command with {}".format(response))
	elif message == "/pong":
		response = "Ping"
		await send_msg(response, conv_id)
		print("Responded to /hello command with {}".format(response))


async def sup(message, conv_id):
	if message == "/sup":
		response = "Ayo Wassssup"
		await send_msg(response, conv_id)
		print("Responded to /hello command with {}".format(response))


async def hello(message, id, conv_id):
	if message == "/hello":
		await get_name.main(id)
		print("written")
		await asyncio.sleep(2)
		f = open("data/name.dat", 'r+')
		name = f.read()
		print(name)
		print("read")
		#f.write("test")
		response = "Hello! {}".format(name)
		await send_msg(response, conv_id)
		print("Responded to /hello command with {}".format(response))


async def help(message, conv_id):
	if message == "/help":
		command_list = open('data/help.dat', 'r').read()
		response = "Wassup This is bot do be dumb tho but find commands on /commands,\n" + command_list
		await send_msg(response, conv_id)
		print("Responded to /hello command with {}".format(response))


async def roast(message, conv_id):
	if message == "/roast":
		print("he has choosen death")
		f = open("data/roasts.dat", "r")
		roasts = eval(f.read())
		response = random.choice(roasts)
		await send_msg(response, conv_id)
		print("Responded to /hello command with {}".format(response))


async def commands(message, conv_id):
	if message == "/commands":
		command_list = open('data/help.dat', 'r').read()
		response = "cool so you came here The commands are: \n{}".format(
		    command_list)
		await send_msg(response, conv_id)
		print("Responded to /hello command with {}".format(response))


async def newline(message, conv_id):
	if message == "/newline":
		response = "newline\nis\ncool"
		await send_msg(response, conv_id)
		print("Responded to /hello command with {}".format(response))


async def meme(message, id, conv_id):
  if message == "/meme":
    if conv_id == classmates:
      await send_msg("Bruh /meme is disabled in this group due to heavy protest by Ian :(\nif u still want memes then dm the bot", conv_id)
    else:
      await send_msg("Sending You The Finest Of Memes......\nIf its taking lots of money its probably a Gif", conv_id)
      me.get_meme()
      id = str(id)
      await img('data/meme.jpg', conv_id)


async def money_com(message, id, conv_id):
  if message.startswith("/money"):
    if message.startswith("/money bal"):
      msg = await money.balance(id)
      await send_msg(msg, conv_id)
    if message.startswith("/money beg"):
      msg = await money.beg(id)
      await send_msg(msg, conv_id)
    if message.startswith("/money withdraw"):
      amount = message.replace("/money withdraw ", "")
      msg = await money.withdraw(message, id, amount)
      await send_msg(msg, conv_id)
    if message.startswith("/money depo"):
      amount = message.replace("/money depo ", "")
      msg = await money.deposit(message, id, amount)
      print(msg)
      await send_msg(msg, conv_id)
    if message.startswith("/money send"):
      params = message.replace("/money send ", "")
      print(params.partition("-")[2])
      amount = params.partition("-")[2]
      print(amount)
      name = params.replace(f"-{amount}", "")
      print(name)
      msg = await money.send(id, name, amount)
      await send_msg(msg, conv_id)
    if message.startswith("/money name"):
      msg = await money.name(id)
      await send_msg(msg, conv_id)
    if message.startswith("/money rob"):
      name = message.replace('/money rob ', "")
      print(name)
      msg = await money.rob(id, name)
      print(msg)
      await send_msg(msg, conv_id)
    if message == "/money all-bal":
      msg = await money.all_ball()
      await send_msg(msg, conv_id)
      

async def suggestion(message, id, conv_id):
	if message.startswith("/suggestion"):
		suggestion = message.replace("/suggestion", "")
		await get_name.main(id)
		await asyncio.sleep(2)
		nf = open('data/name.dat', 'r')
		name = nf.read()
		f = open("data/suggestions.dat", "a")
		f.write("{name}: {suggestion}\n".format(name=name,
		                                        suggestion=suggestion))
		await send_msg("Suggestion Added", conv_id)
		print("Suggestion Added")

async def dev(message, id, conv_id):
  if message.startswith("/dev"):
    if id != admin_id:
      return "You are not Admin lol"
    code = message.replace('/dev ',"")
    exec(code)


# async def if_proper(msg):
# 	if msg in command_list:
# 		print("New Command - {msg}".format(msg))
# 	elif msg == '/':
# 		print("Incomplete Command!")
# 	elif msg.startswith('/'):
# 		print("{msg} is not a command!".format(msg))
# 	elif msg == "Message is Media":
# 		print("{msg} - {num}".format(msg))
# 	else:
# 		print("{msg} is a Normal Message".format(msg))


async def execute_command(message, id, conv):
	#await if_proper(message)
	conv_id = conv
	await hello(message, id, conv_id)
	await money_com(message, id, conv_id)
	await sup(message, conv_id)
	await roast(message, conv_id)
	await help(message, conv_id)
	await dev(message, id,conv_id)
	await commands(message, conv_id)
	await meme(message, id,conv_id)
	await suggestion(message, id, conv_id)
	await pong(message, conv_id)
	await newline(message, conv_id)

