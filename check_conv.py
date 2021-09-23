import asyncio
import hangups


def run_example(example_coroutine, *extra_args):
    """Run a hangups example coroutine.
    Args:
        example_coroutine (coroutine): Coroutine to run with a connected
            hangups client and arguments namespace as arguments.
        extra_args (str): Any extra command line arguments required by the
            example.
    """
    # Obtain hangups authentication cookies, prompting for credentials from
    # standard input if necessary.
    cookies = hangups.get_auth_stdin('token', manual_login=True)
    client = hangups.Client(cookies)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(_async_main(example_coroutine, client),
                                 loop=loop)

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        task.cancel()
        loop.run_until_complete(task)
    finally:
        loop.close()

async def _async_main(example_coroutine, client):
    """Run the example coroutine."""
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
        await example_coroutine(client)
    except asyncio.CancelledError:
        pass
    finally:
        await client.disconnect()
        await task


async def sync_recent_conversations(client):
    user_list, conversation_list = (
        await hangups.build_user_conversation_list(client)
    )
    all_users = user_list.get_all()
    all_conversations = conversation_list.get_all(include_archived=False)

    print('{} known users'.format(len(all_users)))
    for user in all_users:
        print('    {}: {}'.format(user.full_name, user.id_.gaia_id))

    print('{} known conversations'.format(len(all_conversations)))
    for conversation in all_conversations:
        if conversation.name:
            name = conversation.name
        else:
            name = 'Unnamed conversation: '
        print('    {}: {}'.format(name, conversation.id_))

run_example(sync_recent_conversations)