"""
Task02 习题 3：在 2.2 节迷你版 ELIZA 基础上做两处扩展
  1) 新增 5 条规则：工作 / 学习 / 爱好 / 疲惫 / "你记得我什么"
  2) 加入上下文记忆：从对话中抽取姓名、年龄、职业，并在后续回应里引用

运行方式：
  python eliza_extended.py          # 交互对话
  python eliza_extended.py --demo   # 跑一遍预设脚本，方便截图
"""

import re
import random
import sys

# ---------------------------------------------------------------- 记忆区
# 全书唯一的有状态（stateful）的地方：字典 memory 在多轮之间保留
memory = {}


# ---------------------------------------------------------------- 记忆抽取
# 顺序很重要：越具体的模式放越前面
JOB_WORDS = {
    "engineer", "teacher", "student", "designer", "manager", "doctor",
    "nurse", "programmer", "developer", "researcher", "accountant",
    "lawyer", "sales", "writer", "analyst",
}


def extract_memory(text):
    """从一句话里抽取姓名 / 年龄 / 职业，返回被记下的字段名或 None"""
    # 姓名：my name is X / call me X
    m = re.search(r"\b(?:my name is|call me)\s+([A-Za-z]{2,20})", text, re.I)
    if m:
        memory["name"] = m.group(1).capitalize()
        return "name"

    # 年龄：I am 24 / I'm 24 years old
    m = re.search(r"\bi(?:'m| am)\s+(\d{1,3})(?:\s+years?\s+old)?\b", text, re.I)
    if m:
        memory["age"] = m.group(1)
        return "age"

    # 职业：I work as a X / I am a X（X 必须命中职业词表，避免把 "I am tired" 当成职业）
    m = re.search(r"\bi(?:'m| am| work as)\s+(?:an?\s+)?([a-z ]{2,30})", text, re.I)
    if m:
        phrase = m.group(1).strip(" .,!")
        if any(w in JOB_WORDS for w in phrase.split()):
            memory["job"] = phrase
            return "job"

    return None


def render(t
