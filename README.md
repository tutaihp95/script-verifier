# 🎙️ Script Verifier Skill (`script-verifier`)

> **Hệ thống Kiểm định Kịch bản Chi tiết Đa kênh (Part-by-Part) theo Mô hình Hybrid 2 Tầng (Static Python Linter + Dual QA Double-Blind Peer Review)**  
> Tuân thủ chuẩn Master SSOT: `UNIVERSAL_SCRIPT_VERIFICATION_PLAYBOOK.md`

---

## 🏛️ Tổng quan Kiến trúc

```
                 [Tệp Part trong 01_script/: part-1.txt, part-2.txt, ...]
                                                │
                                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TẦNG 1: SCRIPT STATIC LINTER (Script Python - 0 Token, < 0.2 Giây)                     │
│ • Kiểm tra ngân sách từ theo từng Part (±10%) và tổng bài (±5%) đối chiếu OUTLINE.md    │
│ • Rào cản TTS an toàn: Dòng mục tiêu < 115 ký tự (trần cứng tối đa <= 150 ký tự)       │
│ • Chuẩn hóa số 100%: 0 chữ số 0-9, 0 ký tự $, %, 0 markdown, 0 nhãn ngắt nghỉ lạ       │
│ • Bộ lọc từ rác AI: Sạch hoàn toàn từ sáo rỗng EN & VI; triệt tiêu lối viết nhị phân   │
└───────────────────────────────────────┬────────────────────────────────────────────────┘
                                        │ PASS (Exit Code 0)
                                        ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TẦNG 2: THẨM ĐỊNH ĐỐI CHỨNG SONG SONG MÙ ĐÔI (DOUBLE-BLIND PEER REVIEW)                │
│ Cả 2 Agent QA cùng thẩm định độc lập từng Part theo Bộ Master Rubric 15 Tiêu chuẩn:    │
│ • Nhóm 1: Âm học & Văn nói (S-01 ➔ S-02)                                               │
│ • Nhóm 2: Giữ chân & SEO YouTube (S-03 ➔ S-08)                                         │
│ • Nhóm 3: Dữ liệu Định lượng & Bảo toàn Thuật ngữ [Term] (S-09 ➔ S-10)                 │
│ • Nhóm 4: Kỹ thuật TTS & Đa Part (S-11 ➔ S-13)                                         │
│ • Nhóm 5: Chống Rác AI & Mật độ Thông tin (S-14 ➔ S-15)                                │
└───────────────────────────────────────┬────────────────────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ CỔNG NGHIỆM THU: BẢNG ĐỐI CHIẾU CHÉO (SCRIPT_AUDIT_REPORT.md)                          │
│ • CẢ 2 CÙNG PASS (15/15)       ➔ 🔒 ĐÓNG BĂNG PART (LOCKED - PASS)                    │
│ • CÓ BẤT ĐỒNG (1 PASS, 1 FAIL) ➔ 🛠️ SỬA CHI TIẾT THEO BÊN FAIL                        │
│ • CẢ 2 CÙNG FAIL (2 FAIL)      ➔ ⛔ XÓA VÀ VIẾT LẠI MỚI ĐOẠN SAI THEO OUTLINE           │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Cấu trúc Thư mục

```text
script-verifier/
├── SKILL.md                          # Điều phối luồng, lệnh kích hoạt (/verify-script, /verify-part)
├── README.md                         # Hướng dẫn tổng quan & mô tả kỹ thuật
├── .gitignore                        # Cấu hình bỏ qua tệp tạm
├── scripts/
│   └── check_script_structure.py     # Script Python linter Tầng 1 (0 token, regex, WPM, line length)
├── references/
│   ├── master_rubric_15.md           # 15 Tiêu chuẩn chi tiết S-01 -> S-15 trích xuất từ Playbook
│   └── audit_report_template.md      # Biểu mẫu chuẩn xuất file SCRIPT_AUDIT_REPORT.md
└── resources/
    └── ai_slop_dictionary.json       # Danh mục từ rác AI song ngữ EN & VI + regex cấu trúc nhị phân
```

---

## 🚀 Hướng dẫn Sử dụng

### 1. Chạy Linter Tầng 1 (Offline, 0 Token)

```bash
# Kiểm định 1 file Part cụ thể:
python scripts/check_script_structure.py --part 01_script/part-1.txt --outline OUTLINE.md

# Kiểm định toàn bộ thư mục tập phim:
python scripts/check_script_structure.py 02_PRODUCTION/vid_01/
```

### 2. Sử dụng qua Agent / AI Coding Assistant

Trong môi trường hỗ trợ Agentic Custom Skills (như Antigravity IDE, Claude Code, Cursor):

* **Verify 1 Part:**
  > *"Verify part 1 cho vid_01"* hoặc *"/verify-part part-1.txt"*
* **Verify toàn bộ tập phim:**
  > *"Verify kịch bản cho vid_01"* hoặc *"/verify-script 02_PRODUCTION/vid_01"*

---

## 📄 Bản quyền & Đóng góp
Phát triển cho hệ thống sản xuất nội dung YouTube tự động hóa tiêu chuẩn cao (High-Retention Video Production Pipeline).
