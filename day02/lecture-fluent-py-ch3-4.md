# 《Fluent Python》第 2 版 · 第 3-4 章 学习讲义

> 适配 Day 2 Block 1（2 小时）
> 配套代码：`day02/scratch_fluent_py_ch3_4.py`
> 学习节奏：**读 1 节讲义 → 回代码改对应 experiment → 跑通 → 进入下一节**

---

## 学习目标（学完你应该能回答）

读完本讲义+完成 10 个实验，你应该能**不查文档**回答：

1. `dict.setdefault` 和 `defaultdict` 哪个更好？什么时候用哪个？
2. 为什么 `list` 不能当 dict 的 key，但 `tuple` 可以？
3. `Counter` 跟普通 dict 有什么区别？什么场景必用 Counter？
4. 集合（set）的并/交/差/对称差怎么用？什么场景比循环+if 优雅 100 倍？
5. `str` 和 `bytes` 的本质区别是什么？为什么这是 FDE 的高频考点？
6. UTF-8、GBK、Latin-1 的区别？客户给我一份"乱码 CSV"我怎么办？
7. `'café' == 'café'` 可能为 `False`，怎么解？

如果其中任何一个你看完讲义还答不上来，**回来问我，不要假装懂了**。

---

## 第 3 章 · 字典与集合（Dictionaries and Sets）

### 3.1 为什么这一章重要（90 秒先讲清楚）

Python 的官方字节码里有一句俗话：**"Python 的内部就是字典写的"**。这不夸张：

- 类的属性 = `__dict__` 字典
- 模块的命名空间 = 一个字典
- 函数的关键字参数 = 一个字典
- JSON、配置文件、API 响应、数据库行 → 全是字典

**FDE 工作中 70% 的代码本质都在操作字典**：把客户给的 JSON 拆开、把数据库结果重新组织、把 LLM 输出解析成结构。**字典玩不溜的人，FDE 路上每天卡壳。**

集合（set）是字典的"半身"——只有 key 没有 value。这一章把它俩放一起讲，是因为它们底层都是哈希表。

---

### 3.2 字典推导式（dict comprehension）

#### 概念

跟列表推导式 `[x for x in ...]` 一个道理，只是返回 dict：

```python
{key_expr: value_expr for item in iterable}
```

#### 经典场景：从两个并行列表造字典

```python
tickers = ["NVDA", "AAPL", "MSFT"]
prices = [880.0, 195.0, 415.0]

# 一行搞定
quotes = {t: p for t, p in zip(tickers, prices)}
# {'NVDA': 880.0, 'AAPL': 195.0, 'MSFT': 415.0}
```

#### 进阶：带过滤

```python
# 只要价格 > 200 的
expensive = {t: p for t, p in zip(tickers, prices) if p > 200}
# {'NVDA': 880.0, 'MSFT': 415.0}
```

#### 进阶：颠倒键值

```python
inv = {v: k for k, v in quotes.items()}
# {880.0: 'NVDA', 195.0: 'AAPL', 415.0: 'MSFT'}
```

#### FDE 实战意义

客户给你一份 JSON 数组，每个元素长这样：
```python
[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
```

要把它转成 `{1: "Alice", 2: "Bob"}` 这种"按 id 索引"的字典——**dict comprehension 一行搞定**：

```python
users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
by_id = {u["id"]: u["name"] for u in users}
```

这是你将来每天写 5 次的 idiom。

→ 现在去看 `scratch_fluent_py_ch3_4.py` 的 **experiment_1**，把它跑一遍。

---

### 3.3 `setdefault` vs `defaultdict`（FDE 高频）

#### 问题场景

把一堆词按首字母分桶：

```python
words = ["apple", "ant", "banana", "blueberry"]
# 想得到 {'a': ['apple', 'ant'], 'b': ['banana', 'blueberry']}
```

#### 笨办法（新手代码）

```python
groups = {}
for w in words:
    key = w[0]
    if key not in groups:
        groups[key] = []
    groups[key].append(w)
```

写得没错，但**啰嗦**。Python 给了两种 idiomatic 的写法。

#### Idiom A：`dict.setdefault`（标准 dict 上就能用）

```python
groups = {}
for w in words:
    groups.setdefault(w[0], []).append(w)
```

`setdefault(key, default)` 的语义：
- 如果 `key` 已经在字典里 → 返回它的值
- 如果不在 → 把 `default` 写进去，并返回它

注意 `setdefault` 返回的就是那个 list 对象（无论是新建的还是已有的），所以可以直接 `.append` 上去。

#### Idiom B：`defaultdict`

