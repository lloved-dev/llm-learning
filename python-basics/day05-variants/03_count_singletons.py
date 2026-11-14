# 变式练习 3 · 换输出形态
#
# 读文本文件 → 切词 → 计数 → 返回「只出现过一次的词」有几个
# 注意返回的是个数（int），不是词的列表
# 空文件 → ValueError；文件不存在 → 交给 open() 抛 FileNotFoundError

from pathlib import Path


def count_singletons(path):
    """数一数只出现过一次的词有多少个。

    参数:
        path: 文本文件路径
    返回:
        只出现一次的词的数量（int）
    异常:
        ValueError: 文件里没有任何词
        FileNotFoundError: 文件不存在（由 open() 抛出，本函数不处理）
    """
    with open(path, "r", encoding="utf-8") as f:
        # 不带参数的 split()：按任意空白切，自动丢掉空串
        words = f.read().split()

        if len(words) == 0:
            raise ValueError("文件里没有任何词")

        dic = {}
        for word in words:
            if word not in dic:
                dic[word] = 1
            else:
                dic[word] += 1

        # 第二步：遍历计数字典，只数「值为 1」的键有多少个。
        # 这里最容易读错题意——返回的是个数，不是列表；
        # 想要列表得写成 [w for w in dic if dic[w] == 1]，那是另一道题。
        count = 0
        for word in dic:
            if dic[word] == 1:
                count += 1

        return count


if __name__ == "__main__":
    # words.txt: apple×3、banana×2、cherry×1、date×1 → 答案是 2
    TEST_FILE = Path(__file__).parent / "words.txt"
    num = count_singletons(TEST_FILE)
    if num == 2:
        print("[OK] 正常路径：2")
    else:
        print(f"[FAIL] 期望：2，实际：{num}")

    TEST_FILE = Path(__file__).parent / "empty.txt"
    try:
        count_singletons(TEST_FILE)
    except ValueError:
        print("[OK] 空文件抛出 ValueError")
    else:
        print("[FAIL] 空文件本该报错，却正常返回了")

    TEST_FILE = Path(__file__).parent / "nofile.txt"
    try:
        count_singletons(TEST_FILE)
    except FileNotFoundError:
        print("[OK] 不存在的文件抛出 FileNotFoundError")
    else:
        print("[FAIL] 不存在的文件本该报错，却正常返回了")