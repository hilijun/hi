from flask import Flask, send_from_directory, jsonify, request
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)

# 桌面路径
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# ========== 网页路由 ==========

@app.route('/')
def index():
    """访问 http://localhost:5000/ 时显示您的网页"""
    # 如果您的 index.html 在桌面
    return send_from_directory(desktop, 'index.html')

@app.route('/index.html')
def serve_html():
    """也可以直接访问 index.html"""
    return send_from_directory(desktop, 'index.html')

# ========== API路由 ==========

@app.route('/api/live')
def get_live_data():
    """从远程API实时获取最新数据"""
    try:
        url = "https://pc28.help/api/keno.json?nbr=1"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"请求失败，状态码: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/local')
def get_local_data():
    """读取本地JSON文件中的数据"""
    try:
        filepath = os.path.join(desktop, 'keno_data.json')
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify({
                "source": "local_file",
                "update_time": datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d %H:%M:%S"),
                "data": data
            })
        else:
            return jsonify({"error": "本地数据文件不存在"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/keno_data.json')
def serve_json():
    """直接提供JSON文件"""
    try:
        return send_from_directory(desktop, 'keno_data.json')
    except:
        return jsonify({"error": "文件不存在"}), 404

# ========== 启动服务 ==========

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 服务器已启动")
    print(f"📁 网页目录: {desktop}")
    print(f"📍 访问地址: http://localhost:5000")
    print("=" * 50)
    print("按 Ctrl+C 停止服务")
    app.run(host='0.0.0.0', port=5000, debug=False)