# 📋 BIÊN BẢN KIỂM ĐỊNH KỊCH BẢN CHI TIẾT: {{EPISODE_TITLE}}
- **Kênh:** {{CHANNEL_NAME}} | **Hồ sơ tham chiếu:** {{PROFILE_FILE}}
- **Thư mục kiểm toán:** `01_script/` (Gồm {{TOTAL_PARTS}} tệp Part: part-1.txt ➔ part-{{TOTAL_PARTS}}.txt)
- **Mã hồ sơ kiểm toán:** AUDIT-{{EPISODE_ID}}-SCRIPT-DOUBLE-BLIND
- **Thời gian thực hiện:** {{TIMESTAMP}}
- **Kết quả Tầng 1 (Static Linter):** {{TIER_1_STATUS}} (Exit Code 0 | Tổng từ: {{TOTAL_WORDS}} từ | 100% câu <= 150 kt | 0 Chữ số 0-9 | 0 Từ rác AI)
- **Kết quả Tầng 2 (Dual-Auditor Consensus):** {{TIER_2_STATUS}}

---

## 🔒 BẢNG TRẠNG THÁI PHÂN ĐỊNH TỪNG PART (PART-BY-PART ISOLATION MATRIX):

| Tệp tin | Số từ thực tế | Mục tiêu Outline | Ngưỡng chuẩn (±10%) | Kết quả Tầng 1 | Đánh giá Tầng 2 | Phán quyết Part | Hành động yêu cầu |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `part-1.txt` | {{P1_ACTUAL}} từ | {{P1_TARGET}} từ | {{P1_MIN}} – {{P1_MAX}} từ | PASS | PASS | 🔒 LOCKED (PASS) | Đóng băng vĩnh viễn (Đã nghiệm thu) |
| `part-2.txt` | {{P2_ACTUAL}} từ | {{P2_TARGET}} từ | {{P2_MIN}} – {{P2_MAX}} từ | PASS | PASS | 🔒 LOCKED (PASS) | Đóng băng vĩnh viễn (Đã nghiệm thu) |
| `part-3.txt` | {{P3_ACTUAL}} từ | {{P3_TARGET}} từ | {{P3_MIN}} – {{P3_MAX}} từ | {{P3_T1}} | {{P3_T2}} | {{P3_VERDICT}} | {{P3_ACTION}} |

---

## ⚖️ BẢNG ĐỐI CHIẾU CHÉO 15 TIÊU CHUẨN RUBRIC (PEER REVIEW CONSENSUS MATRIX):

| Mã TC | Tiêu Chuẩn Thẩm Định | Tệp Áp dụng | Đánh giá QA 1 | Đánh giá QA 2 | So Khớp Đồng Thuận | Dẫn chứng Trích lục / Phân tích Chuyên môn |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **S-01** | Khí chất Persona & Định vị Kênh | Toàn bộ Part | PASS | PASS | **✅ ĐỒNG THUẬN (PASS)** | Lời thoại thể hiện đúng vị thế đồng minh, cấm giáo điều. |
| **S-02** | Nhịp thở & Single-Breath Unit | Toàn bộ Part | PASS | PASS | **✅ ĐỒNG THUẬN (PASS)** | 100% vế câu < 20 từ, câu ngắn đanh thép kết hợp câu giải thích. |
| **S-03** | Mỏ neo 0:00 & Spoken SEO (2 lần/30s) | **Part 1** | PASS | PASS | **✅ ĐỒNG THUẬN (PASS)** | Part 1 mở màn đúng mỏ neo thumbnail; Focus Keyword lặp lại 2 lần trong 30s đầu. |
| **S-04** | Cú sốc Nhận thức Mở đầu (30-45s) | **Part 1** | PASS | PASS | **✅ ĐỒNG THUẬN (PASS)** | Đập vỡ định kiến thông thường trong 30-45s đầu, không chào hỏi vòng vo. |
| **S-05** | Curiosity Bridges & Rehooks Đa Part | Toàn bộ Part | PASS | PASS | **✅ ĐỒNG THUẬN (PASS)** | Dòng cuối mỗi Part có rehook mở vòng lặp tò mò Zeigarnik. |
| **S-06** | Khung Save Trigger Đúng Mốc Vàng | Part quy định | [N/A] | [N/A] | **✅ ĐỒNG THUẬN [N/A]** | Xuất hiện đúng mốc thời gian vàng theo Outline. |
| **S-07** | Điểm chạm & Viewer Stakes Sát sườn | Toàn bộ Part | PASS | PASS | **✅ ĐỒNG THUẬN (PASS)** | Kéo kiến thức về tác động ví tiền hoặc trải nghiệm sát sườn. |
| **S-08** | Kết bài Dứt khoát (Cold Punchline) | **Part cuối** | [N/A] | [N/A] | **✅ ĐỒNG THUẬN [N/A]** | Câu chốt đanh thép, 0 câu cảm ơn hay chào tạm biệt rườm rà. |
| **S-09** | Bóc tách Số liệu & Bằng chứng Thực tế | Toàn bộ Part | PASS | PASS | **✅ ĐỒNG THUẬN (PASS)** | 100% số liệu đối chiếu nguồn thẩm quyền, không bịa đặt số liệu. |
| **S-10** | Ẩn dụ Trực quan & Bảo toàn `[Term]` | Toàn bộ Part | PASS | PASS | **✅ ĐỒNG THUẬN (PASS)** | Có hình ảnh so sánh đời thường; bảo toàn nguyên vẹn 100% `[Term]`. |
| **S-11** | Độ dài Dòng (< 115 kt) & Ngân sách từ | Toàn bộ Part | PASS | PASS | **✅ ĐỒNG THUẬN (PASS)** | 100% dòng <= 150 kt (mục tiêu < 115 kt); ngân sách từ Part trong ngưỡng ±10%. |
| **S-12** | Chuẩn hóa Văn bản TTS 100% | Toàn bộ Part | PASS | PASS | **✅ ĐỒNG THUẬN (PASS)** | 0 chữ số 0-9, đổi tiền tệ/phần trăm sang chữ, 0 markdown, 0 nhãn lạ. |
| **S-13** | Đồng bộ Cấu trúc Đa Part (Parity) | Toàn bộ Part | PASS | PASS | **✅ ĐỒNG THUẬN (PASS)** | Đủ số lượng Part theo Outline, ranh giới rõ ràng, không trùng lặp. |
| **S-14** | Sạch Hoàn toàn Từ Rác AI | Toàn bộ Part | PASS | PASS | **✅ ĐỒNG THUẬN (PASS)** | Sạch hoàn toàn từ rác EN & VI (delve, tapestry, landscape, vén màn...). |
| **S-15** | Triệt tiêu Lối viết Nhị phân & Mật độ | Toàn bộ Part | PASS | PASS | **✅ ĐỒNG THUẬN (PASS)** | Cấm cấu trúc nhị phân "Not because X, but Y"; mật độ thông tin cao. |

---

## 🏆 PHÁN QUYẾT CHUNG CUỘC: {{FINAL_VERDICT}}
- **Đóng mộc chứng nhận:** **`STATUS: {{CONTRACT_STATUS}}`**
- **Danh sách Part đã khóa băng (Locked):** {{LOCKED_PARTS_LIST}}
- **Chỉ định sửa lỗi cục bộ (nếu có vi phạm):** {{SURGICAL_INSTRUCTIONS}}
- **Cấp phép chuyển giao:** {{TRANSFER_PERMISSION}}
