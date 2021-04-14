#!/usr/bin/env python3
from transformers import BertTokenizer, BertModel
import torch
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')
input_ids = torch.tensor(tokenizer.encode("赴澳放假啊冯绍峰萨法，法萨法萨法沙发上舒服啊啊师傅啊师傅嘎嘎嘎")).unsqueeze(0)  # Batch size 1
outputs = model(input_ids)
last_hidden_states = outputs[0]  # The last hidden-state is the first element of the output tuple
print(last_hidden_states)