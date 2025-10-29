from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 实验要求：原始商品集合（含核心属性）
raw_products = [
    {"id": 1, "name": "冰箱", "category": "家电", "price": 2999, "free_shipping": True},
    {"id": 2, "name": "耳机", "category": "家电", "price": 199, "free_shipping": True},
    {"id": 3, "name": "T恤", "category": "服装", "price": 99, "free_shipping": False},
    {"id": 4, "name": "饼干", "category": "食品", "price": 29, "free_shipping": True},
    {"id": 5, "name": "连衣裙", "category": "服装", "price": 399, "free_shipping": False},
    {"id": 6, "name": "坚果礼盒", "category": "食品", "price": 159, "free_shipping": True},
    {"id": 7, "name": "洗衣机", "category": "家电", "price": 1999, "free_shipping": True},
    {"id": 8, "name": "牛仔裤", "category": "服装", "price": 259, "free_shipping": False},
    {"id": 9, "name": "面包", "category": "食品", "price": 15, "free_shipping": True},
    {"id": 10, "name": "微波炉", "category": "家电", "price": 699, "free_shipping": True}
]

# 实验核心：构建筛选维度集合（用于交集运算）
def get_condition_sets():
    return {
        "category": {  # 类别集合
            "家电": {p["id"] for p in raw_products if p["category"] == "家电"},
            "服装": {p["id"] for p in raw_products if p["category"] == "服装"},
            "食品": {p["id"] for p in raw_products if p["category"] == "食品"}
        },
        "price": {     # 价格区间集合
            "0-100元": {p["id"] for p in raw_products if 0 <= p["price"] < 100},
            "100-500元": {p["id"] for p in raw_products if 100 <= p["price"] < 500},
            "500元以上": {p["id"] for p in raw_products if p["price"] >= 500}
        },
        "shipping": {  # 包邮集合
            "是": {p["id"] for p in raw_products if p["free_shipping"]},
            "否": {p["id"] for p in raw_products if not p["free_shipping"]}
        }
    }

# 1. 首页：展示筛选页面
@app.route("/")
def index():
    return render_template("index.html", raw_products=raw_products)

# 2. 筛选接口（实验核心：集合交集运算）
@app.route("/filter", methods=["POST"])
def filter_products():
    data = request.json
    # 获取选中条件对应的集合
    sets = get_condition_sets()
    matched_ids = (sets["category"][data["category"]] &
                   sets["price"][data["price"]] &
                   sets["shipping"][data["shipping"]])
    # 筛选商品并生成集合表达式
    matched_products = [p for p in raw_products if p["id"] in matched_ids]
    expression = f"{data['category']}集合 ∩ {data['price']}集合 ∩ 包邮{data['shipping']}集合"
    return jsonify({
        "expression": expression,
        "products": matched_products,
        "matched_count": len(matched_products),
        "total_count": len(raw_products)
    })

# 3. 可视化数据接口（仅提供实验必需的统计数据）
@app.route("/statistics", methods=["GET"])
def get_statistics():
    sets = get_condition_sets()
    return jsonify({
        "category_count": {k: len(v) for k, v in sets["category"].items()},
        "price_count": {k: len(v) for k, v in sets["price"].items()},
        "total_count": len(raw_products)
    })

if __name__ == "__main__":
    app.run(debug=True)