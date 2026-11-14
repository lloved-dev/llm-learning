# 变式练习 2 · 不碰文件
#
# 参数是字典 {"姓名": 分数}，返回分数最高的人名和分数
# 空字典 → ValueError（和「空文件」是同一类错误：没有数据可处理）

scores = {"张三": 88, "李四": 95, "王五": 79}
empty = {}


def best_student(scores):
    """从 {"姓名": 分数} 里找出分数最高的那个人。

    参数:
        scores: 姓名为键、分数为值的字典
    返回:
        (姓名, 分数) 元组；分数相同时取后出现的那个
    异常:
        ValueError: 字典为空
    """
    if len(scores) == 0:
        raise ValueError("字典是空的")

    # 先拿第一个元素当初始值。
    # 不要写 max_score = 0：分数可以是负数，0 会把结果直接带偏。
    for name in scores:
        max_name = name
        max_score = scores[name]
        break

    # items() 一次取出键和值。若写成 for k in scores 再 scores[k]，
    # 每个元素都要多查一次字典，而且变量名还得自己记哪个是键。
    for name, score in scores.items():
        # <= ：分数相同时保留后出现的那个
        if max_score <= score:
            max_score = score
            max_name = name

    return max_name, max_score


if __name__ == "__main__":
    name, score = best_student(scores)
    if name == "李四" and score == 95:
        print("[OK] 正常路径：李四 / 95")
    else:
        print(f"[FAIL] 期望：李四 / 95，实际：{name} / {score}")

    try:
        best_student(empty)
    except ValueError:
        print("[OK] 空字典抛出 ValueError")
    else:
        print("[FAIL] 空字典本该报错，却正常返回了")