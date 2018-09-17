# -*- coding: utf-8 -*-
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
import time
import signal
from plugins import analytic
import random
# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')      @発言者名: string でメッセージを送信
# message.send('string')       string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                              文字列中に':'はいらない

@respond_to('detect')
def mention_func(message):
    s=time.time()
    message.reply("Wait for about 30 seconds, please.")
    det=analytic.detect()
    message.reply(det[0])
    e=time.time()-s
    end="Finished in {0}".format(e) + "sec."
    message.reply(end)

@respond_to('table')
def mention_func(message):
    s=time.time()
    message.reply("Wait for about 30 seconds, please.")
    det=analytic.detect()
    res =analytic.think(det[1])
    if type(res)==str :
        message.reply(res)
    else:
        r='\ntable1:'+str(res[0])+'\ntable2:'+str(res[1])+'\ntable3:'+str(res[2])
        message.reply(r)
        fin=analytic.upload(det[1])
        message.reply(fin)
    e=time.time()-s
    end="Finished in {0}".format(e) + "sec."
    message.reply(end)

@respond_to('clear')
def mention_func(message):
    res=analytic.clear()
    message.reply(res)

@respond_to('loop')
def mention_func(message):
    message.reply("I'll loop for 3 hours.")
    for n in range(36):
        s=time.time()
        message.reply("\nWait for about 30 seconds, please.")
        det=analytic.detect()
        res =analytic.think(det[1])
        if type(res)==str :
            message.reply(res)
        else:
            r='\ntable1:'+str(res[0])+'\ntable2:'+str(res[1])+'\ntable3:'+str(res[2])
            message.reply(r)
            fin=analytic.upload(det[1])
            message.reply(fin)
        e=time.time()-s
        end="Finished in {0}".format(e) + "sec."
        message.reply(end)
        time.sleep(270)
    bye=analytic.clear()
    message.reply(bye)

@respond_to('help')
def mention_func(message):
    message.reply("detect: I'll give you a JASON.\ntable: I'll reply how many people are in three table. Table3 is a table near the fridge.\nloop: I'll loop 'table' for (time to reply + 270sec)x36.\nclear: I'll delete temp file.\nhello: ????")

@respond_to('hello')
def mention_func(message):
    str=[
        "I feel the need—the need for speed!",
        "Open the pod bay doors please, HAL.",
        "Hasta la vista, baby.",
        "Elementary, my dear Watson.",
        "Houston, we have a problem.",
        "I'll be back.",
        "There's no place like home.",
        "The name is Bond. James Bond.",
        "E.T. phone home.",
        "May the Force be with you.",
        "No! Try not. Do. Or do not. There is no try.",
        "Fear is the path to the dark side. Fear leads to anger. Anger leads to hate. Hate leads to suffering.",
        "Remember, the Force will be with you, always.",
        "Use the Force, Luke. Let go, Luke.",
        "I'm a Jedi, like my father before me.",
        "It's a trap!",
        "movie famous line by Koki. lol"
    ]
    n = random.randint(0,16)
    message.reply(str[n])
