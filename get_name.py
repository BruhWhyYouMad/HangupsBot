import hangups
import asyncio
import os
async def run(example_coroutine, id):
    # Obtain hangups authentication cookies, prompting for credentials from
    # standard input if necessary.
    cookies = hangups.get_auth_stdin('token', manual_login=True)
    client = hangups.Client(cookies)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(_async_main(example_coroutine, client, id),loop=loop)

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

async def _async_main(example_coroutine, client, id):
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
      await example_coroutine(client, id)
    except asyncio.CancelledError:
      pass
    finally:
      await client.disconnect()
      await task

async def get_name(client, id):
  #self_entity = hangups.hangouts_pb2.GetSelfInfoRequest()
  #client.sync_recent_conversations(client.get_request_header())
  #name = hangups.ConversationList(client).get_user(id)
  
  request = hangups.hangouts_pb2.GetEntityByIdRequest(
    request_header = client.get_request_header(),
    batch_lookup_spec=[hangups.hangouts_pb2.EntityLookupSpec(gaia_id=id)]
  )
  entity = await client.get_entity_by_id(request)
  name = entity.entity[0].properties.display_name
  f = open('data/name.dat', 'w')
  f.write(name)

async def main(id):
  await run(get_name, id)