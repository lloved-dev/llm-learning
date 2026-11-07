"""演示如何调用 fileio 模块。

运行：python main.py —— 在哪个目录运行都可以（路径由 __file__ 算出，不依赖当前目录）。
"""

import fileio
from pathlib import Path

# 路径由调用方（这里）决定，再传给模块 —— 这就是两层的分工：
# fileio 只负责"从某个路径读出第 n 行"，不关心文件在哪、也不知道要打印成什么样。
TEST_FILE = Path(__file__).parent / "test.txt"

# 方式一：一次读完整个文件（小文件更简单）
try:
    result = fileio.read_line(TEST_FILE, 3)
    print(result)
except Exception as e:
    # 出什么错都兜住，只给用户一句人话；e 里保留了技术细节，方便自己排查。
    # 想更严谨可以分别 catch IndexError / ValueError / FileNotFoundError。
    print(f"读取失败：{e}")

# 方式二：边读边数（大文件、或要的行靠前时更省内存和时间）
try:
    end = fileio.readline_scan(TEST_FILE, 3)
    print(end)
except Exception as w:
    print(f"readline_scan函数读取失败:{w}")