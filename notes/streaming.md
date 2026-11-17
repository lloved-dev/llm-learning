# 流式输出与生成器（2026-11-16）

> 一句话：把「等模型全部生成完再显示」改成「生成一点给一点」，靠 `stream=True` +
> 生成器 + `st.write_stream` 三者配合。顺带把 Python 进阶里的**生成器**提前摸了一遍。

代码：`E:\works\chatbot\app.py`（commit `898ad20`，作品集 #1）。

---

## 一、`stream=True` 改的是返回值类型

| | `stream=False`（默认） | `stream=True` |
|---|---|---|
| 返回值 | 一个完整的 `ChatCompletion` 对象 | 一个**流对象**（可迭代，逐个吐 chunk） |
| 文字在哪 | `resp.choices[0].message.content` | `chunk.choices[0].delta.content` |
| 拿到时机 | 等全部生成完 | 生成一点给一点 |

关键差别只有一个词：**`message` 是整体，`delta` 是本次增量**。
打字机效果的根源就在于拿到的是增量，不是全文——不需要自己切字符串。

## 二、边界 chunk：不是每个 chunk 都有文字

一条流的首尾通常有一两个「空壳」chunk（只带结束原因，没有内容）。
Ollama 给 `""`，部分厂商给 `None`，两者都是 falsy：

```python
if not piece:
    continue
```

漏掉这句的后果见过两次：一次画出空白气泡，一次 `len(None)` 直接 `TypeError`。

## 三、`yield` vs `return`（本轮的重点）

```
return  →  等整个 for 循环跑完，才把结果交出去     攒完再给，没有打字机效果
yield   →  每产出一块立刻交出去，函数在这一行暂停   调用方要下一块，才继续跑
```

`return` 之后函数**结束**、现场销毁；`yield` 之后函数**暂停**、局部变量保留。

副产品（官方定义）：**带 `yield` 的函数调用时不会执行函数体，而是立刻返回一个生成器对象。**
所以 `stream_text(resp)` 这一行执行完，`for` 一次都没跑；真正开始跑是
`st.write_stream()` 去迭代它的时候。

结论：**中间层只要是「流 → 流」，就必须写成生成器。** 一旦开始 `+=` 累积，就已经不是流式了。

## 四、`st.write_stream()` 一个当两个用

```python
full = st.write_stream(stream_text(resp))
```

它做两件事：**消费**整条流并边收边渲染；**返回**拼好的完整字符串。
所以不需要自己 `+=`，也不需要单独的累积变量，`full` 直接入库。

顺序陷阱：`full` 只在 `write_stream` **返回之后**才有值，所以 `append` 必须在
`with` 块**外面**——放里面会按 chunk 数 append 几十次。

补充：返回的不一定是 str。若产出的是非字符串对象，返回的是 **list**。

## 五、源码核实：这层中间件其实可以不要

原以为「不写 `stream_text` 就会崩」，读源码后发现是错的。

`streamlit/elements/write.py:219`

```python
for chunk in stream:
    if type_util.is_openai_chunk(chunk):
        chunk = chunk.choices[0].delta.content or ""   # 它自己取 delta
```

`write.py:270`

```python
if isinstance(chunk, str):
    if not chunk:
        continue        # 它自己跳过空串
```

判断依据是正则（`type_util.py:221`）：

```python
_OPENAI_CHUNK_RE = re.compile(r"^openai\..+\.ChatCompletionChunk$")
```

实测本机环境确实命中：

```
type        : openai.types.chat.chat_completion_chunk.ChatCompletionChunk
认作openai块: True
delta内容   : '你'
```

因为我们用 OpenAI SDK 连 Ollama，chunk 就是标准 OpenAI 类型，所以
`st.write_stream(resp)` 直接传**能跑，效果一样**。

### 但中间层仍然保留，理由换成四条

1. 不依赖框架的隐式兜底：换 FastAPI / 命令行 / 纯前端，没人替你取 `delta`
2. 中间层能加自己的逻辑：统计块数、过滤内容、累计 token、处理工具调用的非文本 chunk
3. 显式比隐式好读：三个月后一眼看出这层在「翻译」
4. 这是 Agent 的通用结构：上游吐 A、下游要 B、中间加一层翻译

## 六、容易混的两组词

| 组 | 区别 |
|---|---|
| `message` / `delta` | 整体回答 / 本次新增的一小块 |
| 生成器 generator / 迭代器 iterator | `yield` 造出来的 / 实现 `__next__` 的对象（如 `openai.Stream`） |

`resp` 是 **`openai.Stream`（迭代器）**，不是生成器。两者对外表现一样
（`for` 能遍历、要一块给一块），但名字不能混。

另外 `st.write_stream` **不挑「是不是生成器」**，任何可迭代对象都收
（源码 `write.py:209` 做的是 `iter(stream)`，失败才报 "cannot be iterated"）。

## 七、本轮踩的四个坑

1. `response += i` —— 把 chunk **对象**当字符串加，直接崩
2. 循环里开 `st.chat_message` + `write_stream` —— 每块开一个气泡，屏幕上 40 个气泡
3. `response = ""` 写在循环**里面** —— 每次重置，只剩最后一块
4. 用 `return` 代替 `yield` —— 能跑、不报错，但**没有打字机效果**

第 4 个最该记住：**这类错误不报错，只是悄悄没效果**。所以验收标准必须是肉眼看效果，
不能只看「跑不跑得起来」。

## 八、闭卷自测与判卷

| 题 | 我的答案 | 判 |
|---|---|---|
| 文字在哪个属性？和 `stream=False` 差在哪 | 「在 chunk 上；一个返回整个对象、一个返回流」 | 🟡 方向对，缺 `delta` 这个词 |
| 为什么必须 `yield` | 「要返回一部分渲染一部分，`return` 会等完整之后再返回」 | 🟡 结论对，缺「暂停 + 生成器」机制 |
| `write_stream` 返回什么 | 「一段完整内容，因为它已经包含了 `+=` 的功能」 | ✅ |
| 变式：能不能省掉中间层直接传 `resp` | 「不能，会报错，resp 是生成器对象」 | ❌ 结论错（能跑）；术语也错（迭代器不是生成器） |

三题答对了逻辑，两处精度不足：`delta` 这个词、`yield` 的暂停机制。

## 九、本轮最值钱的教训

> 你以为的「必须」，很可能是框架在背后偷偷兜底。

断言前先做一件事：**读一次源码，或跑一次最小实验**。
这次花了两分钟就推翻了一个很多人会顺口说出的答案。

## 相关

- 生成器 / 迭代器 / 装饰器 —— 第 2 列 Python 编程进阶的正式内容，本轮只是提前碰到
- 项目侧遗留：PyCharm 解释器仍指向 anaconda（红线是假的），待切到 `.venv`