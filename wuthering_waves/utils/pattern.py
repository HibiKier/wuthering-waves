import re

MOBILE_PATTERN = re.compile(r"^1[3-9]\d{9}$")
"""中国大陆手机号码正则表达式"""

CODE_PATTERN = re.compile(r"^\d{6}$")
"""验证码正则表达式"""
