import json

import requests
from django.http import JsonResponse
import thulac
from django.shortcuts import render
from json import dumps


# Create your views here.

from qa import models


def qa_list(request):
    if request.method == 'POST':
        new_q = json.loads(request.body)
        print(new_q)
        new_question = new_q.get("que")
        thu1 = thulac.thulac()  # 默认模式
        result = thu1.cut(new_question, text=True)
        seg = result.split(' ')
        im = []
        for str in seg:
            l = str.split('_')
            im.append(l)
        imp = []
        i = 0
        print(im)
        while i < len(im):
            if im[i][1] == 'n':
                temp = im[i][0]
                j = i + 1
                while j < len(im) and im[j][1] == 'n':
                    temp = temp + im[j][0]
                    j = j + 1
                print(temp)
                i = j
                imp.append(temp)
            else:
                i = i + 1
        new_question = "问题:" + new_question
        new_question = new_question + "关键词:"
        for s in imp:
            new_question = new_question + s + ' '
        new_question = new_question + "回答:"
        url = "http://lab.aminer.cn/isoa-2021/gpt"
        data = {
            "token": "b84fc35e83491ca74dc1afe651bc2530",
            "app": "qa",
            "content": new_question
        }
        headers = {'Content-Type': 'application/json'}
        new_a = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(new_a.text)
        new_an = json.loads(new_a.text)["result"]
        new_answer = new_an["content"]
        data = {
            "token": "b84fc35e83491ca74dc1afe651bc2530",
            "app": "chat",
            "content": new_answer
        }
        new_a = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(new_a.text)
        new_answer = json.loads(new_a.text)["result"]
        qa = models.Qa(question=new_question, answer=new_answer)
        qa.save()
        return JsonResponse({
            "answer": new_answer
        }, status=200)
