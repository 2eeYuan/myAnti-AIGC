#!/usr/bin/env python3
"""
AIGC 特征扫描器 — 检测学术论文中的 AI 生成痕迹

基于知网 3.0 / 万方 / PaperPass 的检测原理，扫描以下维度：
  1. 模板句式密度
  2. 句子长度均匀度（突发性）
  3. 嵌套编号模式
  4. 冒号并列结构
  5. 被动语态比例
  6. 段落长度对称性
  7. 模糊表述密度
  8. 标点符号规律性

用法:
  python aigc_scan.py <file.txt> [--json] [--threshold 50]
  python aigc_scan.py --compare <before.txt> <after.txt>  # 改写前后对比
"""

import re
import sys
import json
import argparse
import math
from collections import Counter
from pathlib import Path


# ─── 模板句式库 ───
TEMPLATE_PATTERNS = [
    # 段落开头模板
    r'^(综上所述[，,])',
    r'^(基于.{2,10}(分析|研究|探讨))',
    r'^(通过.{2,15}(验证|实验|研究|测定))',
    r'^(随着.{2,20}(发展|进步|深入))',
    r'^(近年来[，,])',
    r'^(在.{2,20}(背景下|条件下|过程中))',
    r'^(本研究[旨在对通过])',
    r'^(目前[，,])',
    r'^(当前[，,])',
    r'^(因此[，,])',
    r'^(由此可见[，,])',
    r'^(总而言之[，,])',
    # 过渡词冗余
    r'(此外[，,])',
    r'(另外[，,])',
    r'(与此同时[，,])',
    r'(值得注意的是[，,])',
    r'(需要指出的是[，,])',
    # 模糊表述
    r'(据统计[，,])',
    r'(相关研究表明[，,])',
    r'(一般认为[，,])',
    r'(具有重要的.{2,10}(意义|价值|作用))',
    r'(具有广阔的应用前景)',
    r'(为.{2,20}(提供了|奠定了).{2,10}(基础|依据|参考))',
]

# 被动语态标记
PASSIVE_MARKERS = [
    r'被.{1,15}(测定|检测|验证|确认|证明|发现|计算)',
    r'由.{1,15}(进行|完成|测定|检测|计算)',
    r'经.{1,15}(测定|检测|计算|分析)',
    r'通过.{1,15}(测定|检测|验证|实验|计算)',
    r'采用.{1,15}(进行|测定|检测)',
]

# 嵌套编号模式
NESTED_NUM_PATTERN = re.compile(r'[（(](\d+)[）)]')

# 冒号并列模式
COLON_LIST_PATTERN = re.compile(r'[：:]\s*.+?[；;]\s*.+?[；;]')

# AI 高频词
AI_HIGH_FREQ_WORDS = [
    '至关重要', '不可忽视', '深远影响', '具有重要', '重要意义', '重要价值',
    '提供了重要', '标志着', '开启了', '值得注意的是', '需要指出的是',
    '综上所述', '由此可见', '总而言之', '不难发现', '具有良好的应用前景',
    '具有广阔的', '发挥着重要作用', '发挥着关键作用', '具有举足轻重',
    '在一定程度上', '从某种意义上说', '相关研究表明', '一般认为',
    '具有重要的理论价值', '具有重要的现实意义', '为.*提供了.*基础',
    '扮演着.*角色', '体现了.*理念', '基于.*理论', '依据.*框架',
]

# 全角标点
FULLWIDTH_PUNCT = set('，。！？；：、""''（）【】《》')


def load_text(filepath: str) -> str:
    """读取文本文件"""
    path = Path(filepath)
    if not path.exists():
        print(f"错误: 文件不存在 — {filepath}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding='utf-8')


def split_paragraphs(text: str) -> list[str]:
    """按段落分割"""
    paragraphs = re.split(r'\n\s*\n', text.strip())
    return [p.strip() for p in paragraphs if p.strip()]


def split_sentences(text: str) -> list[str]:
    """按句子分割（中文标点）"""
    sentences = re.split(r'[。！？；\n]+', text)
    return [s.strip() for s in sentences if s.strip()]


def count_chars(text: str) -> int:
    """统计中文字符数"""
    return len(re.findall(r'[一-鿿]', text))


def sentence_lengths(sentences: list[str]) -> list[int]:
    """计算每个句子的字符数"""
    return [count_chars(s) for s in sentences]


def mean(values: list[int]) -> float:
    """计算均值"""
    if not values:
        return 0.0
    return sum(values) / len(values)


def std_dev(values: list[int]) -> float:
    """计算标准差"""
    if len(values) < 2:
        return 0.0
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)


