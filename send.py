import asyncio
import hangups

async def run(example_coroutine, message, id):
    # Obtain hangups authentication cookies, prompting for credentials from
    # standard input if necessary.
    cookies = hangups.get_auth_stdin('token', manual_login=True)
    client = hangups.Client(cookies)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(_async_main(example_coroutine, client, message, id),loop=loop)

    try:
        while True:
          if loop.is_running() == False:
            loop.run_until_complete(task)
          else:
            break
    except KeyboardInterrupt:
        task.cancel()
        loop.run_until_complete(task)
    finally:
        while True:
          if loop.is_running() == False:
            loop.close()
          else:
            break


          
async def _async_main(example_coroutine, client, message, id):
    # Spawn a task for hangups to run in parallel with the example coroutine.
    task = asyncio.ensure_future(client.connect())

    # Wait for hangups to either finish connecting or raise an exception.
    on_connect = asyncio.Future()
    client.on_connect.add_observer(lambda: on_connect.set_result(None))
    done, _ = await asyncio.wait(
        (on_connect, task), return_when=asyncio.FIRST_COMPLETED
    )
    await asyncio.gather(*done)

    # Run the example coroutine. Afterwards, disconnect hangups gracefully and
    # yield the hangups task to handle any exceptions.
    try:
        await example_coroutine(client, message, id)
    except asyncio.CancelledError:
        pass
    finally:
        await client.disconnect()
        await task

async def send_message(client, message, id):
    segments = []
    for i in hangups.ChatMessageSegment.from_str(message):
      segments.append(i.serialize())
    request = hangups.hangouts_pb2.SendChatMessageRequest(
        request_header=client.get_request_header(),
        event_request_header=hangups.hangouts_pb2.EventRequestHeader(
            conversation_id=hangups.hangouts_pb2.ConversationId(
                id=id
            ),
            client_generated_id=client.get_client_generated_id(),
        ),
        message_content=hangups.hangouts_pb2.MessageContent(
            segment=segments
        ),
    )
    await client.send_chat_message(request)

async def main(message, id):
  await run(send_message, message, id)


