# 沉浸式动物微观剧场 部署指南

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量（.env文件）
SILICONFLOW_API_KEY=你的API密钥

# 启动服务
python main.py
```

访问：http://localhost:8000

---

## 部署到 Render（免费）

### 步骤 1：上传到 GitHub

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "初始化动物剧场项目"

# 关联远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/animal-theater-pro.git

# 推送到 GitHub
git push -u origin main
```

### 步骤 2：在 Render 上创建 Web Service

1. 访问：https://render.com
2. 注册/登录账号
3. 点击 **"New +"** → **"Web Service"**
4. **连接 GitHub 仓库**：选择刚创建的仓库
5. **配置服务**：

|配置项|值|
|---|---|
|Name| animal-theater |
|Environment| Python 3 |
|Build Command| `pip install -r requirements.txt` |
|Start Command| `uvicorn main:app --host 0.0.0.0 --port $PORT` |

6. **添加环境变量**：

点击 **"Advanced"** → **"Environment Variables"**，添加：

|Key|Value|
|---|---|
|`SILICONFLOW_API_KEY`|你的SiliconFlow API密钥|

7. 点击 **"Create Web Service"** 部署

### 步骤 3：获取公网访问地址

部署完成后（约2-5分钟），Render会提供一个公网URL，例如：

```
https://animal-theater.onrender.com
```

任何人都可以通过这个链接访问你的动物剧场！

---

## 部署到其他平台（可选）

### Vercel

安装 Vercel CLI 并部署：

```bash
npm install -g vercel
vercel
```

### Railway

访问：https://railway.app
直接导入 GitHub 仓库即可

---

## 常见问题

**Q: 部署后音频无法播放？**
A: Render 免费版有冷启动问题，首次访问需要等待30秒左右。

**Q: 如何更换API密钥？**
A: 在 Render 控制台的 Settings → Environment Variables 中重新设置。

**Q: 如何修改动物库？**
A: 编辑 `main.py` 中的 `ANIMAL_DATABASE` 数组，然后重新部署。

---

## 项目结构

```
animal_theater_pro/
├── main.py              # FastAPI 后端
├── requirements.txt     # Python 依赖
├── Procfile            # Render 部署配置
├── .env                # 本地环境变量（不上传）
├── .gitignore          # Git 忽略文件
└── frontend/
    └── theater.html    # 前端页面
```

祝你部署成功！🚀