def coefficient_of_variation(values: list[int]) -> float:
    """计算变异系数"""
    m = mean(values)
    if m == 0:
        return 0.0
    return std_dev(values) / m


# ─── 维度 1: 模板句式密度 ───
def scan_template_patterns(text: str) -> dict:
    sentences = split_sentences(text)
    total = len(sentences)
    if total == 0:
        return {"score": 0, "count": 0, "total": 0, "details": []}

    matches = []
    for sent in sentences:
        for pattern in TEMPLATE_PATTERNS:
            if re.search(pattern, sent):
                matches.append(sent[:50])
                break

    density = len(matches) / total
    score = min(density * 100, 100)

    return {
        "score": round(score, 1),
        "count": len(matches),
        "total": total,
        "density": round(density, 3),
        "details": matches[:10]
    }


# ─── 维度 2: 句子长度均匀度（突发性） ───
def scan_burstiness(text: str) -> dict:
    sentences = split_sentences(text)
    lengths = sentence_lengths(sentences)

    if len(lengths) < 3:
        return {"score": 0, "cv": 0, "std": 0, "mean": 0}

    cv = coefficient_of_variation(lengths)
    std = std_dev(lengths)
    m = mean(lengths)

    # CV < 0.3 表示高度均匀（AI特征），CV > 0.5 表示自然波动
    if cv < 0.2:
        score = 80
    elif cv < 0.3:
        score = 60
    elif cv < 0.4:
        score = 40
    elif cv < 0.5:
        score = 20
    else:
        score = 0

    return {
        "score": score,
        "cv": round(cv, 3),
        "std": round(std, 1),
        "mean": round(m, 1),
        "min": min(lengths) if lengths else 0,
        "max": max(lengths) if lengths else 0,
    }


# ─── 维度 3: 嵌套编号模式 ───
def scan_nested_numbers(text: str) -> dict:
    matches = NESTED_NUM_PATTERN.findall(text)
    total_nums = len(matches)

    # 检查连续编号
    consecutive = 0
    prev = -1
    for m in matches:
        num = int(m)
        if prev >= 0 and num == prev + 1:
            consecutive += 1
        prev = num

    score = min(consecutive * 15, 100) if consecutive >= 3 else 0

    return {
        "score": score,
        "total_numbers": total_nums,
        "consecutive_sequences": consecutive,
    }


# ─── 维度 4: 冒号并列结构 ───
def scan_colon_lists(text: str) -> dict:
    matches = COLON_LIST_PATTERN.findall(text)
    score = min(len(matches) * 20, 100)

    return {
        "score": score,
        "count": len(matches),
        "details": [m[:60] for m in matches[:5]]
    }


# ─── 维度 5: 被动语态比例 ───
def scan_passive_voice(text: str) -> dict:
    sentences = split_sentences(text)
    total = len(sentences)
    if total == 0:
        return {"score": 0, "count": 0, "total": 0}

    passive_count = 0
    for sent in sentences:
        for pattern in PASSIVE_MARKERS:
            if re.search(pattern, sent):
                passive_count += 1
                break

    ratio = passive_count / total
    score = min(ratio * 200, 100)

    return {
        "score": round(score, 1),
        "count": passive_count,
        "total": total,
        "ratio": round(ratio, 3)
    }


# ─── 维度 6: 段落长度对称性 ───
def scan_paragraph_symmetry(paragraphs: list[str]) -> dict:
    lengths = [count_chars(p) for p in paragraphs]

    if len(lengths) < 3:
        return {"score": 0, "cv": 0, "std": 0, "mean": 0}

    cv = coefficient_of_variation(lengths)
    std = std_dev(lengths)
    m = mean(lengths)

    # 段落长度过于均匀是 AI 特征
    if cv < 0.2:
        score = 80
    elif cv < 0.3:
        score = 50
    elif cv < 0.4:
        score = 30
    else:
        score = 0

    return {
        "score": score,
        "cv": round(cv, 3),
        "std": round(std, 1),
        "mean": round(m, 1),
        "min": min(lengths),
        "max": max(lengths),
    }


# ─── 维度 7: 模糊表述密度 ───
def scan_vague_expressions(text: str) -> dict:
    vague_patterns = [
        r'有研究表明',
        r'相关研究指出',
        r'学界普遍认为',
        r'众所周知',
        r'一般认为',
        r'据统计',
        r'有学者认为',
        r'一些研究者',
        r'专家认为',
        r'业内普遍',
    ]

    count = 0
    details = []
    for pattern in vague_patterns:
        matches = re.findall(pattern, text)
        count += len(matches)
        if matches:
            details.append(f"{pattern}: {len(matches)}次")

    score = min(count * 20, 100)

    return {
        "score": score,
        "count": count,
        "details": details
    }