```python
from collections import defaultdict

groups = defaultdict(list)   # 工厂函数：访问不存在的 key 时自动 list()
for w in words:
    groups[w[0]].append(w)
```

#### 关键区别（这是面试题）

| 特性 | `setdefault` | `defaultdict` |
|---|---|---|
| 用在普通 dict 上 | ✅ | ❌ 必须是 `defaultdict` |
| 访问不存在的 key | 不会创建 | **会创建并返回默认值** |
| 序列化 / 跟外部 dict 互操作 | 没问题 | 有时会被当作普通 dict 处理，default 行为丢失 |

**defaultdict 的"陷阱"**：

```python
d = defaultdict(list)
print(d["nonexistent"])   # 输出 []，但同时它把 "nonexistent" 加进了字典！
print(dict(d))            # {'nonexistent': []}
```

→ 这就是为什么读字典的"探查代码"在 defaultdict 上要用 `if key in d` 而不是 `d.get(key)` 或 `d[key]`。

#### 我的推荐

- **写新代码：用 `defaultdict`**——更简洁
- **改别人的代码、不能改 dict 类型：用 `setdefault`**
- **读取一个可能存在可能不存在的 key：用 `dict.get(key, default)`**——这是第三种 idiom，**它不修改字典**

→ 现在去看 `scratch_fluent_py_ch3_4.py` 的 **experiment_2**，把它跑一遍，**特别注意 `defaultdict` 访问 'z' 之后字典内容变化的现象**。

---

### 3.4 哈希性（Hashability）—— 什么能当 key

#### 规则

**只有 hashable 的对象能当 dict 的 key**（也能放进 set）。

判断 hashable 的简单口诀：
- **不可变**（immutable） → 通常 hashable
  - `int`、`float`、`str`、`bool`、`tuple`（前提：tuple 内部全部 hashable）、`frozenset` → ✅
- **可变**（mutable） → 不 hashable
  - `list`、`dict`、`set` → ❌

#### 为什么？

字典的实现是哈希表：把 key 通过 `hash(key)` 算出一个数字，决定它放在内存哪个槽。如果 key 是 list，你 append 一个元素后它的 hash 变了，原来放的位置就**找不到自己**了——字典就坏了。

所以 Python 直接禁止：

```python
>>> {[1, 2]: "v"}
TypeError: unhashable type: 'list'
```

#### 实战 idiom

| 想要的 key | 用什么 |
|---|---|
| 多字段复合 key | tuple，如 `(ticker, "2026-Q1")` |
| 一组无序唯一标签 | frozenset，如 `frozenset(["AI", "SaaS"])` |
| 任意对象作为 key | 实现 `__hash__` 和 `__eq__` 的自定义类 |

#### FDE 实战

API 返回了一堆数据，你想用"账户 ID + 月份"做联合 key 缓存：

```python
cache: dict[tuple[int, str], dict] = {}
cache[(123, "2026-01")] = {"revenue": 1000}
cache[(123, "2026-02")] = {"revenue": 1100}
```

这就是为什么 tuple 能 hash 是个**重要的设计**——不是"恰好可以"，是"专门设计来支撑这个 idiom 的"。

→ **experiment_3**

---

### 3.5 `Counter` —— 为统计而生的字典

#### 它解决什么问题

"数一数每个东西出现了几次"。

#### 笨办法

```python
counts = {}
for x in items:
    counts[x] = counts.get(x, 0) + 1
```

#### Idiomatic

```python
from collections import Counter
counts = Counter(items)
```

#### 它有几个独门绝技

```python
counts.most_common(3)   # 出现次数 top 3 → [('INFO', 50), ('ERROR', 10), ('WARN', 3)]
counts.update(more_items)   # 累加，不是覆盖
counts1 + counts2       # 两个 Counter 相加
counts1 - counts2       # 相减（保留正值）
counts1 & counts2       # 逐 key 取最小值（"交集"语义）
counts1 | counts2       # 逐 key 取最大值（"并集"语义）
```

#### FDE 实战 1：日志统计

```python
levels = [line.split()[0] for line in log_lines]
counts = Counter(levels)
print(counts.most_common(3))
```

#### FDE 实战 2：anagram 判定

LeetCode 242 的 Pythonic 解法（你今天就要做这道题）：

```python
def is_anagram(s, t):
    return Counter(s) == Counter(t)
```

#### FDE 实战 3：分析客户提供的 CSV

```python
import csv
from collections import Counter

with open("customer_orders.csv") as f:
    reader = csv.DictReader(f)
    cities = Counter(row["city"] for row in reader)

print("Top 5 cities by order count:", cities.most_common(5))
```

