import json

import requests
from django.http import JsonResponse
import thulac
import jieba.analyse
import textwrap
from transformers import BertTokenizer, BertModel
import torch
# import jieba.posseg as pseg
from django.shortcuts import render
from json import dumps

# Create your views here.

from qa import models

waiting_list = {}

def qa_list(request):
    if request.method == 'POST':
        t1 = MyTimer()
        new_q = json.loads(request.body)
        print(new_q)
        new_question = new_q.get("que")
        #temp = new_question
        imp = jieba.analyse.extract_tags(new_question, topK=4)
        # t1.start()
        # tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        # model = BertModel.from_pretrained('bert-base-chinese')
        # # model.to_('cuda:0')
        # input_ids = torch.tensor(tokenizer.encode("赴澳放假啊冯绍峰萨法，法萨法萨法沙发上舒服啊啊师傅啊师傅嘎嘎嘎")).unsqueeze(0)  # Batch size 1
        # outputs = model(input_ids)
        # last_hidden_states = outputs[0]  # The last hidden-state is the first element of the output tuple
        # print(last_hidden_states)
        # t1.stop()
        # print(t1.prompt)
        #t2 = MyTimer()
        #t2.start()
        #thu1 = thulac.thulac()  # 默认模式
        #result = thu1.cut(new_question, text=True)
        #t2.stop()
        #print(t2.prompt)
        #seg = result.split(' ')
        #im = []
        #for str in seg:
            #l = str.split('_')
            #im.append(l)
        #imp = []
        #i = 0
        #print(im)
        #while i < len(im):
            #if im[i][1][0] == 'n':
                #temp = im[i][0]
                #j = i + 1
                #while j < len(im) and im[j][1] == 'n':
                    #temp = temp + im[j][0]
                    #j = j + 1
                # print(temp)
                #i = j
                #imp.append(temp)
            #else:
                #i = i + 1
        new_question = "问题:" + new_question
        new_question = new_question + "关键词:"
        i = -1
        # for s in imp:
        #     new_question = new_question + s + ' '
        #     i = i + 1
        #     if i >= 3:
        #         break
        new_question = new_question + ' 问题描述：' + new_question
        new_question = ' '.join((new_question, ' '.join(imp)))
        new_question = new_question + " 回答用户：大学生" + " 回答:"
        print(new_question)
        if waiting_list.__contains__(new_question):
            new_answer = waiting_list[new_question]
            del waiting_list[new_question]
        else:
            url = "http://lab.aminer.cn/isoa-2021/gpt"
            data = {
                "token": "b84fc35e83491ca74dc1afe651bc2530",
                "app": "qa",
                "content": new_question
            }
            headers = {'Content-Type': 'application/json'}
            t1.start()
            new_a = requests.post(url=url, data=json.dumps(data), headers=headers)
            print(new_a.text)
            new_an = json.loads(new_a.text)["result"]
            new_answer = new_an["content"]
            # new_answer = "反而啊说到发都上风我日小在出在小册特惹尔小发到说沣i鹅u日欧容ID离开算法但是丰富而成"
            # new_answer = '\n'.join(textwrap.wrap(new_answer, 15))
            print(new_answer)
        # data = {
        # "token": "b84fc35e83491ca74dc1afe651bc2530",
        # "app": "chat",
        # "content": new_answer
        # }
        # new_a = requests.post(url=url, data=json.dumps(data), headers=headers)
        # print(new_a.text)
        # new_answer = json.loads(new_a.text)["result"]
            qa = models.Qa(question=new_question, answer=new_answer)
            qa.save()
            t1.stop()
            print(t1.prompt)
            if int(t1.prompt) > 6 and not waiting_list.__contains__(new_question):
                waiting_list[new_question] = new_answer
                print(waiting_list)
        return JsonResponse({
            "answer": new_answer
        }, status=200)


import time as t


class MyTimer:
    # 开始计时
    def start(self):
        self.begin = t.localtime()
        self.prompt = '提示：请先用stop()停止计时'
        print('开始计时')

    # 停止计时
    def stop(self):
        if not self.begin:
            print('提示：请先用start()开始计时')
        else:
            self.end = t.localtime()
            self._calc()
            print('计时结束')

    # 计时器相加
    def __add__(self, other):
        prompt = ''
        result = []
        for index in range(6):
            result.append(self.lasted[index] + other.lasted[index])
            if result[index]:
                prompt = prompt + (str(result[index]))
        return prompt

    def __init__(self):
        self.unit = ['年', '月', '天', '小时', '分钟', '秒']
        self.borrow = [0, 12, 31, 24, 60, 60]
        self.prompt = '未开始计时'
        self.lasted = []
        self.begin = 0
        self.end = 0

    def __str__(self):
        return self.prompt  # 重写__str__魔法方法，程序在调用print函数时，打印当时状态的prompt内容

    __repr__ = __str__  # 将__repr__和__str__相同化

    # 内部方法，计算运行时间
    def _calc(self):
        self.lasted = []  # 制作一个空列表，存放每个单位相减的值
        self.prompt = ''
        for index in range(6):
            temp = self.end[index] - self.begin[index]
            if temp < 0:
                i = 1
                while self.lasted[index - i] < 1:  # 向前边的位数借
                    self.lasted[index - i] += self.borrow[index - i] - 1
                    self.lasted[index - i - 1] -= 1
                    i += 1  # 向更高位借
                self.lasted.append(self.borrow[index] + temp)
                self.lasted[index - 1] -= 1
            else:
                self.lasted.append(temp)
        for index in range(6):
            self.lasted.append(self.end[index] - self.begin[index])
            if self.lasted[index]:
                self.prompt += str(self.lasted[index])

        # 为下一轮计时初始化变量
        self.begin = 0
        self.end = 0