# ─── 维度 8: AI 高频词密度 ───
def scan_ai_high_freq_words(text: str) -> dict:
    count = 0
    details = []
    for word in AI_HIGH_FREQ_WORDS:
        matches = re.findall(word, text)
        if matches:
            count += len(matches)
            details.append(f"{word}: {len(matches)}次")

    total_chars = count_chars(text)
    density = count / max(total_chars / 1000, 1)  # 每千字

    score = min(density * 20, 100)

    return {
        "score": round(score, 1),
        "count": count,
        "density_per_1k": round(density, 2),
        "details": details[:10]
    }


# ─── 综合评分 ───
def compute_overall_score(dimensions: dict) -> float:
    """加权计算综合分数（0-100，越高越可能是 AI 生成）"""
    weights = {
        "template_patterns": 0.20,
        "burstiness": 0.20,
        "nested_numbers": 0.05,
        "colon_lists": 0.05,
        "passive_voice": 0.10,
        "paragraph_symmetry": 0.15,
        "vague_expressions": 0.10,
        "ai_high_freq_words": 0.15,
    }

    total = 0.0
    for dim_name, weight in weights.items():
        if dim_name in dimensions:
            total += dimensions[dim_name].get("score", 0) * weight

    return round(total, 1)


def identify_high_risk_paragraphs(paragraphs: list[str]) -> list[dict]:
    """识别高风险段落"""
    risks = []
    for i, para in enumerate(paragraphs):
        reasons = []
        sentences = split_sentences(para)

        # 检查模板词
        template_count = 0
        for sent in sentences:
            for pattern in TEMPLATE_PATTERNS:
                if re.search(pattern, sent):
                    template_count += 1
                    break
        if template_count >= 2:
            reasons.append(f"模板词{template_count}处")

        # 检查句长均匀度
        lengths = sentence_lengths(sentences)
        if len(lengths) >= 3:
            cv = coefficient_of_variation(lengths)
            if cv < 0.3:
                reasons.append(f"句长过于均匀(CV={cv:.2f})")

        # 检查三元并列
        if re.search(r'[：:]\s*.+?[；;]\s*.+?[；;]', para):
            reasons.append("冒号并列结构")

        # 检查段末总结
        last_sent = sentences[-1] if sentences else ""
        summary_words = ['综上所述', '由此可见', '总而言之', '不难发现', '可以看出']
        for word in summary_words:
            if word in last_sent:
                reasons.append(f"段末总结「{word}」")
                break

        # 检查 AI 高频词
        ai_word_count = 0
        for word in AI_HIGH_FREQ_WORDS:
            ai_word_count += len(re.findall(word, para))
        if ai_word_count >= 3:
            reasons.append(f"AI高频词{ai_word_count}处")

        if reasons:
            risks.append({
                "paragraph": i + 1,
                "preview": para[:80] + "..." if len(para) > 80 else para,
                "reasons": reasons,
                "risk_level": "high" if len(reasons) >= 3 else "medium"
            })

    return risks


def main():
    # 修复 Windows 终端编码问题
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description='AIGC 特征扫描器')
    parser.add_argument('file', help='要扫描的文本文件路径')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--threshold', type=float, default=50.0,
                        help='风险阈值（0-100，默认50）')
    parser.add_argument('--compare', metavar='BEFORE',
                        help='改写前文件路径，输出前后对比报告')
    args = parser.parse_args()

    # ─── 对比模式 ───
    if args.compare:
        run_compare(args.compare, args.file, args.json)
        return

    # ─── 单文件扫描模式 ───
    result = scan_single(args.file)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_single_report(result)


def scan_single(filepath: str) -> dict:
    """扫描单个文件，返回结果字典"""
    text = load_text(filepath)
    paragraphs = split_paragraphs(text)
    all_sentences = split_sentences(text)

    dimensions = {
        "template_patterns": scan_template_patterns(text),
        "burstiness": scan_burstiness(text),
        "nested_numbers": scan_nested_numbers(text),
        "colon_lists": scan_colon_lists(text),
        "passive_voice": scan_passive_voice(text),
        "paragraph_symmetry": scan_paragraph_symmetry(paragraphs),
        "vague_expressions": scan_vague_expressions(text),
        "ai_high_freq_words": scan_ai_high_freq_words(text),
    }

    overall_score = compute_overall_score(dimensions)
    high_risk = identify_high_risk_paragraphs(paragraphs)

    return {
        "file": str(filepath),
        "overall_score": overall_score,
        "risk_level": "high" if overall_score >= 70 else "medium" if overall_score >= 40 else "low",
        "total_paragraphs": len(paragraphs),
        "total_sentences": len(all_sentences),
        "total_chars": count_chars(text),
        "dimensions": dimensions,
        "high_risk_paragraphs": high_risk,
        "high_risk_count": len(high_risk),
    }


