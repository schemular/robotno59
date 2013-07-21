#-*- coding:utf-8 -*-
#
# Copyright 2013 cold
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# 是否输出调试信息
DEBUG = False

# QQ 号码
QQ = 2021307885

# QQ 密码
QQ_PWD = "password"

# 允许机器人发送消息的最大长度
# 此配置避免结果过长在群内造成刷屏
MAX_LENGTH = 150

# 机器人接收内容超过这个长度将贴到网上
MAX_RECEIVER_LENGTH = 300

# 需要改动QQ某些东西, 比如设置签名, 所要提供的密码
Set_Password = "setpassword"

# 两条消息最小时间间隔, bot 连续发送消息, 如果频率过快会被tx过滤掉
# 设置一个时间间隔来确保消息被正常投递, 安全值是0.5, 其他更小的值未测试
MESSAGE_INTERVAL = 0.5

DATABASE_FOLDER = "data"

UPLOAD_CHECKIMG = False
