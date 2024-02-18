from datetime import datetime
import os, runpy, sys, typing, json, requests

# 对每次训练权重文件夹的命名
now = lambda: datetime.now().strftime("%Y%m%d_%H%M%S")

def sendDingTalkMessage(msg: str = None):
    # 替换成你的钉钉机器人的access_token，也可以直接用我的
    dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=bfd6ed1edee89290b9d5098db63691b55f9b97bdd9c5eb69788df32e4f01e203"
    dingding_headers = {'Content-Type': 'application/json'}

    message_content = "daka, finish time is " + now() + "\n" + msg

    payload = {
        "msgtype": "text",
        "text": {
            "content": message_content
        }
    }
    # 请求钉钉api，发送钉钉提醒
    requests.post(dingding_url, headers=dingding_headers, data=json.dumps(payload))

# 对每次训练权重文件夹的命名
now = lambda: datetime.now().strftime("%Y%m%d_%H%M%S")
autodl_pre = "/root/autodl-tmp/datasets"
d9lab_pre = "/d9lab/songjie/datasets"
data_dir_prefix = d9lab_pre if os.uname().nodename.startswith("h3c") else autodl_pre

def run(command: str or list[str]): # type: ignore
    # 以下是执行程序
    args = command.split()
    if args[0] == "python":
        args.pop(0)
    if args[0] == '-m':
        args.pop(0)
        fun = runpy.run_module
    else:
        fun = runpy.run_path
    sys.argv.extend(args[1:])
    fun(args[0], run_name="__main__")
    
def train():
    return f"python train.py --c config/usb_cv/meanteacher/meanteacher_cifar100_200_0.yaml \
    --model_pth_dir ./save_models/usb_cv/meanteacher_mydataset/{now()} \
    --use_wandb --wandb_run_name=MeanTeacher_use_amp \
    --wandb_notes 开启半精，并将batch扩大一倍，各iter缩小1/2，看看效果"
    
# 切换不同的脚本
# command = [timm for _ in range(3)] # 重复执行5次
command = train

auto_shutdown = False

if callable(command):
    run(command())
elif isinstance(command, list):
    for cmd in command:
        if callable(cmd):
            run(cmd())
        else:
            raise TypeError("command must be callable or list of callables")
else:
    raise TypeError("command must be callable or list of callables")

sendDingTalkMessage("训练完成")

# python fast_commands.py > output.log 2>&1
# tar cf - * | ssh -p 22 h3c@10.108.201.73 "cd /d9lab/songjie/datasets/mydataset_semi && tar xf -"