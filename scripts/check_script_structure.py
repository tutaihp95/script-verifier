#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_script_structure.py
--------------------------
TẦNG 1 STATIC LINTER - KIỂM ĐỊNH KỸ THUẬT CỨNG CHO KỊCH BẢN VOICE (0 TOKEN, < 0.2s)
Tuân thủ tiêu chuẩn SSOT: UNIVERSAL_SCRIPT_VERIFICATION_PLAYBOOK.md

Chức năng:
  1. Kiểm tra ngân sách từ theo từng Part (sai số <= ±10%) và toàn bài (<= ±5%) đối chiếu OUTLINE.md
  2. Rào cản độ dài dòng thoại: mục tiêu < 115 ký tự, trần cứng tối đa <= 150 ký tự
  3. Chuẩn hóa TTS 100%: 0 chữ số 0-9, 0 ký tự $, %, 0 mã Markdown, 0 thẻ nhãn lạ
  4. Quét sạch từ rác AI (Anti-Slop) và cấu trúc nhị phân mòn vẹt

Exit Codes:
  0: PASS (Đạt chuẩn kỹ thuật, sẵn sàng chuyển Tầng 2 LLM Double-Blind Review)
  1: FAIL (Có lỗi cơ học, cần sửa trực tiếp tại số dòng được chỉ định)
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path

# Cấu hình UTF-8 cho Windows Terminal
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Từ điển rác AI mặc định (fallback nếu không đọc được file json)
DEFAULT_SLOP = {
    "banned_words_en": [
        "delve", "unravel", "tapestry", "beacon", "testament",
        "navigate", "landscape", "at its core", "vital", "crucial",
        "game-changer", "game changer", "ever-evolving", "ever evolving",
        "shed light on", "realm", "multifaceted"
    ],
    "cliche_openings_en": [
        "in today's fast-paced world", "in today's world",
        "have you ever wondered why", "have you ever wondered",
        "throughout history", "since the dawn of time"
    ],
    "preachy_phrases_en": [
        "it's important to remember that", "it's important to note that",
        "it is important to remember", "serves as a testament to",
        "serves as a reminder", "a multifaceted issue",
        "it's worth noting", "it is worth noting"
    ],
    "signposted_endings_en": [
        "in conclusion", "to sum up", "wrapping up",
        "that's all for today", "thanks for watching",
        "don't forget to like and subscribe", "make sure to subscribe"
    ],
    "banned_words_vi": [
        "bức tranh toàn cảnh", "vén màn bí mật", "hãy cùng đi sâu vào",
        "chìa khóa vạn năng", "bước ngoặt lịch sử", "khiến chúng ta phải suy ngẫm",
        "không thể phủ nhận rằng"
    ],
    "binary_contrast_patterns": [
        r"(?i)\b(?:not\s+because|it['’]?s\s+not\s+about)\b.*?\b(?:but|it['’]?s\s+about)\b",
        r"(?i)\b(?:không\s+phải\s+vì|không\s+chỉ\s+là)\b.*?\b(?:mà\s+là|mà\s+còn\s+là)\b",
        r"(?i)\b[\w\s]+\s+isn['’]?t\s+the\s+(?:problem|issue|point),\s+[\w\s]+\s+is\b"
    ]
}


def load_slop_dictionary(script_dir):
    """Tìm và nạp từ điển slop từ resources/ai_slop_dictionary.json"""
    possible_paths = [
        script_dir / "resources" / "ai_slop_dictionary.json",
        script_dir.parent / "resources" / "ai_slop_dictionary.json",
        Path(__file__).resolve().parent.parent / "resources" / "ai_slop_dictionary.json",
    ]
    for p in possible_paths:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return DEFAULT_SLOP


