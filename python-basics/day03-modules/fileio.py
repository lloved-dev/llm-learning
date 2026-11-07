"""文件读写工具模块。

对外提供两个"读第 n 行"的函数，行为完全一致，只是实现思路不同：

    read_line      一次把整个文件读进内存，再取第 n 行   —— 适合小文件
    readline_scan  边读边数，数到第 n 行就停            —— 适合大文件 / 只要靠前的行

两个函数遵守同一套约定：
    - 行号 n 从 1 开始（人类习惯），内部再换算成列表下标
    - 成功：返回该行内容，已去掉行尾换行符
    - 失败：n < 1        -> ValueError（参数本身不合法）
            n 超过行数   -> IndexError（位置上没有东西）
            文件不存在   -> FileNotFoundError（open 天然抛出，不额外包装）
"""

from pathlib import Path

# 用 __file__ 定位样本文件，保证"不管你在哪个目录运行"都能找到。
# 如果写成 "test.txt"，Python 会去"当前工作目录"找，换个目录运行就报 FileNotFoundError。
TEST_FILE = Path(__file__).parent / "test.txt"


def read_line(path, n):
    """读取第 n 行（n 从 1 开始），一次读完整个文件。"""
    # 参数校验放在最前面（fail fast）：行号都非法了，没必要先打开文件。
    # 用 ValueError 而不是 IndexError —— 这是"值本身不合法"，不是"位置不存在"。
    if n < 1:
        raise ValueError(f"行号必须从 1 开始，收到 {n}")

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()      # 整个文件 -> list，每项是一行（带结尾换行符）
        # n 是 1 基、列表是 0 基，所以减 1。
        # 越界时 Python 自己就抛 IndexError，这里不用再手动判断。
        # rstrip("\n") 只去掉行尾换行，保留行首空格（用 strip() 会误删有效缩进）。
        return lines[n - 1].rstrip("\n")


def readline_scan(path, n):
    """读取第 n 行（n 从 1 开始），边读边数，读到就停。"""
    if n < 1:
        raise ValueError(f"行号必须从 1 开始，收到 {n}")

    with open(path, 'r', encoding='utf-8') as m:
        for i in range(1, n + 1):
            line = m.readline()
            # readline() 读到文件末尾返回空字符串 ''，而不是报错。
            # 必须在这里拦下来，否则会把 '' 当成"第 n 行的内容"返回出去。
            # 顺序很关键：先判断"读完了没有"，再判断"是不是第 n 行"。
            if line == '':
                raise IndexError(f"文件不足 {n} 行")
            if i == n:
                return line.rstrip("\n")


# 模块自测：只有直接运行 `python fileio.py` 才会执行；
# 被 main.py import 时不会跑（这就是 __name__ 的作用）。
if __name__ == "__main__":
    # 正例：两个函数应该读出同一行
    print(f"read_line      -> {read_line(TEST_FILE, 3)}")
    print(f"readline_scan  -> {readline_scan(TEST_FILE, 3)}")

    # 反例 1：行号超出文件行数 -> 期望 IndexError（只接这一种，抛别的都算失败）
    # 把函数当值放进元组里遍历：以后加第三个读函数，只要加一个名字，测试自动覆盖。
    for fn in (read_line, readline_scan):
        try:
            fn(TEST_FILE, 10)
        except IndexError:
            print(f"{fn.__name__} 超界 -> IndexError ✅")
        else:
            # else 只在"没有抛异常"时执行：说明本该失败却成功了，是 bug
            print(f"{fn.__name__} 超界 -> ❌ 本该报错却成功了")

    # 反例 2：行号非法（0）-> 期望 ValueError
    for fn in (read_line, readline_scan):
        try:
            fn(TEST_FILE, 0)
        except ValueError:
            print(f"{fn.__name__} n=0 -> ValueError ✅")
        else:
            print(f"{fn.__name__} n=0 -> ❌ 本该报错却成功了")