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
      while loop.is_running() == False:
        loop.run_until_complete(task)
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

async def upload_image(client, image, conv_id):
    # Upload image to obtain image_id:
    image_file = open(image, 'rb')
    uploaded_image = await client.upload_image(
        image_file, return_uploaded_image=True
    )

    # Send a chat message referencing the uploaded image_id:
    request = hangups.hangouts_pb2.SendChatMessageRequest(
        request_header=client.get_request_header(),
        event_request_header=hangups.hangouts_pb2.EventRequestHeader(
            conversation_id=hangups.hangouts_pb2.ConversationId(
                id=conv_id
            ),
            client_generated_id=client.get_client_generated_id(),
        ),
        existing_media=hangups.hangouts_pb2.ExistingMedia(
            photo=hangups.hangouts_pb2.Photo(
                photo_id=uploaded_image.image_id,
            ),
        ),
    )
    await client.send_chat_message(request)

async def main(image, id):
  await run(upload_image, image, id)