→ **experiment_4**

---

### 3.6 集合（set）—— 哈希表的"另一半"

#### 集合是什么

Python 的 `set` 是一个**无序、不重复**的容器，底层和 dict 一样是哈希表，所以 `in` 操作平均 O(1)。

```python
yesterday_holdings = {"NVDA", "AAPL", "MSFT", "GOOGL"}
today_holdings = {"NVDA", "AAPL", "TSLA", "MSFT"}
```

#### 集合代数（这是为什么 set 很值钱）

| 操作 | 符号 | 方法 | 含义 |
|---|---|---|---|
| 并集 | `\|` | `.union()` | 在任一集合里 |
| 交集 | `&` | `.intersection()` | 同时在两集合里 |
| 差集 | `-` | `.difference()` | 在 A 但不在 B |
| 对称差 | `^` | `.symmetric_difference()` | 在恰好一个里 |

#### 经典 FDE 场景：两个时间点的"差异分析"

```python
dropped = yesterday - today    # 卖出的：{'GOOGL'}
added   = today - yesterday    # 买入的：{'TSLA'}
kept    = yesterday & today    # 持有的：{'NVDA', 'AAPL', 'MSFT'}
```

3 行代码做完一份"持仓变化报告"。如果用 list + 嵌套 for 循环，得 30 行。

#### 笨办法 vs idiomatic 对照

```python
# ❌ 新手写法
dropped = []
for item in yesterday:
    if item not in today:
        dropped.append(item)

# ✅ 老手写法
dropped = yesterday - today
```

#### 注意：`set` 是可变的，`frozenset` 才是不可变的

```python
{1, 2, 3}            # set，可变，不能当 dict key
frozenset({1, 2, 3}) # frozenset，不可变，能当 dict key
```

→ **experiment_5**

---

## 第 4 章 · 文本与字节（Unicode Text vs Bytes）

### 4.1 为什么这一章重要

> "我对接了客户的 CSV，跑出来全是乱码。"
>
> "我的 API 测试通过了，但生产上一遇到中文用户名就 500 错误。"

这两句话你**未来一定会从客户嘴里听到**。FDE 不能在编码问题上掉链子。

这一章的核心是建立一个**清晰的心智模型**：

> **`str` 是文本（人类读的），`bytes` 是字节（机器读的）。它们之间通过编码（encoding）互转。**

---

### 4.2 `str` vs `bytes` 的本质

#### `str` 是 Unicode 字符串

```python
s = "财报"
len(s)       # 2 —— 两个 Unicode 字符
type(s)      # <class 'str'>
```

`s` 在内存里是一个 Unicode codepoint 序列。**它不是字节，它是字符**。

#### `bytes` 是字节序列

```python
b = s.encode("utf-8")
b            # b'\xe8\xb4\xa2\xe6\x8a\xa5'
len(b)       # 6 —— 两个汉字在 UTF-8 下各占 3 字节
type(b)      # <class 'bytes'>
```

`b` 是真正能写到磁盘、发到网络上的东西。

#### 转换

| 方向 | 方法 |
|---|---|
| `str` → `bytes` | `.encode("utf-8")` |
| `bytes` → `str` | `.decode("utf-8")` |

#### 关键认知

**Python 3 强制区分这两者**——你不能拿一个 `str` 直接写到 socket 里，必须先 encode。这是 Python 3 比 Python 2 大幅进步的一点（Python 2 把 str 和 bytes 混着用，bug 满天飞）。

→ **experiment_6**

---

### 4.3 编码失败：什么时候出问题

#### 编码（encode）失败：`str` → `bytes`

```python
"财报".encode("latin-1")
# UnicodeEncodeError: 'latin-1' codec can't encode characters
# in position 0-1: ordinal not in range(256)
```

为什么？Latin-1 只能表达 0-255 的字符（基本就是西欧字母）。汉字根本不在它的"字符表"里。

#### 三种错误处理策略

```python
"财报".encode("latin-1", errors="strict")    # 默认，抛异常
"财报".encode("latin-1", errors="replace")   # b'??'  替换为问号
"财报".encode("latin-1", errors="ignore")    # b''    直接吞掉
```

**FDE 何时用哪个？**
- `strict`：默认，让程序崩溃比让数据悄悄损坏好（**生产代码默认这个**）
- `replace`：客户日志清洗、warn 用户但不阻塞
- `ignore`：**几乎从来不应该用**，会让你查不到 bug

#### 解码（decode）失败：`bytes` → `str`

```python
# 客户上传了一份 GBK 编码的 CSV，你按 UTF-8 读
raw = "公司,营收\n苹果,1000".encode("gbk")
raw.decode("utf-8")
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb9
```

