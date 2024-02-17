import os
import random

label_name = "SEK"
# 指定源文件夹和目标文件夹
src_dir = "/d9lab/songjie/datasets/mydataset_semi/sample_images/" + label_name
val_dir = "/d9lab/songjie/datasets/mydataset_semi/sample_images/val/" + label_name
train_dir = "/d9lab/songjie/datasets/mydataset_semi/sample_images/train/" + label_name

# 确保目标文件夹存在
if not os.path.exists(val_dir):
    os.makedirs(val_dir)
if not os.path.exists(train_dir):
    os.makedirs(train_dir)

# 获取源文件夹中所有文件的列表
files = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]

if len(files) == 0:
    print("文件夹为空")
    exit()

# 随机抽取500个文件
random.shuffle(files)
selected_files = files[:500]

# 移动文件
for file in files:
    src_file = os.path.join(src_dir, file)
    if file in selected_files:
        dst_file = os.path.join(val_dir, file)
    else:
        dst_file = os.path.join(train_dir, file)
    os.rename(src_file, dst_file)