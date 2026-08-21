import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
import json
import joblib
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score

# Nguong chat luong cua lab nay la f1_score, KHONG phai accuracy.
# Ly do: bo du lieu Adult co ty le lop 75/25. Mot mo hinh doan bua
# "thu nhap thap" cho moi mau da dat accuracy 0.75 ma khong hoc duoc gi.
F1_THRESHOLD = 0.65

if "MLFLOW_TRACKING_URI" not in os.environ:
    mlflow.set_tracking_uri("sqlite:///mlflow.db")


def train(
    params: dict,
    data_path: str = "data/train_batch1.csv",
    eval_path: str = "data/holdout.csv",
) -> float:
    """
    Huan luyen mo hinh va ghi nhan ket qua vao MLflow.

    Tham so:
        params     : dict chua cac sieu tham so cho GradientBoostingClassifier.
        data_path  : duong dan den file du lieu huan luyen.
        eval_path  : duong dan den file du lieu danh gia (holdout).

    Tra ve:
        f1 (float): diem F1 cua lop duong (thu nhap > 50K) tren tap holdout.
    """

    # 1. Đọc dữ liệu huấn luyện và đánh giá
    df_train = pd.read_csv(data_path)
    df_eval = pd.read_csv(eval_path)

    # 2. Tách đặc trưng (X) và nhãn (y)
    X_train = df_train.drop(columns=["target"])
    y_train = df_train["target"]
    X_eval = df_eval.drop(columns=["target"])
    y_eval = df_eval["target"]

    with mlflow.start_run():

        # 3. Ghi nhận các siêu tham số vào MLflow
        mlflow.log_params(params)

        # 4. Khởi tạo và huấn luyện GradientBoostingClassifier
        # Sử dụng random_state=42 để đảm bảo tính tái tạo
        model = GradientBoostingClassifier(**params, random_state=42)
        model.fit(X_train, y_train)

        # 5. Dự đoán trên tập holdout và tính chỉ số
        # Chú ý: f1_score ở đây tính cho LỚP DƯƠNG (target = 1), không dùng average
        preds = model.predict(X_eval)
        f1 = float(f1_score(y_eval, preds))
        acc = float(accuracy_score(y_eval, preds))

        # 6. Ghi nhận chỉ số và log model vào MLflow
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, "model")

        # 7. In kết quả ra màn hình
        print(f"F1: {f1:.4f} | Accuracy: {acc:.4f}")

        # 8. Lưu metrics ra file outputs/report.json (để GitHub Actions đọc ở Bước 2)
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/report.json", "w") as f:
            json.dump({"f1_score": f1, "accuracy": acc}, f)

        # 9. Lưu mô hình ra file models/model.joblib (để upload lên Cloud Storage ở Bước 2)
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.joblib")

    # 10. Trả về f1
    return f1


if __name__ == "__main__":
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    train(params)
