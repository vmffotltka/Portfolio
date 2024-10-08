# -*- coding: utf-8 -*-
"""oneClickCrawler.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bS-dAW0DJ2atsx-scQU6D2OgbU2-bLoy
"""

from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd
import datetime as dt
import os.path
from os import path

class oneClickCrawler:

  def crawler(self,category_num):
    self.category_num = category_num
    #웹브라우져 헤더 추가
    #User-Agent를 조작하는 경우
    hdr =  {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    req = urllib.request.Request('https://prod.danawa.com/list/?cate='+category_num, headers = hdr)
    data = urllib.request.urlopen(req).read()
    page = data.decode('utf-8','ignore')
    soup = BeautifulSoup(page, 'html.parser')
    prod_items = soup.select('div.main_prodlist > ul.product_list > li.prod_item')
    return prod_items

  def cpu_crawler(self, link):
    self.link = link
    crawled_data = self.crawler(link)
    i=0
    partslist = []
    for item in crawled_data:
        if i==30: break;
        # strip 메서드로 앞 뒤 공백 제거
        name = item.select_one('p > a').get_text()[8:].strip() # 부품명
        price = item.select_one('p > a > strong').get_text() # 가격
        details = item.select_one('div.spec-box--full').get_text()
        details = re.split("[/'\n']", details) # 상세정보들
        if link[-6:] == '113973': # intel 소캣 split
            socket = details[0].strip()[5:-1] if details else 'N/A'
        elif link[-6:] == '113990': # amd 소켓 splite
            socket = details[0].strip()[6:-1] if details else 'N/A'
        integrated_graphics = True if '내장그래픽: 탑재' in details else False # 내장그래픽
        for detail in details:
            if '메모리 규격' in detail:
                memory_type = str(detail[8:])
            if '시네벤치R23(싱글)' in detail:
                singlebench = detail[13:]
            if '시네벤치R23(멀티)' in detail:
                multibench = detail[13:]
        partslist.append([name, price, socket, integrated_graphics, memory_type, singlebench, multibench])
        i+=1
    result = pd.DataFrame(partslist, columns=['Product Name', 'Price', 'Socket', 'Integrated Graphics','메모리 타입','시네벤치R23(싱글)','시네벤치R23(멀티)'])
    return result

  def memory_crawling(self, link):
    self.link = link
    crawled_data = self.crawler(link)
    i=0
    partslist = list()
    for item in crawled_data:
        if i==30: break;
        storage = item.select('div.over_preview > p.memory_sect > span.text')
        price = item.select('p > a > strong')
        for j in range(len(storage)):
            name = item.select_one('p > a').get_text()[8:].strip() # 부품명 # strip 메서드로 앞 뒤 공백 제거
            details = item.select_one('div.spec-box.spec-box--full > div.spec_list').get_text().split('/') # 상세정보들
            speed = details[2] # 메모리 클럭
            price_ = price[j].get_text()
            storage_ = storage[j].get_text()
            if(len(storage_)) == 3: # 8GB나 4GB인 애들은 길이가 3이니까
                storage_ = str(int(storage_[:1])*2)+'GB('+storage_[:1]+'Gx2)'
            elif len(storage_) == 4: # 16GB~64GB까지
                storage_ = str(int(storage_[:2])*2)+'GB('+storage_[:2]+'Gx2)'
            elif len(storage_) == 5: # 128GB~512GB 까지
                storage_ = str(int(storage_[:3])*2)+'GB('+storage_[:3]+'Gx2)'
            partslist.append([name, price_, storage_, speed])
        i+=1
    result = pd.DataFrame(partslist, columns=['Product Name', 'Price','Storage', 'Speed'])
    return result

  # 메인보드 크롤링
  def board_crawling(self, link):
    self.link = link
    crawled_data = self.crawler(link)
    i=0
    partslist = list()
    for item in crawled_data:
        if i==30: break;
        # strip 메서드로 앞 뒤 공백 제거
        name = item.select_one('p > a').get_text()[8:].strip() # 부품명
        price = item.select_one('p > a > strong').get_text() # 가격
        details = item.select_one('div.spec-box.spec-box--full > div.spec_list').get_text().split('/') # 상세정보들
        socket_type = re.split("[()]", details[0])[1][2:] # details 중 0 번째에 위치하고 있으며, AMD(소캣AM5) 이런식으로 되어 있어서 쪼갰음
        # print(socket_type)
        for idx in range(len(details)):
            if '메모리' in details[idx]:
                memory_type = str(details[idx][4:])
                memory_speed = str(details[idx+1].split()[0])
                break
        size = details[2].split()[0]
        partslist.append([name, price, socket_type, memory_type, memory_speed, size])
        i+=1
    result = pd.DataFrame(partslist, columns=['Product Name', 'Price', 'Socket_type', 'Memory_Type','Memory_Speed', 'Size'])
    return result

  def gpu_crawling(self, link):
    self.link = link
    crawled_data = self.crawler(link)
    i=0
    partslist = list()
    for item in crawled_data:
        if i==30: break;
        # strip 메서드로 앞 뒤 공백 제거
        name = item.select_one('p > a').get_text()[8:].strip() # 부품명
        price = item.select_one('p > a > strong').get_text() # 가격
        details = item.select_one('div.spec-box.spec-box--full > div.spec_list').get_text().split('/') # 상세정보들
        for idx in range(len(details)):
            if '정격파워' in details[idx]:
                # power_usage = str(details[idx].split()[1])
                power_type = str(details[idx].split()[1])
            if '가로(길이)' in details[idx]:
                size = str(details[idx].split()[1])
                break
        partslist.append([name, price, power_type, size])
        i+=1
    result = pd.DataFrame(partslist, columns=['Product Name', 'Price', 'Power_Type', '가로(길이)'])
    return result

  # 파워 크롤링
  def power_crawling(self, link):
    self.link = link
    crawled_data = self.crawler(link)
    i=0
    partslist = list()
    for item in crawled_data:
        if i==30: break;
        # strip 메서드로 앞 뒤 공백 제거
        name = item.select_one('p > a').get_text()[8:].strip() # 부품명
        price = item.select_one('p > a > strong').get_text() # 가격
        # link =
        details = item.select_one('div.spec-box.spec-box--full > div.spec_list').get_text().split('/') # 상세정보들
        for idx in range(len(details)):
            if '파워' in details[idx]:
                power_size = str(details[idx].split()[0])
            if '정격출력' in details[idx]:
                output = str(details[idx].split()[1])
                break
        partslist.append([name, price, power_size, output])
        i+=1
    result = pd.DataFrame(partslist, columns=['Product Name', 'Price', '파워규격', '정격출력'])
    return result

  # 케이스 크롤링 - 원래 방식
  def case_crawling(self, link):
    self.link = link
    crawled_data = self.crawler(link)
    i=0
    partslist = list()
    for item in crawled_data:
        if i==30: break;
        # strip 메서드로 앞 뒤 공백 제거
        name = item.select_one('p > a').get_text()[8:].strip() # 부품명
        price = item.select_one('p > a > strong').get_text() # 가격
        # link =
        details = item.select_one('div.spec-box.spec-box--full > div.spec_list').get_text().split('/') # 상세정보들
        for idx in range(len(details)):
            if 'VGA 장착 길이' in details[idx]:
                vga_length = str(details[idx].split()[3])
            if 'CPU쿨러 장착높이' in details[idx]:
                cpuCooler_height = str(details[idx].split()[2])
                break
        partslist.append([name, price, vga_length, cpuCooler_height])
        i+=1
    result = pd.DataFrame(partslist, columns=['Product Name', 'Price', 'VGA 장착길이', 'CPU쿨러 장착높이'])
    return result

# 오늘 날짜의 폴더 생성
today = str(dt.datetime.now().date())
os.mkdir(today)

oc = oneClickCrawler()
# CPU
intel_link ='113973'
amd_link = '113990'
intel_cpu = oc.cpu_crawler(intel_link)
amd_cpu = oc.cpu_crawler(amd_link)
intel_cpu.to_csv(today+'/intel.csv',encoding='cp949', index=False)
amd_cpu.to_csv(today+'/amd.csv',encoding='cp949', index=False)

# RAM
ddr4_link = '1131326'
ddr5_link = '11341201'
ddr4 = oc.memory_crawling(ddr4_link)
ddr5 = oc.memory_crawling(ddr5_link)
ddr4.to_csv(today+'/ddr4.csv',encoding='cp949', index=False)
ddr5.to_csv(today+'/ddr5.csv',encoding='cp949', index=False)

# MAINBOARD
amd_board_link = '1131249'
intel_board_link = '11345282'
amd_board = oc.board_crawling(amd_board_link)
intel_board = oc.board_crawling(intel_board_link)
amd_board.to_csv(today+'/amd_board.csv',encoding='cp949', index=False)
intel_board.to_csv(today+'/intel_board.csv',encoding='cp949', index=False)

# GPU 크롤링
gpu_link = '112753'
gpu = oc.gpu_crawling(gpu_link)
gpu.to_csv(today+'/gpu.csv',encoding='cp949', index=False)

# POWER
power_link = '11338807' # 80 PLUS 인증 파워만 가져옴
power = oc.power_crawling(power_link)
power.to_csv(today+'/power.csv',encoding='cp949', index=False)

# CASE
case_link = '113971'
case = oc.case_crawling(case_link)
case.to_csv(today+'/case.csv',encoding='cp949', index=False)