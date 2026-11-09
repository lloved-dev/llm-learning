"""统计文本中出现次数最多的单词。

本文件的约定：
  - “单词”按空白字符切分（空格、换行、制表符），连续空白视为一个分隔符
  - 中文未做分词，所以 “系列的第一个模型” 会被当作一个词
  - 出现次数并列时，返回最后遍历到的那一个（见下方 <= 的说明）
"""
from pathlib import Path


def top_word(path):
    """返回 (出现次数最多的词, 次数)。

    参数:
        path: 文本文件路径
    返回:
        (词, 次数) 元组
    异常:
        ValueError: 文件内容为空（没有可统计的词）
        FileNotFoundError: 文件不存在（由 open 抛出，本函数不捕获）
    """
    with (open(path, 'r', encoding='utf-8') as k):
        content = k.read()

        # 不传参数 = 按任意空白切分，连续的空格/换行会合并成一个分隔符
        content = content.split()

        # fail fast：空文件根本没有词，这里报错比后面 content[0] 抛 IndexError 更清楚
        if len(content) == 0:
            raise ValueError("文件是空的")

        # 计数：第一次见到记为 1（此刻它已经出现了一次），之后每见一次 +1
        dit = {}
        for i in range(0, len(content)):
            if content[i] not in dit:
                dit[content[i]] = 1
            else:
                dit[content[i]] += 1

        # 拿第一个词作基准：次数和“是谁”要同时记住，
        # 只记次数的话，最后只知道最高分、不知道是谁拿的
        max_count = dit[content[0]]
        max_name = content[0]

        # 用 <= 表示并列时后出现的胜出；想保留先出现的，把 <= 改成 <
        for x in dit:
            if max_count <= dit[x]:
                max_count = dit[x]
                max_name = x        # 换分数时必须同时换人，两者永远同步

        return max_name, max_count


if __name__ == "__main__":
    # 只有直接运行时才执行自测；被别的文件 import 时不会跑
    # 路径全部用 __file__ 推导，所以从任何目录启动，结果都一样

    # 测试 1：正常路径。断言具体结果，而不是“没崩就算过”
    TEST_FILE = Path(__file__).parent / "test.txt"
    name1, num1 = top_word(TEST_FILE)
    if name1 == "K3.1" and num1 == 3:
        print("[OK] 正常路径：K3.1 / 3")
    else:
        print(f"[FAIL] 期望 词=K3.1 次数=3，实际 词={name1} 次数={num1}")

    # 测试 2：空文件必须抛 ValueError
    # 三个测试各自一个 try，绝不共用一个 —— 共用时后面的失败会被前面掩盖
    TEST_FILE = Path(__file__).parent / "empty.txt"
    try:
        name2, num2 = top_word(TEST_FILE)
    except ValueError as V:
        print("[OK] 空文件抛出 ValueError")
    else:
        print("[FAIL] 空文件本该报错，却正常返回了")

    # 测试 3：文件不存在必须抛 FileNotFoundError
    TEST_FILE = Path(__file__).parent / "nofile.txt"
    try:
        name3, num3 = top_word(TEST_FILE)
    except FileNotFoundError as f:
        print("[OK] 不存在的文件抛出 FileNotFoundError")
    else:
        print("[FAIL] 不存在的文件本该报错，却正常返回了")