**这是 FDE 工作中最常遇到的"乱码"问题**。中国客户给的 Excel/CSV 经常是 GBK/GB18030 编码（特别是从老版 Windows 导出的）。

#### 解决套路

1. 先用 `chardet` 库猜编码：
   ```python
   import chardet
   with open("file.csv", "rb") as f:
       raw = f.read()
   guess = chardet.detect(raw)
   print(guess)   # {'encoding': 'GB2312', 'confidence': 0.99}
   ```
2. 用猜的编码 decode：
   ```python
   text = raw.decode(guess["encoding"])
   ```

→ **experiment_7** 和 **experiment_8**

---

### 4.4 Unicode 标准化（normalization）—— 隐藏的相等性陷阱

#### 神奇的 bug

```python
a = "café"            # 你输入的
b = "cafe\u0301"      # 系统从某个地方拿到的

a == b               # False ！
```

两个字符串**看起来一样**，但 Python 说它们不相等。原因：

- `a` 用了**预组合字符** `é`（一个 Unicode 码位 U+00E9）
- `b` 用了**组合字符** `e + ́`（两个码位：e 加上后置的 acute accent）

#### 解决：归一化

```python
import unicodedata
unicodedata.normalize("NFC", a) == unicodedata.normalize("NFC", b)   # True
```

四种归一化形式：
- `NFC`（**最常用**）：尽可能合并成预组合字符
- `NFD`：拆开成基础字符 + 修饰符
- `NFKC`、`NFKD`：兼容模式（会把全角"Ａ"和半角"A"视为相同）

#### FDE 实战

用户搜索"café 餐厅"，数据库里存的是"cafe + 组合acute餐厅"——直接比对永远找不到。

**惯例**：所有进入数据库的字符串先 NFC 归一化，所有比较前也 NFC 归一化。

→ **experiment_9**

---

## 4.5 海象运算符（PEP 572，Python 3.8+）—— 顺手送你一个

### 它是什么

```python
:=        # "海象"——眼睛是冒号，牙齿是等号
```

它能**在表达式中赋值**。

#### 老写法

```python
data = read_api()
if data:
    process(data)
```

#### 海象写法

```python
if data := read_api():
    process(data)
```

少一行，且语义更紧凑。

#### 在 dict / list 推导里更香

```python
# 老写法：要么算两次，要么先存起来
[expensive_calc(x) for x in items if expensive_calc(x) > 10]   # ❌ 算两次

# 海象：算一次
[y for x in items if (y := expensive_calc(x)) > 10]
```

→ **experiment_10**

---

## 收工自检（必做）

读完讲义+跑通 10 个实验后，关掉 Cursor，**用嘴回答**（或写在反思日志里）：

1. dict comprehension 一行能做什么、不能做什么？
2. 我什么时候用 setdefault，什么时候用 defaultdict，什么时候用 dict.get？
3. 为什么 list 不能当 key？给我一个有意义的复合 key 的实例。
4. Counter 的 `most_common` 怎么用？我现实生活中下次会用它做什么？
5. 集合的 4 种代数操作分别叫什么？我能想到一个 FDE 工作场景每个都用一次吗？
6. str 和 bytes 的关系？从字节到字符串叫什么操作？
7. 客户给我一份"打开是乱码"的 CSV，我的 3 步排查流程是什么？
8. `'café' == 'café'` 为什么可能 False？我怎么修？

**每一题都答得出来 → 这 2 小时的 ROI 拉满。答不出 → 回来找我，咱们重学这一节。**

---

## 给"提速器"

如果你节奏快，2h 内全部跑完了还想多榨一点价值，**bonus**：

- 把 experiment_4（Counter 那个）的 `log_lines` 换成你最近真实的一份日志（任何文本文件）
- 把 experiment_5（set 代数）的两个 set 换成你昨天和今天的浏览器打开标签页的网站列表
- 把 experiment_8（GBK 解码）保存一份**双语文件**（中英混合），故意用错误编码打开，记录现象

把这些 bonus 实验补充到脚本里，commit 进去——你的 commit history 就更"有血有肉"。

---

## 下一步

完成 Block 1 后告诉我："Block 1 完成，进入 Block 2"，我会**激活 Block 2 LeetCode** 的引导节奏：
- 一道一道题来
- 每题先讲思路，你写代码，写完跑通再看下一题
- 1 小时刚好 5 道（每题平均 12 分钟）

如果哪个 experiment 卡住了，**直接把报错或疑问贴给我**——这是你最该用我的时刻。

加油。
