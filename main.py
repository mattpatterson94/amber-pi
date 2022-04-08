from dotenv import load_dotenv
import requests
import json
import os
import epaper
from PIL import Image,ImageDraw,ImageFont

load_dotenv()

def get_electricity_prices():
  amber_api_key = os.getenv('AMBER_API_KEY')
  site_id = os.getenv('SITE_ID')

  response = requests.get(
    f'https://api.amber.com.au/v1/sites/{site_id}/prices/current?next=1&previous=1&resolution=30',
    headers = {
      "Authorization": f'Bearer {amber_api_key}',
      "accept": "application/json"
    }
  )
  intervals = json.loads(response.text)

  general_intervals = list(filter(lambda interval: interval['channelType'] == 'general', intervals))

  return general_intervals

def format_price(price):
  return f'{round(price)}¢'

def display_current_price(epd, draw, price):
  font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Font.ttc'), 48)
  content = format_price(price['perKwh'])
  w, h = draw.textsize(content, font = font)
  left = (epd.height - w) / 2
  top = (epd.width - h) / 2

  draw.text((left, top), content, font = font, fill = 0)

def display_prev_price(epd, draw, price):
  font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Font.ttc'), 24)
  content = format_price(price['perKwh'])
  w, h = draw.textsize(content, font = font)
  left = 10
  top = (epd.width - h) / 2

  draw.text((left, top), content, font = font, fill = 0)

def display_next_price(epd, draw, price):
  font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Font.ttc'), 24)
  content = format_price(price['perKwh'])
  w, h = draw.textsize(content, font = font)
  left = epd.height - (w + 10)
  top = (epd.width - h) / 2

  draw.text((left, top), content, font = font, fill = 0)

def display_electricity_prices(prices):
  epaper_model = os.getenv('EPAPER_MODEL')
  epd = epaper.epaper(epaper_model).EPD()
  epd.init(epd.FULL_UPDATE)
  epd.Clear(0xFF)

  image = Image.new('1', (epd.height, epd.width), 255)
  draw = ImageDraw.Draw(image)

  display_prev_price(epd, draw, prices[0])
  display_current_price(epd, draw, prices[1])
  display_next_price(epd, draw, prices[2])

  epd.display(epd.getbuffer(image))

prices = get_electricity_prices()
display_electricity_prices(prices)
