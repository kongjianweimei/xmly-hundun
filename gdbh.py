#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
功能: 果冻宝盒看广告、签到任务，每天0.7元 ，新注册的用户好像可以零撸实物，软件出来好几年了只要号不黑基本上不会跑路
TG交流 https://t.me/jd_wool
TG频道 https://t.me/jd_wool_notify1
建议cron: 10 7 * * *  python3 gdbh.py
new Env('果冻宝盒');
软件下载：https://wwa.lanzoui.com/iTPUfvk7x7i
脚本地址：https://raw.githubusercontent.com/gcdd1993/My-Scripts/master/other/gdbh.py
邀请码：3V67Q2 感谢支持
教程：
"""

import datetime
import hashlib
import json
import random
import sys
import time

import requests


def print_ts(s):
    print("[{0}]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s))
    sys.stdout.flush()


def checkin(userinfo):
    """
    每日签到
    """
    timestamp = str(int(time.time()))
    sign = gen_sign(userinfo, timestamp)
    url = 'https://proxy.guodongbaohe.com/coins/checkin?member_id=' + userinfo['userid'] + '&platform=' + userinfo['platform'] + '&timestamp=' + timestamp + '&signature=' + sign + '&'
    r = requests.get(url=url, headers=headers(userinfo)).json()
    if r['status'] == 0:
        print_ts("签到成功")
    else:
        print_ts(f"签到失败 " + str(r))
        time.sleep(3)


def video(userinfo):
    """
    看广告
    """
    for i in range(6):
        timestamp = str(int(time.time()))
        sign = gen_sign(userinfo, timestamp)
        url = 'https://proxy.guodongbaohe.com/coins/award?member_id=' + userinfo['userid'] + '&platform=' + userinfo['platform'] + '&timestamp=' + timestamp + '&signature=' + sign + '&'
        r = requests.get(url=url, headers=headers(userinfo)).json()
        if r['status'] == 0:
            delay_seconds = random.randint(90, 100)
            print_ts(f"执行第{i + 1}次广告任务完成，获得 {r['result']} 个金币，随机等待{delay_seconds}秒")
            time.sleep(delay_seconds)
        else:
            print_ts(f"看视频失败 " + str(r))
            time.sleep(3)


def gen_sign(userinfo, timestamp):
    data = 'member_id=' + userinfo['userid'] + '&platform=' + userinfo['platform'] + '&timestamp=' + timestamp + '&faf78c39388faeaa49c305804bbc1119'
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


def headers(userinfo):
    return {
        "Host": "proxy.guodongbaohe.com",
        "x-userid": userinfo['userid'],
        "x-appid": "2102202714",
        "x-devid": "No-dev",
        "x-nettype": "WIFI",
        "x-agent": userinfo['agent'],
        "x-platform": userinfo['platform'],
        "x-devtype": "no",
        "x-token": userinfo['token'],
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.14.9"
    }


if __name__ == '__main__':
    with open("gdbh_token.json", "r") as f:
        userinfos = json.load(f)
        print_ts(f"========= 共载入{len(userinfos)}个账号 =========")
        for idx, value in enumerate(userinfos):
            print_ts(f"开始第{idx + 1}个账号")
            checkin(value)
            video(value)
