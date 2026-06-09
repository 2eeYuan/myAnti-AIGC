# myAnti-AIGC

[English](README_EN.md) | 中文

降低中文学术论文 AIGC 检测率的 Claude Code Skill。

基于三个热门开源项目（[aigc-reduce](https://github.com/ydyjya/aigc-reduce)、[humanizer-zh-academic](https://github.com/CJayWong/humanizer-zh-academic)、[thesis-creator](https://github.com/GrammarSense/thesis-creator)）的核心方法论合并而成，针对中文学术写作场景做了整合与优化。

## 适用场景

| 场景 | 适配度 |
|------|--------|
| 期刊论文 | 适配 |
| 毕业论文（本科/硕士/博士） | 适配 |
| 研究报告 | 适配 |
| 学术博客/评论 | 适配 |

**触发词**：降AIGC率、去AI味、人工润色、humanize、论文降重、AI痕迹消除、降低论文AI率

## 安装

### 前置条件

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 已安装
- Python 3.10+（扫描脚本需要）

### 安装步骤

**方式一：克隆到项目目录**

```bash
cd your-project-directory
git clone https://github.com/2eeYuan/myAnti-AIGC.git
```

**方式二：克隆到 Claude Code 全局 skill 目录**

```bash
cd ~/.claude/skills
git clone https://github.com/2eeYuan/myAnti-AIGC.git
```

**方式三：手动下载**

下载 ZIP 解压后，确保目录结构如下：

```
your-project/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── myAnti-AIGC/
        ├── SKILL.md
        ├── references/
        │   ├── ai-patterns.md
        │   ├── replacement-tables.md
        │   └── detection-principles.md
        └── scripts/
            └── aigc_scan.py
```

## 使用方法

### 1. 自然语言触发

在 Claude Code 中直接描述需求即可：

```
> 帮我降低这段论文的AI率
> 这段文字AIGC检测率太高了，帮我润色一下
> 去AI味，这是我的论文第三章
```

Claude Code 会自动加载 skill 并执行三步流程：
1. **风险识别报告** — 扫描并列出高风险段落和命中模式
2. **改写** — 用户确认后输出改写版本
3. **改写后验证** — 自动再扫描一遍，输出前后对比报告，直到风险降至低水平

### 2. 手动运行扫描脚本

```bash
# 基本用法
python skills/myAnti-AIGC/scripts/aigc_scan.py your_paper.txt

# JSON 输出（便于程序处理）
python skills/myAnti-AIGC/scripts/aigc_scan.py your_paper.txt --json

# 自定义风险阈值（默认 50）
python skills/myAnti-AIGC/scripts/aigc_scan.py your_paper.txt --threshold 60

# 改写前后对比（核心功能）
python skills/myAnti-AIGC/scripts/aigc_scan.py --compare 原文.txt 改写后.txt
```

扫描输出示例：

```
============================================================
  AIGC 特征扫描报告
============================================================
  文件: paper.txt
  段落数: 12  |  句子数: 68  |  字数: 3200
============================================================

  [MED] 综合风险评分: 48.5/100 (medium)

  维度                 得分  详情
  --------------------------------------------------
  模板句式密度     ██████░░░░  62.5  8/68句
  句长均匀度       ████░░░░░░  40.0  CV=0.312
  嵌套编号         ██░░░░░░░░  20.0
  冒号并列         ░░░░░░░░░░   0.0
  被动语态         ███░░░░░░░  30.0
  段落对称性       █████░░░░░  50.0
  模糊表述         ████░░░░░░  40.0  2处
  AI高频词         ██████░░░░  60.0  6.2/千字

  [!] 高风险段落 (3 个):
  [H] 第1段: 模板词2处, AI高频词3处
  [M] 第3段: 句长过于均匀(CV=0.22)
  [H] 第7段: 模板词3处, 段末总结「综上所述」

  建议: 需要局部修改。重点处理高风险段落。
```

### 3. 改写前后对比

改写完成后，用 `--compare` 模式验证效果：

```bash
python skills/myAnti-AIGC/scripts/aigc_scan.py --compare 原文.txt 改写后.txt
```

对比报告示例：

```
================================================================
  AIGC 改写前后对比报告
================================================================

  改写前: before.txt
    段落: 3  句子: 9  字数: 198
  改写后: after.txt
    段落: 4  句子: 13  字数: 264
  字数变化: +66 (+33.3%)

  ================================================================
  综合风险评分
  ================================================================
  改写前: 56.3/100 (medium)
  改写后: 19.5/100 (low)
  变化:   -36.8 [v]
  >>> 明显改善

  ================================================================
  各维度对比
  ================================================================
  维度                改写前  改写后  变化  趋势
  ------------------------------------------------------------
  模板句式密度         66.7    0.0  -66.7 v
  句长均匀度           60.0   60.0    0.0 =
  段落对称性           80.0   50.0  -30.0 v
  模糊表述             40.0    0.0  -40.0 v
  AI高频词           100.0    0.0 -100.0 v

  结论: 改写效果良好，风险等级降至低风险。
```

## Skill 核心方法论

### 四条铁律

1. **禁止 AI 全量重写** — 用 AI 重写 AI 文本会叠加 AI 指纹，必须通过确定性字符串替换完成
2. **修改率必须 >40%** — 深度修改（>40%）可使检测规避率达 60-80%
3. **确定性替换** — 每次操作只改一小处，保留原文大部分 token 不变
4. **保持学术语体** — 降重不是口语化，学术语体底线不可突破

### 三轮降重协议

| 轮次 | 目标 | 手段 |
|------|------|------|
| 第一轮 | 去除 AI 痕迹（减法） | 词级替换 → 句级重构 → 段落调整 |
| 第二轮 | 注入人类特征（加法） | 节奏工程、不确定性注入、操作细节 |
| 第三轮 | Anti-AI 审计（自检） | 逐项排查剩余 AI 痕迹 |

### 21 种 AI 痕迹识别模式

覆盖内容层面（理论起笔、段末套路、三元并列、被动分析套话等）和统计层面（重要性膨胀、同义词轮换、空洞结论、破折号滥用等）的 AI 写作特征。

详见 [`references/ai-patterns.md`](skills/myAnti-AIGC/references/ai-patterns.md)。

### 强制硬约束

| 约束项 | 硬上限 | 说明 |
|--------|--------|------|
| AI 高频词 | 每段 ≤2 个 | 超出必须替换 |
| 段末总结套句 | 全文 ≤1 处 | 超出必须删除或改写 |
| 整齐三元并列 | 每段 ≤1 处 | 超出必须打破对称 |
| 「依据/基于XX理论」开头段落 | ≤20% 段落数 | 超出必须移位 |
| 正文加粗 | 全文 ≤5 处 | 超出必须削减 |
| 泛化结尾 | 全文 0 处 | 命中即修复 |
| 模糊归因 | 全文 0 处 | 命中即删除或具体化 |

## 目录结构

```
myAnti-AIGC/
├── .claude-plugin/
│   └── plugin.json              ← Skill 注册入口
├── skills/
│   └── myAnti-AIGC/
│       ├── SKILL.md             ← 核心指令（Claude 读了才知道怎么干活）
│       ├── references/
│       │   ├── ai-patterns.md        ← 21 种 AI 痕迹模式库
│       │   ├── replacement-tables.md ← 词级/句级/段落级替换表 + AI 高频词清单
│       │   └── detection-principles.md ← 检测器技术原理（知网 3.0 / 万方 / GPTZero）
│       └── scripts/
│           └── aigc_scan.py     ← 8 维度自动扫描脚本
├── .gitignore
└── README.md
```

### 各文件职责

| 文件 | 职责 | 何时被加载 |
|------|------|-----------|
| `plugin.json` | 告诉 Claude Code 这里有一个 skill | 系统启动时 |
| `SKILL.md` | 完整的工作手册：角色、规则、流程、策略 | 用户触发 skill 时 |
| `ai-patterns.md` | AI 写作特征的识别与改写指南 | 审计阶段按需读取 |
| `replacement-tables.md` | 替换操作的详细规则和词表 | 第一轮替换时按需读取 |
| `detection-principles.md` | 知网/万方/GPTZero 等检测器的技术原理 | 了解检测逻辑时按需读取 |
| `aigc_scan.py` | 自动化扫描工具，支持单文件扫描和改写前后对比 | SKILL.md 指令触发时执行 |

## 扫描维度说明

`aigc_scan.py` 从 8 个维度检测 AI 痕迹，综合加权计算风险评分（0-100）：

| 维度 | 权重 | 检测内容 |
|------|------|----------|
| 模板句式密度 | 20% | 「综上所述」「基于…分析」等模板词出现频率 |
| 句长均匀度（突发性） | 20% | 句子长度的变异系数，AI 文本 CV < 0.3 |
| 嵌套编号 | 5% | 连续 (1)(2)(3) 编号模式 |
| 冒号并列 | 5% | 「：A；B；C」的三元并列结构 |
| 被动语态 | 10% | 「被测定为」「由…进行」等被动标记 |
| 段落对称性 | 15% | 连续段落长度是否过于一致 |
| 模糊表述 | 10% | 「有研究表明」「专家认为」等无出处归因 |
| AI 高频词 | 15% | 「至关重要」「不可忽视」「具有重要意义」等 |

**风险等级**：综合评分 ≥70 为高风险，40-69 为中风险，<40 为低风险。

## 参考项目

本 skill 的方法论来源于以下开源项目：

- **[aigc-reduce](https://github.com/ydyjya/aigc-reduce)**（282 stars）— 确定性替换方案、三轮降重协议、aigc_scan.py 扫描工具
- **[humanizer-zh-academic](https://github.com/CJayWong/humanizer-zh-academic)**（156 stars）— AI 写作模式识别、强制硬约束体系、噪声保留原则
- **[thesis-creator](https://github.com/GrammarSense/thesis-creator)**（156 stars）— P0-P3 优先级策略、学科适配矩阵、成语替换方法

## 局限性

- 本 skill 专注于**中文学术写作**，英文论文需另行适配
- 降重效果取决于原文的 AI 痕迹程度和修改深度，不保证在所有检测平台上通过
- AIGC 检测技术持续演进，本 skill 的规则需要随检测器升级而更新
- 扫描脚本基于规则匹配，无法替代专业检测平台的深度学习判别

## License

MIT
