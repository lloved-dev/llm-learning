# 变式练习 1 · 换统计对象
#
# 读文本文件 → 按空白切词 → 统计每个「词的首字符」出现了多少次 → 返回最多的那个
# 首字符不是整个词：apple 记到 a，banana 记到 b
# 大小写区分：a 和 A 算两个不同的首字符
# 空文件 → ValueError；文件不存在 → 交给 open() 抛 FileNotFoundError

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
        # 用不带参数的 split()：按任意空白切分，自动丢掉空串。
        # 若写成 split(' ')，行尾换行会切出一个空串 ''，后面 word[0] 直接 IndexError；
        # 更隐蔽的是 '' .split(' ') 返回 [''] 长度为 1，空文件检查也会失效。
        words = f.read().split()

        if len(words) == 0:
            raise ValueError("文件里没有任何词")

        dic = {}
        for word in words:
            initial = word[0]
            if initial not in dic:
                dic[initial] = 1
            else:
                dic[initial] += 1

        # 初始值取「第一个词的首字符」，不要写 max_count = 0。
        # 这里计数一定大于 0，写 0 也不会错；但同一套找最大值的写法挪到「分数」上就会错，
        # 因为分数可以是负数。统一用「第一个元素」当初始值，两种场景都安全。
        max_char = words[0][0]
        max_count = dic[max_char]

        for ch in dic:
            # 用 <= 而不是 <：次数相同时保留后出现的那个
            if max_count <= dic[ch]:
                max_count = dic[ch]
                max_char = ch

        return max_char, max_count


if __name__ == "__main__":
    # words.txt: apple banana apple / cherry apple banana / date
    # 手工核算：a×3、b×2、c×1、d×1 → 答案是 a / 3
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