def extract_part_targets_from_outline(outline_path, default_wpm=150):
    """
    Bóc tách ngân sách số từ cho từng Hồi (Part) từ OUTLINE.md
    Hỗ trợ các dạng:
      - 'Part 1: ... (~130 từ)'
      - 'PHẦN I: ... (~130 từ)'
      - 'Part 2 ... (0:45 – 3:45)' -> tính từ thời lượng * WPM
    """
    if not outline_path or not os.path.exists(outline_path):
        return {}

    with open(outline_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    targets = {}

    # Dạng 1: Tìm dòng tiêu đề có số từ rõ ràng: ~X từ hoặc ~X words
    # Ví dụ: ## PHẦN I: COLD-OPEN (0:00 – 0:45 | ~130 từ)
    p_header_word = re.findall(
        r"(?:PART|PHẦN|HỒI)\s+([0-9IVXLCDM]+)[\s\S]*?~([0-9]+)\s*(?:từ|words)",
        content,
        re.IGNORECASE
    )
    for part_id_raw, word_count in p_header_word:
        p_num = normalize_part_num(part_id_raw)
        if p_num:
            targets[p_num] = int(word_count)

    # Dạng 2: Bóc tách từ bảng Macro Progression Map hoặc thời lượng (0:45 - 3:45)
    # Nếu chưa có mục tiêu từ Dạng 1
    duration_matches = re.findall(
        r"PART\s+([0-9]+)[\s\S]*?\((\d+):(\d{2})\s*[-–]\s*(\d+):(\d{2})\)",
        content,
        re.IGNORECASE
    )
    for p_str, m1, s1, m2, s2 in duration_matches:
        p_num = int(p_str)
        if p_num not in targets:
            dur_sec = (int(m2) * 60 + int(s2)) - (int(m1) * 60 + int(s1))
            if dur_sec > 0:
                est_words = int(dur_sec * (default_wpm / 60.0))
                targets[p_num] = est_words

    return targets


def normalize_part_num(val):
    val = str(val).strip().upper()
    if val.isdigit():
        return int(val)
    roman_map = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10}
    return roman_map.get(val, None)


