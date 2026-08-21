# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

<!--
HƯỚNG DẪN - đọc rồi XÓA TOÀN BỘ các khối chú thích này sau khi điền xong:

  - Giới hạn: KHÔNG QUÁ 1 TRANG A4, tương đương khoảng 450 - 550 từ nội dung.
  - Chỉ điền vào các chỗ ___ và các ô trong bảng. Không thêm mục mới.
  - Viết bằng câu hoàn chỉnh, không gạch đầu dòng cụt lủn.
  - Kiểm tra độ dài sau khi đã xóa hết chú thích:
        wc -w nop-bai/bao-cao.md
    và xem trước bản in bằng cách mở file trên GitHub rồi Ctrl+P / Cmd+P.
-->

| | |
|---|---|
| Họ và tên | ___ |
| MSSV | ___ |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/___/___ |
| Ngày nộp | ___ |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

<!-- Khoảng 120 - 150 từ. Điền kết quả thật từ MLflow UI ở Bước 1, tối thiểu 3 lần chạy. -->

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.8740 |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

**Lý do:** Bộ siêu tham số này đạt điểm `f1_score` cao nhất (0.7149), vượt qua ngưỡng chất lượng tối thiểu 0.65 của bài toán phân loại mất cân bằng lớp. So với lần chạy 1 có accuracy cao nhất (0.8780), lần chạy 3 chấp nhận đánh đổi một phần nhỏ accuracy tổng thể để tăng khả năng phát hiện đúng các trường hợp thuộc lớp thiểu số (thu nhập > 50K). Khi tăng `n_estimators` từ 50 lên 200 kết hợp với `max_depth=5`, mô hình Gradient Boosting có đủ độ sâu và số lượng cây để học các mẫu dữ liệu phức tạp hơn mà không bị underfitting.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tập dữ liệu Adult có phân bố lớp mất cân bằng nghiêm trọng khi chỉ có khoảng 24.8% mẫu thuộc lớp thu nhập cao (>50K USD). Trong tình huống này, một mô hình suy đoán ngây thơ (naive model) luôn trả về kết quả "thu nhập thấp" cho mọi cá nhân vẫn sẽ đạt chỉ số Accuracy lên tới 75.2%. Tuy nhiên, mô hình đó hoàn toàn vô dụng trên thực tế vì không phát hiện được bất kỳ đối tượng mục tiêu nào ($F_1 = 0$).

Chỉ số F1-Score trên lớp dương (thu nhập > 50K) là trung bình điều hòa giữa Precision và Recall, phản ánh chính xác khả năng mô hình vừa phân loại đúng đối tượng mục tiêu vừa hạn chế cảnh báo sai. Lab không sử dụng `average="weighted"` hay `average="macro"` vì các cách tính này bị kéo lên cao bởi lớp đa số (75.2%), làm mất đi ý nghĩa thực sự của ngưỡng kiểm thử chất lượng trong pipeline CI/CD.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

<!-- Nêu 2 - 3 khó khăn thật, mỗi ô một câu ngắn. -->

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| ___ | ___ | ___ |
| ___ | ___ | ___ |
| ___ | ___ | ___ |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

<!-- Lấy số liệu từ bảng ở mục 3.6 của tasks/buoc-3.md. -->

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | ___ | ___ |
| Bước 3 (thêm `train_batch2`) | ___ | ___ |

**Nhận xét:** ___

<!--
Một câu trả lời trung thực kiểu "f1 giảm 0,01 vì dữ liệu mới cùng phân phối, không mang
thêm thông tin mới" được đánh giá cao hơn kết luận sai rằng thêm dữ liệu luôn tốt hơn.
-->

---

## 5. Phần Bonus Đã Thực Hiện (nếu có)

<!-- Xóa cả mục 5 nếu không làm bonus. Mỗi bonus tối đa 1 dòng. -->

- [ ] Bonus 1 - Tracking MLflow từ xa với DagsHub: ___
- [ ] Bonus 2 - Điều chỉnh ngưỡng quyết định: ___
- [ ] Bonus 3 - Báo cáo precision / recall tự động: ___
- [ ] Bonus 4 - Hoàn trả về phiên bản trước: ___
- [ ] Bonus 5 - Cảnh báo lệch lạc dữ liệu: ___
