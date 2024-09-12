import pyodbc
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Hàm kết nối đến CSDL
def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=thptqg24;'
            'UID=sa;'
            'PWD=123456aA@$'
        )
        return conn
    except pyodbc.Error as e:
        print("Lỗi kết nối CSDL:", e)
        return None

# Hàm định dạng điểm số
def format_score(score):
    if score is None:
        return None
    try:
        score = float(score)
        # Nếu điểm lớn hơn 100, chia cho 100
        if score > 100:
            return f"{score / 100:.2f}"
        # Nếu điểm từ 10 đến 100, chia cho 10
        elif score >= 10:
            return f"{score / 10:.2f}"
        # Nếu điểm nhỏ hơn 10, giữ nguyên
        else:
            return f"{score:.2f}"
    except (ValueError, TypeError):
        print(f"Giá trị điểm không hợp lệ: {score}")
        return None

@app.route('/')
def index():
    return render_template('index.html', error="", sbd="")

# Hàm tính điểm khối thi
def calculate_block_scores(points):
    block_scores = {}

    # Khối A: Toán, Vật Lý, Hóa Học
    if all(points.get(subject) is not None for subject in ["Toán", "Vật Lý", "Hóa Học"]):
        block_scores["Khối A"] = (
            float(points["Toán"]) +
            float(points["Vật Lý"]) +
            float(points["Hóa Học"])
        )

    # Khối A1: Toán, Vật Lý, Ngoại Ngữ
    if all(points.get(subject) is not None for subject in ["Toán", "Vật Lý", "Ngoại Ngữ"]):
        block_scores["Khối A1"] = (
            float(points["Toán"]) +
            float(points["Vật Lý"]) +
            float(points["Ngoại Ngữ"])
        )

    # Khối B: Toán, Hóa Học, Sinh Học
    if all(points.get(subject) is not None for subject in ["Toán", "Hóa Học", "Sinh Học"]):
        block_scores["Khối B"] = (
            float(points["Toán"]) +
            float(points["Hóa Học"]) +
            float(points["Sinh Học"])
        )

    # Khối C: Ngữ Văn, Lịch Sử, Địa Lý
    if all(points.get(subject) is not None for subject in ["Ngữ Văn", "Lịch Sử", "Địa Lý"]):
        block_scores["Khối C"] = (
            float(points["Ngữ Văn"]) +
            float(points["Lịch Sử"]) +
            float(points["Địa Lý"])
        )

    # Khối D: Toán, Ngữ Văn, Ngoại Ngữ
    if all(points.get(subject) is not None for subject in ["Toán", "Ngữ Văn", "Ngoại Ngữ"]):
        block_scores["Khối D"] = (
            float(points["Toán"]) +
            float(points["Ngữ Văn"]) +
            float(points["Ngoại Ngữ"])
        )

    # Khối D1: Toán, Ngữ Văn, Ngoại Ngữ (chọn Tiếng Anh)
    if all(points.get(subject) is not None for subject in ["Toán", "Ngữ Văn", "Ngoại Ngữ"]):
        block_scores["Khối D1"] = (
            float(points["Toán"]) +
            float(points["Ngữ Văn"]) +
            float(points["Ngoại Ngữ"])
        )

    # Khối D7: Toán, Hóa Học, Ngoại Ngữ
    if all(points.get(subject) is not None for subject in ["Toán", "Hóa Học", "Ngoại Ngữ"]):
        block_scores["Khối D7"] = (
            float(points["Toán"]) +
            float(points["Hóa Học"]) +
            float(points["Ngoại Ngữ"])
        )

    # Khối C1: Ngữ Văn, Toán, Vật Lý
    if all(points.get(subject) is not None for subject in ["Ngữ Văn", "Toán", "Vật Lý"]):
        block_scores["Khối C1"] = (
            float(points["Ngữ Văn"]) +
            float(points["Toán"]) +
            float(points["Vật Lý"])
        )

    # Khối B2: Toán, Sinh Học, Địa Lý
    if all(points.get(subject) is not None for subject in ["Toán", "Sinh Học", "Địa Lý"]):
        block_scores["Khối B2"] = (
            float(points["Toán"]) +
            float(points["Sinh Học"]) +
            float(points["Địa Lý"])
        )

    return block_scores

@app.route('/search', methods=['GET'])
def search():
    sbd = request.args.get('sbd').strip()
    if not sbd:
        return redirect(url_for('index'))

    conn = get_db_connection()
    if not conn:
        return render_template('index.html', error="Lỗi kết nối cơ sở dữ liệu")

    cursor = conn.cursor()

    # Truy vấn SQL để lấy tất cả các điểm cho SBD
    cursor.execute("SELECT * FROM diem_thi_1 WHERE sbd = ?", (sbd,))
    result = cursor.fetchone()
    conn.close()

    if result:
        sbd_value = result[0]  # Lấy giá trị SBD

        # Xử lý các điểm và loại bỏ các giá trị NULL
        points = {
            "Toán": format_score(result[1]),
            "Ngữ Văn": format_score(result[2]),
            "Ngoại Ngữ": format_score(result[3]),
            "Vật Lý": format_score(result[4]),
            "Hóa Học": format_score(result[5]),
            "Sinh Học": format_score(result[6]),
            "Lịch Sử": format_score(result[7]),
            "Địa Lý": format_score(result[8]),
            "GDCD": format_score(result[9])
        }

        # Lọc điểm không phải là NULL
        points = {subject: score for subject, score in points.items() if score is not None}

        # Tính điểm cho các khối thi
        block_scores = calculate_block_scores(points)

        return render_template('result.html', sbd=sbd_value, points=points, block_scores=block_scores, error="")
    else:
        return render_template('index.html', error="Không có dữ liệu cho Số Báo Danh này.")

if __name__ == '__main__':
    app.run(debug=True)
