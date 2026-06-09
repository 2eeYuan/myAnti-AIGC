# myAnti-AIGC

English | [中文](README.md)

A Claude Code Skill for reducing AIGC detection rates in Chinese and English academic papers.

Synthesized from three popular open-source projects ([aigc-reduce](https://github.com/ydyjya/aigc-reduce), [humanizer-zh-academic](https://github.com/CJayWong/humanizer-zh-academic), [thesis-creator](https://github.com/GrammarSense/thesis-creator)), optimized for Chinese academic writing scenarios.

## Supported Scenarios

| Scenario | Support |
|----------|---------|
| Journal papers | Supported |
| Thesis (Bachelor/Master/PhD) | Supported |
| Research reports | Supported |
| Academic blogs / commentaries | Supported |

**Supported languages**: Chinese / English

**Trigger words**: 降AIGC率, 去AI味, 人工润色, humanize, 论文降重, AI痕迹消除, reduce AI detection, academic humanizer, remove AI patterns, de-AI

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3.10+ (for the scanning script)

### Setup

**Option 1: Clone into your project directory**

```bash
cd your-project-directory
git clone https://github.com/2eeYuan/myAnti-AIGC.git
```

**Option 2: Clone into Claude Code global skill directory**

```bash
cd ~/.claude/skills
git clone https://github.com/2eeYuan/myAnti-AIGC.git
```

**Option 3: Manual download**

Download the ZIP and ensure the following directory structure:

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

## Usage

### 1. Natural Language Trigger

Simply describe your needs in Claude Code:

```
> Help me reduce the AIGC detection rate of this paper
> This text has too high an AI score, please polish it
> Remove AI traces from chapter 3 of my thesis
```

Claude Code will automatically load the skill and execute a 3-step workflow:

1. **Risk Assessment Report** — Scan and list high-risk paragraphs with matched patterns
2. **Rewrite** — Output revised version after user confirmation
3. **Post-Rewrite Verification** — Re-scan and generate a before/after comparison report until risk drops to low level

### 2. Manual Scanning

Supports `.txt`, `.pdf`, and `.docx` formats. PDF text is extracted page-by-page with page tracking. DOCX detects page breaks for page boundaries.

```bash
# Chinese scan (default)
python skills/myAnti-AIGC/scripts/aigc_scan.py your_paper.txt

# English scan
python skills/myAnti-AIGC/scripts/aigc_scan.py your_paper.txt --lang en

# Scan PDF (auto-extracts text per page, reports page numbers)
python skills/myAnti-AIGC/scripts/aigc_scan.py your_paper.pdf

# Scan DOCX (detects page breaks, reports page numbers)
python skills/myAnti-AIGC/scripts/aigc_scan.py your_paper.docx

# JSON output (for programmatic use)
python skills/myAnti-AIGC/scripts/aigc_scan.py your_paper.txt --json

# Before/after comparison
python skills/myAnti-AIGC/scripts/aigc_scan.py --compare original.txt rewritten.txt

# English before/after comparison
python skills/myAnti-AIGC/scripts/aigc_scan.py --compare before.txt after.txt --lang en
```

Scan output example:

```
============================================================
  AIGC Feature Scan Report
============================================================
  File: paper.txt
  Paragraphs: 12  |  Sentences: 68  |  Characters: 3200
============================================================

  [MED] Overall Risk Score: 48.5/100 (medium)

  Dimension              Score   Details
  --------------------------------------------------
  Template Patterns  ██████░░░░  62.5  8/68 sentences
  Sentence Uniformity ████░░░░░░  40.0  CV=0.312
  Nested Numbers     ██░░░░░░░░  20.0
  Colon Lists        ░░░░░░░░░░   0.0
  Passive Voice      ███░░░░░░░  30.0
  Paragraph Symmetry █████░░░░░  50.0
  Vague Expressions  ████░░░░░░  40.0  2 found
  AI High-Freq Words ██████░░░░  60.0  6.2/1000 chars

  [!] High-Risk Paragraphs (3):
  [H] Para 1 (P1): template phrase x2, AI high-freq word x3
     | With the rapid development of AI technology, NLP has made...
  [M] Para 3 (P1): uniform sentence length (CV=0.22)
     | This study employs deep learning methods for experiments...
  [H] Para 7 (P2): template phrase x3, concluding cliche "综上所述"
     | In conclusion, this research has important theoretical value...

  Recommendation: Partial revision needed. Focus on high-risk paragraphs.
```

### 3. Before/After Comparison

After rewriting, verify the effect with `--compare` mode:

```bash
python skills/myAnti-AIGC/scripts/aigc_scan.py --compare original.txt rewritten.txt
```

Comparison report example:

```
================================================================
  AIGC Before/After Comparison Report
================================================================

  Before: original.txt
    Paragraphs: 3  Sentences: 9  Characters: 198
  After: rewritten.txt
    Paragraphs: 4  Sentences: 13  Characters: 264
  Character diff: +66 (+33.3%)

  ================================================================
  Overall Risk Score
  ================================================================
  Before: 56.3/100 (medium)
  After:  19.5/100 (low)
  Change: -36.8 [v]
  >>> Significant improvement

  ================================================================
  Dimension Comparison
  ================================================================
  Dimension           Before   After   Change  Trend
  ------------------------------------------------------------
  Template Patterns    66.7     0.0   -66.7 v
  Sentence Uniformity  60.0    60.0     0.0 =
  Paragraph Symmetry   80.0    50.0   -30.0 v
  Vague Expressions    40.0     0.0   -40.0 v
  AI High-Freq Words  100.0     0.0  -100.0 v

  Conclusion: Rewrite effective. Risk level dropped to low.
```

## Core Methodology

### Four Iron Rules

1. **No AI Full Rewrite** — Using AI to rewrite AI text stacks AI fingerprints. All edits must be deterministic string replacements.
2. **Modification Rate > 40%** — Deep modification (>40%) achieves 60-80% detection evasion rate.
3. **Deterministic Replacement** — Each edit changes only a small portion, preserving most of the original tokens.
4. **Maintain Academic Register** — Reducing AI traces is not the same as making text colloquial. Academic standards must be upheld.

### Three-Round Reduction Protocol

| Round | Goal | Methods |
|-------|------|---------|
| Round 1 | Remove AI traces (subtraction) | Word-level replacement → Sentence restructuring → Paragraph adjustment |
| Round 2 | Inject human characteristics (addition) | Rhythm engineering, uncertainty injection, operational details |
| Round 3 | Anti-AI audit (self-check) | Systematic scan for remaining AI patterns |

### 21 AI Pattern Recognition Modes

Covers content-level patterns (theory-first openings, summary clichés, triple parallelism, passive analysis phrases) and statistical patterns (significance inflation, synonym cycling, generic conclusions, em dash overuse, etc.).

See [`references/ai-patterns.md`](skills/myAnti-AIGC/references/ai-patterns.md) for details.

### Hard Constraints

| Constraint | Hard Limit | Description |
|------------|------------|-------------|
| AI high-frequency words | ≤ 2 per paragraph | Must replace excess |
| Paragraph-ending summary phrases | ≤ 1 in entire text | Must delete or rewrite |
| Triple parallelism | ≤ 1 per paragraph | Must break symmetry |
| "Based on XX theory" paragraph openings | ≤ 20% of paragraphs | Must relocate |
| Bold text in body | ≤ 5 in entire text | Must reduce |
| Generic conclusions | 0 in entire text | Fix immediately |
| Vague attribution | 0 in entire text | Delete or make specific |

## Project Structure

```
myAnti-AIGC/
├── .claude-plugin/
│   └── plugin.json              ← Skill registration
├── skills/
│   └── myAnti-AIGC/
│       ├── SKILL.md             ← Core instructions (bilingual)
│       ├── references/
│       │   ├── ai-patterns.md        ← Chinese AI pattern library (21 patterns)
│       │   ├── replacement-tables.md ← Chinese replacement tables + AI word lists
│       │   ├── detection-principles.md ← Detector principles (CNKI 3.0 / Wanfang / GPTZero)
│       │   ├── en-ai-patterns.md     ← English AI patterns (26 content + 49 structural)
│       │   └── en-replacement-tables.md ← English replacement tables + 3-tier AI word lists
│       └── scripts/
│           └── aigc_scan.py     ← 8-dimension scanner (zh/en + before/after comparison)
├── .gitignore
├── README.md
└── README_EN.md
```

### File Responsibilities

| File | Purpose | When Loaded |
|------|---------|-------------|
| `plugin.json` | Tells Claude Code a skill exists here | At system startup |
| `SKILL.md` | Complete work manual: role, rules, workflow, strategies (bilingual) | When user triggers the skill |
| `ai-patterns.md` | Chinese AI writing pattern identification and rewriting guide | On-demand during Chinese audit |
| `replacement-tables.md` | Chinese replacement rules and word lists | On-demand during Chinese Round 1 |
| `en-ai-patterns.md` | English AI patterns (merged from 3 open-source projects) | On-demand during English audit |
| `en-replacement-tables.md` | English replacement tables + 3-tier AI word lists + legitimate phrase whitelist | On-demand during English Round 1 |
| `detection-principles.md` | How detectors work (CNKI / Wanfang / GPTZero) | On-demand for understanding detection logic |
| `aigc_scan.py` | Automated scanner, `--lang zh\|en` + `--compare` | Triggered by SKILL.md instructions |

## Scan Dimensions

`aigc_scan.py` detects AI traces across 8 dimensions with weighted scoring (0-100):

| Dimension | Weight | Detection |
|-----------|--------|-----------|
| Template Patterns | 20% | Frequency of template phrases like "综上所述", "基于…分析" |
| Sentence Uniformity (Burstiness) | 20% | Coefficient of variation in sentence length; AI text CV < 0.3 |
| Nested Numbers | 5% | Sequential (1)(2)(3) numbering patterns |
| Colon Lists | 5% | Triple parallelism: "：A；B；C" structures |
| Passive Voice | 10% | Passive markers like "被测定为", "由…进行" |
| Paragraph Symmetry | 15% | Whether consecutive paragraphs have similar lengths |
| Vague Expressions | 10% | Unsourced claims like "有研究表明", "专家认为" |
| AI High-Freq Words | 15% | Words like "至关重要", "不可忽视", "具有重要意义" |

**Risk Levels**: Score ≥ 70 = high risk, 40-69 = medium risk, < 40 = low risk.

## Reference Projects

This skill's methodology is derived from the following open-source projects:

**Chinese:**
- **[aigc-reduce](https://github.com/ydyjya/aigc-reduce)** (282 stars) — Deterministic replacement, three-round protocol, scanner tool
- **[humanizer-zh-academic](https://github.com/CJayWong/humanizer-zh-academic)** (156 stars) — AI pattern recognition, hard constraints, noise preservation
- **[thesis-creator](https://github.com/GrammarSense/thesis-creator)** (156 stars) — P0-P3 priority, discipline adaptation, idiom replacement

**English:**
- **[humanizer_academic](https://github.com/matsuikentaro1/humanizer_academic)** (99 stars) — Medical/academic patterns, legitimate phrase whitelist
- **[slopbuster](https://github.com/gabelul/slopbuster)** (16 stars) — 49 structural rules, multi-mode scanner, 10-point scoring
- **[humanize-academic-writing](https://github.com/momo2young/humanize-academic-writing)** (14 stars) — Social science focus, rhythm engineering, specificity injection

## Limitations

- This skill focuses on **Chinese academic writing**; English papers require separate adaptation
- Effectiveness depends on the original text's AI trace level and modification depth; no guarantee of passing all detection platforms
- AIGC detection technology evolves continuously; rules need updating as detectors improve
- The scanner is rule-based and cannot replace deep learning classifiers used by professional detection platforms

## License

MIT