def print_single_report(result: dict):
    """打印单文件扫描报告"""
    print(f"\n{'='*60}")
    print(f"  AIGC 特征扫描报告")
    print(f"{'='*60}")
    print(f"  文件: {result['file']}")
    print(f"  段落数: {result['total_paragraphs']}  |  句子数: {result['total_sentences']}  |  字数: {result['total_chars']}")
    print(f"{'='*60}")

    risk_emoji = "[HIGH]" if result["risk_level"] == "high" else "[MED]" if result["risk_level"] == "medium" else "[LOW]"
    print(f"\n  {risk_emoji} 综合风险评分: {result['overall_score']}/100 ({result['risk_level']})")

    print(f"\n  {'维度':<20} {'得分':>6} {'详情'}")
    print(f"  {'-'*50}")

    dim_names = {
        "template_patterns": "模板句式密度",
        "burstiness": "句长均匀度",
        "nested_numbers": "嵌套编号",
        "colon_lists": "冒号并列",
        "passive_voice": "被动语态",
        "paragraph_symmetry": "段落对称性",
        "vague_expressions": "模糊表述",
        "ai_high_freq_words": "AI高频词",
    }

    dimensions = result["dimensions"]
    for dim_key, dim_name in dim_names.items():
        dim = dimensions[dim_key]
        score = dim.get("score", 0)
        bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))

        extra = ""
        if dim_key == "burstiness":
            extra = f"CV={dim.get('cv', 0):.3f}"
        elif dim_key == "template_patterns":
            extra = f"{dim.get('count', 0)}/{dim.get('total', 0)}句"
        elif dim_key == "ai_high_freq_words":
            extra = f"{dim.get('density_per_1k', 0):.1f}/千字"
        elif dim_key == "vague_expressions":
            extra = f"{dim.get('count', 0)}处"

        print(f"  {dim_name:<18} {bar} {score:>5.1f}  {extra}")

    high_risk = result["high_risk_paragraphs"]
    if high_risk:
        print(f"\n  [!] 高风险段落 ({len(high_risk)} 个):")
        print(f"  {'-'*50}")
        for risk in high_risk:
            level = "[H]" if risk["risk_level"] == "high" else "[M]"
            print(f"  {level} 第{risk['paragraph']}段: {', '.join(risk['reasons'])}")
            print(f"     {risk['preview'][:60]}...")
    else:
        print(f"\n  [OK] 未发现高风险段落")

    print(f"\n  {'='*60}")
    overall = result["overall_score"]
    if overall >= 70:
        print("  建议: 需要深度改写。运行三轮降重协议。")
    elif overall >= 40:
        print("  建议: 需要局部修改。重点处理高风险段落。")
    else:
        print("  建议: 风险较低。可做轻度润色。")
    print(f"  {'='*60}\n")


