import keep_alive
import os
import commands
from runner import run
import asyncio
import hangups
        # if msg in command_list:
        #   print("New Command - {msg}".format(msg))
        # elif msg == '/':
        #   print("Incomplete Command!")
        # elif msg.startswith('/'):
        #   print("{msg} is not a command!".format(msg))
        # elif msg == "Message is Media":
        #   print("{msg} - {num}".format(msg))
        # else:
        #   print("{msg} is a Normal Message".format(msg))
        # await commands.execute_command(msg, conv_id)
#conv_id = os.environ['conv_id']
conv_id = 'UgxkokYg7g_hO0vpO654AaABAQ'
admin_id = "103262826359014660363"
#classmates = UgxkokYg7g_hO0vpO654AaABAQ

async def receive_messages(client, args):
    print('Loading Conversation List...')
    user_list, conv_list = (
        await hangups.build_user_conversation_list(client)
    )
    conv_list.on_event.add_observer(on_event)

    print('Waiting For Chat Messages...')
    while True:
        await asyncio.sleep(1)


async def on_event(conv_event):
    if isinstance(conv_event, hangups.ChatMessageEvent):
      if conv_event.user_id.chat_id == admin_id:
        print('Sent Chat Message: {!r}'.format(conv_event.text))
      else:
        print('Received Chat Message: {!r}'.format(conv_event.text))
      await commands.execute_command(conv_event.text, conv_event.user_id.chat_id, conv_event.conversation_id)
        
        


keep_alive.keep_alive()
#print(hangups.conversation.get_user('112320625019354005386'))
#run(get_name_from_id, '100619629124393024992')
run(receive_messages, "bruh")
#run(get_name_from_id, '112320625019354005386')
#112320625019354005386

