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
| Họ và tên | Trần Tuấn Đạt |
| MSSV | VinUni-K4-AI |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/jimm9Tran/K4-Track2-Day21-CI-CD-for-AI-Systems |
| Ngày nộp | 21/08/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

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

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| Không unpickle được mô hình khi deploy trên Cloud VM | Phiên bản scikit-learn trên VM mặc định cài bản mới nhất (1.7.2), không tương thích với artifact được train ở bản 1.4.2 | Ghim cố định và cài đặt đúng phiên bản `scikit-learn==1.4.2` đồng nhất trên Cloud VM |
| Lỗi xác thực GCP khi DVC pull trong GitHub Actions | DVC đọc credentialpath từ cấu hình `.dvc/config` không khớp với đường dẫn tạm của runner | Ghi đồng thời secret `STORAGE_CREDENTIALS` ra cả `sa-key.json` gốc và `/tmp/sa-key.json` |

---

## 4. So Sánh Bước 2 và Bước 3

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | 0.7149 | 0.8740 |
| Bước 3 (thêm `train_batch2`) | 0.7354 | 0.8820 |

**Nhận xét:** Khi bổ sung thêm 22.361 mẫu từ `train_batch2` (tổng cộng 44.722 mẫu), điểm F1-score của mô hình tăng từ 0.7149 lên 0.7354 và Accuracy tăng nhẹ từ 0.8740 lên 0.8820. Quan trọng nhất là toàn bộ quy trình huấn luyện lại, kiểm tra ngưỡng chất lượng và triển khai phiên bản mô hình mới lên API phục vụ suy luận đã diễn ra hoàn toàn tự động thông qua pipeline Continuous Training (CT) mà không cần bất kỳ can thiệp thủ công nào.
