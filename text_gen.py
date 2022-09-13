import pandas as pd
import numpy as np

all_dataset = pd.read_csv('all_datasets.csv')

all_np_title = all_dataset['title'].to_numpy()

np.savetxt('title.txt', all_np_title, fmt='%s')

from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2ConfigCPU
from aitextgen import aitextgen

# The name of the downloaded Shakespeare text for training
file_name = "title.txt"

# Train a custom BPE Tokenizer on the downloaded text
# This will save one file: `aitextgen.tokenizer.json`, which contains the
# information needed to rebuild the tokenizer.
train_tokenizer(file_name)
tokenizer_file = "aitextgen.tokenizer.json"

# GPT2ConfigCPU is a mini variant of GPT-2 optimized for CPU-training
# e.g. the # of input tokens here is 64 vs. 1024 for base GPT-2.
config = GPT2ConfigCPU()

# Instantiate aitextgen using the created tokenizer and config
ai = aitextgen(tokenizer_file=tokenizer_file, config=config)

# You can build datasets for training by creating TokenDatasets,
# which automatically processes the dataset with the appropriate size.
data = TokenDataset(file_name, tokenizer_file=tokenizer_file, block_size=64)

# Train the model! It will save pytorch_model.bin periodically and after completion to the `trained_model` folder.
# On a 2020 8-core iMac, this took ~25 minutes to run.
ai.train(data, batch_size=8, num_steps=10000, generate_every=5000, save_every=5000)

# Generate text from it!
#ai.generate(10)

title_temp = []
title_temp = ai.generate(1000,return_as_list=True)

title_ls = []

for i in range (len(title_temp)):
    title_temp[i] = title_temp[i].split("\n")
    for j in range (len(title_temp[i])):
        if title_temp[i][j] != '':
            title_ls.append(title_temp[i][j])

 title_temp2 = json.dumps(title_ls)
f = open("title_list.json","w")
f.write(title_temp2)
f.close()

all_np_desc = all_dataset['description'].to_numpy()
np.savetxt('desc.txt', all_np_desc, fmt='%s')

file_name = "desc.txt"

# Train a custom BPE Tokenizer on the downloaded text
# This will save one file: `aitextgen.tokenizer.json`, which contains the
# information needed to rebuild the tokenizer.
train_tokenizer(file_name)
tokenizer_file = "aitextgen.tokenizer.json"

# GPT2ConfigCPU is a mini variant of GPT-2 optimized for CPU-training
# e.g. the # of input tokens here is 64 vs. 1024 for base GPT-2.
config = GPT2ConfigCPU()

# Instantiate aitextgen using the created tokenizer and config
ai_desc = aitextgen(tokenizer_file=tokenizer_file, config=config)

# You can build datasets for training by creating TokenDatasets,
# which automatically processes the dataset with the appropriate size.
data2 = TokenDataset(file_name, tokenizer_file=tokenizer_file, block_size=64)

# Train the model! It will save pytorch_model.bin periodically and after completion to the `trained_model` folder.
# On a 2020 8-core iMac, this took ~25 minutes to run.
ai_desc.train(data2, batch_size=8, num_steps=1000, generate_every=5000, save_every=5000)

desc_temp = []
desc_temp = ai_desc.generate(2000,return_as_list=True)

desc_js = json.dumps(desc_temp)
f = open("desc_list.json","w")
f.write(desc_js)
f.close()

with open('desc_list.json') as json_file:
    desc_list = json.load(json_file)