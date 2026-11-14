# 变式练习 4 · 第 1 题的闭卷重做
#
# 第一遍（练习 1）参考了自己 stats.py 的骨架，还被提示过一次 split(' ') 的边界问题。
# 这一遍不看任何旧代码，从空白文件重写，用来验证是「学会了」还是「抄通了」。
# 大小写区分：a 和 A 算两个不同的首字符

from pathlib import Path


def top_initial(path):
    """统计词首字符里出现次数最多的那一个。

    参数:
        path: 文本文件路径
    返回:
        (首字符, 次数) 元组；次数相同时取后出现的那个
    异常:
        ValueError: 文件里没有任何词
        FileNotFoundError: 文件不存在（由 open() 抛出，本函数不处理）
    """
    with open(path, "r", encoding="utf-8") as f:
        # split() 不加参数：按任意空白切分并丢弃空串。
        # 加了 ' ' 会把行尾换行切出一个空串，然后 word[0] 就是 IndexError。
        words = f.read().split()

        if len(words) == 0:
            raise ValueError("文件里没有任何词")

        dic = {}
        for word in words:
            char = word[0]
            if char not in dic:
                dic[char] = 1
            else:
                dic[char] += 1

        # 用第一个元素当初始值，而不是 0——分数场景下 0 会出错，这里统一成安全写法
        max_char = words[0][0]
        max_count = dic[max_char]

        for j in dic:
            # <= 而不是 <：次数相同时保留后出现的那个
            if max_count <= dic[j]:
                max_count = dic[j]
                max_char = j

        return max_char, max_count


if __name__ == "__main__":
    TEST_FILE = Path(__file__).parent / "words.txt"
    char, count = top_initial(TEST_FILE)
    if char == "a" and count == 3:
        print("[OK] 正常路径：a / 3")
    else:
        print(f"[FAIL] 期望：a / 3，实际：{char} / {count}")

    TEST_FILE = Path(__file__).parent / "empty.txt"
    try:
        top_initial(TEST_FILE)
    except ValueError:
        print("[OK] 空文件抛出 ValueError")
    else:
        print("[FAIL] 空文件本该报错，却正常返回了")

    TEST_FILE = Path(__file__).parent / "nofile.txt"
    try:
        top_initial(TEST_FILE)
    except FileNotFoundError:
        print("[OK] 不存在的文件抛出 FileNotFoundError")
    else:
        print("[FAIL] 不存在的文件本该报错，却正常返回了")