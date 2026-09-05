import json
import sys
from pathlib import Path

# 针对漏斗和 R13 的核心关注词
CORE_KEYWORDS = ["初步接触", "需求确认", "方案演示", "商务谈判", "赢单", "丢单", "funnel", "转化率"]

def extract_content(obj):
    """递归提取 JSON 中的关键文本（优先抓代码、命令、执行输出）"""
    results = []
    if isinstance(obj, dict):
        # 常见智能体轨迹中的代码与输出字段
        for k in ["code", "command", "text", "content", "arguments", "output", "result", "stdout"]:
            if k in obj and obj[k]:
                results.append(str(obj[k]))
        for v in obj.values():
            results.extend(extract_content(v))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(extract_content(item))
    return results

def inspect_trajectory(file_path, agent_name):
    p = Path(file_path)
    if not p.exists():
        print(f"❌ 文件不存在: {p}")
        return

    print(f"\n" + "="*80)
    print(f" 正在深入解析 {agent_name} 轨迹中的【漏斗计算与 R13 关键证据】")
    print("="*80)

    with p.open("r", encoding="utf-8", errors="ignore") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            
            # 只有同时包含核心漏斗词汇时才抓取
            if any(kw in line for kw in CORE_KEYWORDS):
                try:
                    data = json.loads(line)
                    event_type = data.get("type", "N/A")
                    
                    # 提取所有包含关键词的文本片段
                    text_blocks = extract_content(data)
                    relevant_snippets = []
                    for tb in text_blocks:
                        if any(kw in tb for kw in CORE_KEYWORDS):
                            relevant_snippets.append(tb.strip())
                    
                    if relevant_snippets:
                        print(f"\n>>> 【{agent_name} 物理行号: 第 {line_no} 行】 | 事件类型: {event_type}")
                        # 去重打印最核心的内容
                        seen = set()
                        for s in relevant_snippets:
                            snippet_key = s[:100]
                            if snippet_key not in seen:
                                seen.add(snippet_key)
                                # 限制单段长度，避免满屏过长
                                display_text = s if len(s) < 1200 else (s[:1000] + "\n...[内容过长截断]...")
                                print("-" * 40)
                                print(display_text)
                                print("-" * 40)
                except Exception as e:
                    pass

if __name__ == "__main__":
    # codex 文件的路径
    #codex_path = r"D:\RL\BPO试标题及规则文档\BPO璇曟爣棰樺強瑙勫垯鏂囨。\杞ㄨ抗瀵规瘮褰掑洜\RL\codex\sft_gdpeval_007_saas_sales_performance_analysis\trajectory\01a02fb4-6541-7c50-ae20-81ccc6b53d7b.jsonl"
    
    # workbuddy 文件的路径
    workbuddy_path = r"D:\RL\BPO试标题及规则文档\BPO璇曟爣棰樺強瑙勫垯鏂囨。\杞ㄨ抗瀵规瘮褰掑洜\RL\workbuddy\sft_gdpeval_007_saas_sales_performance_analysis\trajectory\9340eb1b-3109-4f02-a1a6-0aae7ed672dc.jsonl"

    # codex 路径分析：  

    #inspect_trajectory(codex_path, "Codex")
    
    #  workbuddy 路径分析：

    inspect_trajectory(workbuddy_path, "WorkBuddy")