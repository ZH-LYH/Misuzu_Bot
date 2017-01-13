# -- coding: UTF-8 --
import telepot
import time
import urllib.request
import json

#bot配置
token = '295778546:AAGB41vL07u6Vm_uVpzfk_DjYNeB1Mj7j-E'
username = '@Misuzu_Bot'

bot = telepot.Bot(token)

#消息处理
def handle(msg) :
       content_type, chat_type, chat_id, date, msg_id = telepot.glance(msg,'chat',True)
       chat_id = int(chat_id)
       print(content_type, chat_type, chat_id, date, msg_id)
       if content_type == 'text' :
              cmd = msg['text']
              print(msg['text'])
              if cmd.startswith('/') :
                     if cmd.startswith('/help'):
                            bot_help(chat_id)
                     elif cmd.startswith('/weather'):
                            weather(cmd,chat_id)
                     elif cmd.startswith('/hitokoto'):
                            hitokoto(chat_id)
                     else:
                            bot_error(chat_id)


#帮助
def bot_help(chat_id):
       help_msg = '''
/help -帮助
/weather -天气查询
'''
       bot.sendMessage(chat_id, help_msg)

#天气查询
def weather(cmd,chat_id):
       weather = parse_cmd(cmd, '/weather')
       if weather == '':
              bot.sendMessage(chat_id,'输入城市小観鈴才能帮主人查询哦')
       else:
              weatherUrl = 'https://free-api.heweather.com/v5/now?city='+urllib.parse.quote(weather)+'&key=83a2bdf7d08c4167ac16c2ee277d22ed'
              #print(weatherUrl)
              stdout = urllib.request.urlopen(weatherUrl)
              weatherInfo = stdout.read().decode('utf-8')
              weatherJsonData = json.loads(weatherInfo)
              bot.sendMessage(chat_id,'小観鈴为主人找到了'+weatherJsonData['HeWeather5'][0]['basic']['city']+'的天气\n天气状况:'+weatherJsonData['HeWeather5'][0]['now']['cond']['txt']+'  '+weatherJsonData['HeWeather5'][0]['now']['wind']['sc']+'级'+weatherJsonData['HeWeather5'][0]['now']['wind']['dir']+'\n温度:'+weatherJsonData['HeWeather5'][0]['now']['tmp']+'℃\n体感温度:'+weatherJsonData['HeWeather5'][0]['now']['fl']+'℃\n相对湿度:'+weatherJsonData['HeWeather5'][0]['now']['hum']+'%\n降水量:'+weatherJsonData['HeWeather5'][0]['now']['pcpn']+' mm\n气压:'+weatherJsonData['HeWeather5'][0]['now']['pres']+'\n能见度:'+weatherJsonData['HeWeather5'][0]['now']['vis']+'km')
              
              
"""def weather(cmd,chat_id):
       weather = parse_cmd(cmd, '/weather')
       if weather == '':
              bot.sendMessage(chat_id, '输入城市小観鈴才能帮主人查询哦')
       else:
              if weather == '汕头':
                     citycode = '101280501'
              elif weather == '深圳':
                     citycode = '101280601'
              else:
                     citycode = '小観鈴找不到这个城市的天气哟'
              bot.sendMessage(chat_id,citycode)
"""

def hitokoto(chat_id):
       hitokotoUrl = 'http://api.hitokoto.cn'
       stdout = urllib.request.urlopen(hitokotoUrl)
       hitokotoInfo = stdout.read().decode('utf-8')
       hitokotoJsonData = json.loads(hitokotoInfo)
       bot.sendMessage(chat_id,hitokotoJsonData['hitokoto']+'\n ── '+hitokotoJsonData['from'])

# 错误信息
def bot_error(chat_id):
       error_msg = '小観鈴好像并不明白 QwQ'
       bot.sendMessage(chat_id, error_msg)

# 命令预处理
def parse_cmd(cmd, func):
       return cmd.lstrip(func).lstrip(username).strip(' ').replace('\n','')

#开始运行
bot.message_loop(handle)

while 1:
       time.sleep(10)