def extract_part_number_from_filename(filename):
    match = re.search(r"part[-_]?(\d+)", filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def lint_part_file(file_path, target_words=None, tolerance_part=0.10, slop_dict=None):
    """
    Quét kiểm định cơ học cho 1 tệp kịch bản Part:
    Trả về dict chứa danh sách lỗi và thống kê.
    """
    if slop_dict is None:
        slop_dict = DEFAULT_SLOP

    results = {
        "file": str(file_path),
        "filename": os.path.basename(file_path),
        "total_words": 0,
        "total_lines": 0,
        "target_words": target_words,
        "tolerance_part": tolerance_part,
        "word_budget_status": "PASS",
        "word_budget_error_pct": 0.0,
        "hard_errors": [],
        "warnings": [],
    }

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_lines = f.readlines()

    all_words = []
    line_num = 0

    for raw_line in raw_lines:
        line_num += 1
        line = raw_line.strip()
        if not line:
            continue

        results["total_lines"] += 1
        words_in_line = line.split()
        all_words.extend(words_in_line)

        # 1. Kiểm tra độ dài dòng
        line_len = len(line)
        if line_len > 150:
            results["hard_errors"].append(
                f"Dòng {line_num} vượt trần cứng 150 ký tự ({line_len} kt): '{line[:60]}...'"
            )
        elif line_len >= 115:
            results["warnings"].append(
                f"Dòng {line_num} dài hơn mức khuyến nghị 115 ký tự ({line_len} kt): '{line[:50]}...'"
            )

        # 2. Kiểm tra chữ số 0-9
        digit_matches = re.findall(r"\b\d+[\d.,]*\b|\d+", line)
        if digit_matches:
            results["hard_errors"].append(
                f"Dòng {line_num} chứa chữ số chưa chuẩn hóa sang chữ viết: {', '.join(digit_matches)}"
            )

        # 3. Kiểm tra ký tự tiền tệ & phần trăm: $, %, €, £, ¥
        symbol_matches = re.findall(r"[$%€£¥]", line)
        if symbol_matches:
            results["hard_errors"].append(
                f"Dòng {line_num} chứa ký hiệu đặc biệt ({', '.join(set(symbol_matches))}) chưa chuyển thành chữ"
            )

        # 4. Kiểm tra mã Markdown
        if re.search(r"^#+\s", line):
            results["hard_errors"].append(f"Dòng {line_num} chứa thẻ tiêu đề Markdown: '{line[:40]}'")
        if re.search(r"\*\*.*?\*\*|\*[^*]+\*|__.*?__", line):
            results["hard_errors"].append(f"Dòng {line_num} chứa ký tự in đậm/nghiêng Markdown: '{line[:50]}'")
        if re.search(r"^>\s", line):
            results["hard_errors"].append(f"Dòng {line_num} chứa ký tự trích dẫn Markdown (>)")

        # 5. Kiểm tra thẻ nhãn cảm xúc lạ hoặc thẻ ngắt nghỉ
        if re.search(r"\[pause[^\]]*\]|\[beat[^\]]*\]|\[visual[^\]]*\]", line, re.IGNORECASE):
            results["hard_errors"].append(f"Dòng {line_num} chứa thẻ âm học / visual cue dạng [tag]")
        if re.search(r"^\([a-zA-Z\s,:-]+\)", line):
            results["hard_errors"].append(f"Dòng {line_num} chứa thẻ Tone Tag đầu dòng: '{line[:35]}'")

        # 6. Kiểm tra từ rác AI (Anti-Slop)
        line_lower = line.lower()
        for banned in slop_dict.get("banned_words_en", []):
            pattern = r"\b" + re.escape(banned.lower()) + r"\b"
            if re.search(pattern, line_lower):
                results["hard_errors"].append(f"Dòng {line_num} chứa từ rác AI cấm (Anti-Slop): '{banned}'")

        for banned_vi in slop_dict.get("banned_words_vi", []):
            if banned_vi.lower() in line_lower:
                results["hard_errors"].append(f"Dòng {line_num} chứa cụm từ rác tiếng Việt: '{banned_vi}'")

        for preachy in slop_dict.get("preachy_phrases_en", []):
            if preachy.lower() in line_lower:
                results["hard_errors"].append(f"Dòng {line_num} chứa câu thuyết giáo AI: '{preachy}'")

        for ending in slop_dict.get("signposted_endings_en", []):
            if ending.lower() in line_lower:
                results["hard_errors"].append(f"Dòng {line_num} chứa cụm từ báo kết bài sáo rỗng: '{ending}'")

        # 7. Kiểm tra cấu trúc nhị phân mòn vẹt
        for bp in slop_dict.get("binary_contrast_patterns", []):
            if re.search(bp, line, re.IGNORECASE):
                results["hard_errors"].append(
                    f"Dòng {line_num} vi phạm cấu trúc đối lập nhị phân ('Not because X, but Y'): '{line[:50]}...'"
                )

    results["total_words"] = len(all_words)

    # 8. Kiểm tra ngân sách từ đối chiếu Outline
    if target_words and target_words > 0:
        actual = results["total_words"]
        diff = actual - target_words
        err_pct = (diff / target_words) * 100.0
        results["word_budget_error_pct"] = round(err_pct, 1)

        min_words = int(target_words * (1.0 - tolerance_part))
        max_words = int(target_words * (1.0 + tolerance_part))

        if actual < min_words or actual > max_words:
            results["word_budget_status"] = "FAIL"
            results["hard_errors"].append(
                f"Lệch ngân sách từ Part: Thực tế {actual} từ / Mục tiêu {target_words} từ "
                f"({err_pct:+.1f}%, vượt ngưỡng cho phép ±{int(tolerance_part*100)}% [{min_words} – {max_words} từ])"
            )

    return results


def find_outline_in_context(target_dir):
    """Tìm OUTLINE.md ở thư mục hiện tại hoặc các cấp cha"""
    curr = Path(target_dir).resolve()
    for _ in range(4):
        candidate = curr / "OUTLINE.md"
        if candidate.exists():
            return candidate
        curr = curr.parent
    return None


def locate_script_files(target_path):
    """Xác định danh sách tệp part-X.txt hoặc script_en_part_X.txt"""
    p = Path(target_path)
    if p.is_file():
        return [p]

    # Nếu là thư mục, tìm trong thư mục con 01_script/ trước
    part_files = []
    sub_01 = p / "01_script"
    if sub_01.exists() and sub_01.is_dir():
        part_files = sorted(list(sub_01.glob("part-*.txt")) + list(sub_01.glob("script_en_part_*.txt")))

    if not part_files:
        part_files = sorted(list(p.glob("part-*.txt")) + list(p.glob("script_en_part_*.txt")))

    return part_files


def main():
    parser = argparse.ArgumentParser(
        description="check_script_structure.py - Tầng 1 Static Python Linter cho kịch bản voice YouTube"
    )
    parser.add_argument("target", nargs="?", default=".", help="Đường dẫn thư mục tập phim hoặc thư mục 01_script")
    parser.add_argument("--part", help="Chỉ kiểm định một tệp Part cụ thể (ví dụ: part-1.txt)")
    parser.add_argument("--outline", help="Chỉ định đường dẫn tệp OUTLINE.md")
    parser.add_argument("--tolerance", type=float, default=0.10, help="Dung sai từ cho từng Part (mặc định 0.10 = ±10%)")
    parser.add_argument("--total_tolerance", type=float, default=0.05, help="Dung sai từ cho toàn bài (mặc định 0.05 = ±5%)")
    parser.add_argument("--wpm", type=int, default=150, help="Tốc độ đọc WPM để ước lượng (mặc định 150 WPM)")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    slop_dict = load_slop_dictionary(script_dir)

    target_path = Path(args.target).resolve()
    outline_path = Path(args.outline).resolve() if args.outline else find_outline_in_context(target_path)
    targets_from_outline = extract_part_targets_from_outline(outline_path, default_wpm=args.wpm) if outline_path else {}

    # Xác định tệp cần kiểm tra
    if args.part:
        part_p = Path(args.part)
        if not part_p.exists():
            part_p = target_path / args.part
        if not part_p.exists():
            print(f"[!] LỖI: Không tìm thấy tệp Part chỉ định: {args.part}", file=sys.stderr)
            sys.exit(1)
        files_to_check = [part_p]
    else:
        files_to_check = locate_script_files(target_path)

    if not files_to_check:
        print(f"[!] LỖI: Không tìm thấy bất kỳ tệp part-*.txt nào tại: {target_path}", file=sys.stderr)
        sys.exit(1)

    print("=" * 80)
    print("🔍 TẦNG 1: SCRIPT STATIC LINTER (KIỂM ĐỊNH KỸ THUẬT CỨNG)")
    print(f"• Thư mục kiểm tra: {target_path}")
    print(f"• Tệp Outline: {outline_path if outline_path else '[Không tìm thấy OUTLINE.md - Bỏ qua check ngân sách từ]'}")
    print(f"• Số lượng tệp Part: {len(files_to_check)}")
    print(f"• Ngưỡng dung sai: Từng Part ±{int(args.tolerance*100)}% | Toàn bài ±{int(args.total_tolerance*100)}%")
    print("=" * 80)

    total_article_words = 0
    total_target_words = 0
    all_results = []
    has_hard_error = False

    for fp in files_to_check:
        p_num = extract_part_number_from_filename(fp.name)
        target_w = targets_from_outline.get(p_num) if p_num else None
        if target_w:
            total_target_words += target_w

        res = lint_part_file(fp, target_words=target_w, tolerance_part=args.tolerance, slop_dict=slop_dict)
        all_results.append(res)
        total_article_words += res["total_words"]

        if res["hard_errors"]:
            has_hard_error = True

    # In kết quả theo từng Part
    for res in all_results:
        fn = res["filename"]
        act_w = res["total_words"]
        tgt_w = res["target_words"]
        err_pct = res["word_budget_error_pct"]
        is_pass = len(res["hard_errors"]) == 0

        status_tag = "✅ PASS" if is_pass else "❌ FAIL"
        tgt_str = f"{tgt_w} từ ({err_pct:+.1f}%)" if tgt_w else "N/A"

        print(f"\n📄 [{status_tag}] {fn}: {act_w} từ (Mục tiêu: {tgt_str}) | {res['total_lines']} dòng thoại")

        if res["hard_errors"]:
            print("   ⛔ LỖI CỨNG (BẮT BUỘC SỬA):")
            for err in res["hard_errors"]:
                print(f"      • {err}")

        if res["warnings"]:
            print("   ⚠️ CẢNH BÁO NHẸ:")
            for w in res["warnings"]:
                print(f"      • {w}")

    # Kiểm tra ngân sách tổng toàn bài (nếu kiểm định từ 2 Part trở lên và có Outline)
    print("\n" + "-" * 80)
    print("📊 TỔNG KẾT TOÀN TẬP:")
    print(f"• Tổng số từ thực tế: {total_article_words} từ")
    if total_target_words > 0:
        total_diff = total_article_words - total_target_words
        total_err_pct = (total_diff / total_target_words) * 100.0
        min_tot = int(total_target_words * (1.0 - args.total_tolerance))
        max_tot = int(total_target_words * (1.0 + args.total_tolerance))
        tot_pass = min_tot <= total_article_words <= max_tot

        print(f"• Tổng số từ mục tiêu: {total_target_words} từ (Khoảng chuẩn ±{int(args.total_tolerance*100)}%: {min_tot} – {max_tot} từ)")
        print(f"• Sai số toàn bài: {total_err_pct:+.1f}% ➔ {'✅ ĐẠT' if tot_pass else '❌ VƯỢT NGƯỠNG'}")

        if not tot_pass and len(files_to_check) > 1:
            has_hard_error = True
            print(f"[!] LỖI CỨNG: Tổng số từ toàn bài lệch {total_err_pct:+.1f}%, vượt trần cho phép ±{int(args.total_tolerance*100)}%")

    print("=" * 80)

    if has_hard_error:
        print("⛔ KẾT QUẢ TẦNG 1: THẤT BẠI (EXIT CODE 1)")
        print("Biên kịch/Agent hãy sửa trực tiếp các lỗi dòng ở trên, KHÔNG gọi LLM Tầng 2 khi chưa đạt.")
        sys.exit(1)
    else:
        print("🔒 KẾT QUẢ TẦNG 1: THÀNH CÔNG RỰC RỠ (EXIT CODE 0)")
        print("Tất cả tệp Part đã vượt qua rào cản kỹ thuật. Sẵn sàng chuyển tiếp sang TẦNG 2 (DUAL QA PEER REVIEW).")
        sys.exit(0)


if __name__ == "__main__":
    main()
