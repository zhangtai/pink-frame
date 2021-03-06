#!venv/bin/python3
import subprocess

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
import requests
import json


def main():
    urls = {'gz': 'https://weather.com/zh-CN/weather/today/l/8531a23947fdad24dcfb9cd37e6d6bd77617fa7c8b242e4773c74381cf55845b',
            'yl': 'https://weather.com/zh-CN/weather/today/l/9de9f2a3405e9d73c726ff55c4d29e922ea72308adfa5b47742d5fea473ef105'}
    output_path = 'output/'
    input_path = 'resources/'

    for url_key, url in urls.items():
        load_page(url_key, url, output_path)

    sensor_img = produce_sensor_data(input_path, output_path)

    im_name = create_new_postcard(output_path, sensor_img)

    subprocess.call(['sudo', './pf', f"{output_path}{im_name}"])


def load_page(url_key, url, output_path):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(800, 3000)

    driver.get(url)
    get_screenshot_of_element(output_path, driver, url_key)

    driver.close()
    driver.quit()


def get_screenshot_of_element(output_path, driver, url_key):
    elements = {'current': 'WxuCurrentConditions-main-b3094163-ef75-4558-8d9a-e35e6b9b1034',
                'main': 'WxuTodayWeatherCard-main-486ce56c-74e0-4152-bd76-7aea8e98520a',
                'detail': 'todayDetails'}
    for ele_key, ele in elements.items():
        image_name = url_key + ele_key + '.png'
        driver.find_element_by_id(ele).screenshot(output_path + image_name)


def create_new_postcard(output_path, sensor_img):
    bgimage = Image.new('RGB', (1872, 1404), (255, 255, 255))
    imlist = {'gzcurrent.png': (60, 40), 'gzmain.png': (60, 300), 'gzdetail.png': (60, 660),
     'ylcurrent.png': (720, 40), 'ylmain.png': (720, 300), 'yldetail.png': (720, 660)}

    for im_key, image in imlist.items():
        imtemp = Image.open(output_path + im_key)
        resized_im = imtemp.resize((round(imtemp.size[0] * 1.35), round(imtemp.size[1] * 1.35)))
        offset = imlist[im_key]
        bgimage.paste(resized_im, offset)

    sensor_offset_y = 60
    for sensor_item in sensor_img:
        sim = Image.open(output_path + sensor_item)
        sensor_offset_x = 1450
        bgimage.paste(sim, (sensor_offset_x, sensor_offset_y))
        sensor_offset_y += 410

    timestamp = f'{datetime.now():%Y%m%d%H%M%S%z}'
    im_name = 'weather_postcard' + timestamp + '.png'
    base_dir = os.getcwd()
    path = os.path.join(base_dir, output_path, im_name)
    bgimage.save(path, 'bmp')

    os.system(f"cd {output_path} && rm -rf gz* yl* sensor*")
    return im_name


def produce_sensor_data(input_path, output_path):
    base_url = f"{HOME_ASSISTANT_SERVER}/api/states/sensor."
    headers = {
        "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
        "Content-Type": "application/json",
    }
    sensor_list = {"Living Room": '158d000201ba3f', "Bedroom": '158d0002028531', "Reading Room": '158d0004072c42'}
    sensor_img = []
    title_font = ImageFont.truetype("examples/Arial.ttf", 28)
    data_font = ImageFont.truetype("examples/Arial.ttf", 45)

    for key, sensor in sensor_list.items():
        temp_url = base_url + 'temperature_lumi_' + sensor_list[key]
        humi_url = base_url + 'humidity_lumi_' + sensor_list[key]
        temperature = requests.request("GET", temp_url, headers=headers).json()['state'] + ' ??C'
        humidity = requests.request("GET", humi_url, headers=headers).json()['state'] + ' %'

        temp_img = Image.open(input_path + 'sensor_bg.png')
        draw = ImageDraw.Draw(temp_img)
        draw.text(((temp_img.width - title_font.getsize(key)[0]) / 2, 90), key, (255, 255, 255), font=title_font, align='center')
        draw.text(((temp_img.width - data_font.getsize(temperature)[0]) / 2, 145), temperature, (255, 255, 255), font=data_font, align='center')
        draw.text(((temp_img.width - data_font.getsize(humidity)[0]) / 2, 210), humidity, (255, 255, 255), font=data_font, align='center')
        draw.line((90, 200, 250, 200), width=3)
        sensor_img_name = 'sensor' + key + '.png'
        temp_img.save(output_path + sensor_img_name)
        sensor_img.append(sensor_img_name)
    return sensor_img


if __name__ == "__main__":
    main()
