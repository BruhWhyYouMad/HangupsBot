import requests
import shutil
import sys

print(sys.path[0])
img_path = sys.path[0].replace('/tools', '/data/meme.jpg')

# reddit = asyncpraw.Reddit(client_id='q0NliLq94yzJ0A',
#                      client_secret='HqOybjTmMX63yyxKbqJ4OaxgH_SSYA',
#                      user_agent='Discord Meme Bot')



def get_meme():
  # sub = await reddit.subreddit("dankmemes")
  # meme = await sub.random()
  # await reddit.close()
  # image_url = meme.url
  # r = requests.get(image_url, stream = True)
  #r.raw.decode_content = True
  r = requests.get('https://meme-api.herokuapp.com/gimme/memes')
  print(r.json()["url"])
  if r.json()["nsfw"] == True:
    nsfw_url = "https://i.ibb.co/8rn2th1/5-C79-EA2-D-DA52-4-E84-9-A47-7-EEB663014-E7.png"
    img_request = requests.get(nsfw_url, stream = True)
    with open('/home/runner/HangupsBot/data/meme.jpg','wb') as f:
      shutil.copyfileobj(img_request.raw, f)
  else:
    img_request = requests.get(r.json()["url"], stream = True)
    with open('/home/runner/HangupsBot/data/meme.jpg','wb') as f:
      shutil.copyfileobj(img_request.raw, f)