def run_compare(before_path: str, after_path: str, as_json: bool):
    """改写前后对比扫描"""
    before = scan_single(before_path)
    after = scan_single(after_path)

    if as_json:
        comparison = {
            "before": before,
            "after": after,
            "delta": {
                "overall_score": round(after["overall_score"] - before["overall_score"], 1),
                "high_risk_count": after["high_risk_count"] - before["high_risk_count"],
                "char_diff": after["total_chars"] - before["total_chars"],
            }
        }
        print(json.dumps(comparison, ensure_ascii=False, indent=2))
        return

    dim_names = {
        "template_patterns": "模板句式密度",
        "burstiness": "句长均匀度",
        "nested_numbers": "嵌套编号",
        "colon_lists": "冒号并列",
        "passive_voice": "被动语态",
        "paragraph_symmetry": "段落对称性",
        "vague_expressions": "模糊表述",
        "ai_high_freq_words": "AI高频词",
    }

    print(f"\n{'='*64}")
    print(f"  AIGC 改写前后对比报告")
    print(f"{'='*64}")

    # 基本信息
    print(f"\n  改写前: {before_path}")
    print(f"    段落: {before['total_paragraphs']}  句子: {before['total_sentences']}  字数: {before['total_chars']}")
    print(f"  改写后: {after_path}")
    print(f"    段落: {after['total_paragraphs']}  句子: {after['total_sentences']}  字数: {after['total_chars']}")

    char_diff = after['total_chars'] - before['total_chars']
    char_pct = (char_diff / max(before['total_chars'], 1)) * 100
    sign = "+" if char_diff >= 0 else ""
    print(f"  字数变化: {sign}{char_diff} ({sign}{char_pct:.1f}%)")

    # 综合评分对比
    b_score = before["overall_score"]
    a_score = after["overall_score"]
    delta = a_score - b_score
    delta_sign = "+" if delta >= 0 else ""
    arrow = "v" if delta < 0 else "^" if delta > 0 else "="

    b_level = before["risk_level"]
    a_level = after["risk_level"]

    print(f"\n  {'='*64}")
    print(f"  综合风险评分")
    print(f"  {'='*64}")
    print(f"  改写前: {b_score}/100 ({b_level})")
    print(f"  改写后: {a_score}/100 ({a_level})")
    print(f"  变化:   {delta_sign}{delta} [{arrow}]")

    if delta < -10:
        print(f"  >>> 明显改善")
    elif delta < 0:
        print(f"  >>> 有所改善")
    elif delta == 0:
        print(f"  >>> 无变化")
    else:
        print(f"  >>> 注意: 评分上升，可能需要重新检查改写策略")

    # 各维度对比
    print(f"\n  {'='*64}")
    print(f"  各维度对比")
    print(f"  {'='*64}")
    print(f"  {'维度':<16} {'改写前':>8} {'改写后':>8} {'变化':>8} {'趋势'}")
    print(f"  {'-'*60}")

    for dim_key, dim_name in dim_names.items():
        b_dim = before["dimensions"][dim_key]
        a_dim = after["dimensions"][dim_key]
        b_s = b_dim.get("score", 0)
        a_s = a_dim.get("score", 0)
        d = a_s - b_s
        d_sign = "+" if d > 0 else "" if d == 0 else ""
        trend = "v" if d < 0 else "^" if d > 0 else "="

        # 附加信息
        extra_before = ""
        extra_after = ""
        if dim_key == "burstiness":
            extra_before = f"CV={b_dim.get('cv', 0):.3f}"
            extra_after = f"CV={a_dim.get('cv', 0):.3f}"
        elif dim_key == "template_patterns":
            extra_before = f"{b_dim.get('count', 0)}处"
            extra_after = f"{a_dim.get('count', 0)}处"
        elif dim_key == "ai_high_freq_words":
            extra_before = f"{b_dim.get('density_per_1k', 0):.1f}/千字"
            extra_after = f"{a_dim.get('density_per_1k', 0):.1f}/千字"

        print(f"  {dim_name:<14} {b_s:>6.1f}  {extra_before:>10}  {a_s:>6.1f}  {extra_after:>10}  {d_sign}{d} {trend}")

    # 高风险段落变化
    b_hr = before["high_risk_count"]
    a_hr = after["high_risk_count"]
    hr_delta = a_hr - b_hr

    print(f"\n  {'='*64}")
    print(f"  高风险段落")
    print(f"  {'='*64}")
    print(f"  改写前: {b_hr} 个高风险段落")
    print(f"  改写后: {a_hr} 个高风险段落")

    if hr_delta < 0:
        print(f"  >>> 减少了 {abs(hr_delta)} 个高风险段落")
    elif hr_delta > 0:
        print(f"  >>> 注意: 增加了 {hr_delta} 个高风险段落")
    else:
        print(f"  >>> 高风险段落数量未变")

    # 改写后仍存在的高风险段落
    if after["high_risk_paragraphs"]:
        print(f"\n  改写后仍需关注的段落:")
        for risk in after["high_risk_paragraphs"]:
            level = "[H]" if risk["risk_level"] == "high" else "[M]"
            print(f"  {level} 第{risk['paragraph']}段: {', '.join(risk['reasons'])}")

    # 总结
    print(f"\n  {'='*64}")
    if delta < -10 and a_score < 40:
        print("  结论: 改写效果良好，风险等级降至低风险。")
    elif delta < 0:
        print("  结论: 改写有效果，建议对剩余高风险段落做针对性修改。")
    elif delta == 0:
        print("  结论: 风险评分无变化，建议调整改写策略后重试。")
    else:
        print("  结论: 风险评分上升，改写可能引入了新的 AI 模式，需要重新审视。")
    print(f"  {'='*64}\n")


if __name__ == '__main__':
    main()
