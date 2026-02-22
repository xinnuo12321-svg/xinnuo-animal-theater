# 🌲 沉浸式动物微观剧场

一款专为3-5岁幼儿和美术老师打造的沉浸式动物科普H5应用，融合真实野外动物叫声、高清精美动物图片和AI温柔科普。

## ✨ 核心特色

- **真实野外声音** - 智能调用 Xeno-canto API，获取真实野外动物录音（备有 Wikimedia CC0 音频）
- **精选用图** - 10种精选动物，精选Unsplash高清美图
- **AI温柔科普** - DeepSeek V3 生成50字内幼儿友好科普文案
- **沉浸式UI** - 移动端优先的高级深色设计，完美适配手机竖屏
- **零成本部署** - 可一键部署至 Render 免费，支持公网访问
- **国内直访优化** - 通过 Render 代理服务器下载资源，国内用户无需梯子即可流畅使用

## 📜 版权声明

本项目使用的所有音视频资源均来自**免费可商用的公开来源**，包括：
- **图片**：Unsplash License（免费商用，无需署名）
- **音频**：WikiMedia Commons CC0 / Soundjay CC0（免费商用，无需署名）

详细的版权声明和资源来源请查看：**[RESOURCES_LICENSE.md](RESOURCES_LICENSE.md)**

## 🚀 快速开始

### 本地运行

```bash
git clone 你的仓库地址
cd animal_theater_pro
pip install -r requirements.txt
echo "SILICONFLOW_API_KEY=你的密钥" > .env
python main.py
```

访问 http://localhost:8000

### 云端部署

详细部署指南请查看 [DEPLOY.md](DEPLOY.md)

简而言之：
1. 上传到 GitHub
2. 在 Render 创建 Web Service
3. 添加环境变量 `SILICONFLOW_API_KEY`
4. 获取公网访问地址

## 🎨 技术栈

- **后端**: FastAPI + Python 3.9+
- **前端**: 原生 HTML/CSS/JavaScript（无需框架）
- **AI**: DeepSeek V3 (SiliconFlow)
- **音频**: Xeno-canto API
- **部署**: Render/Vercel

## 📱 动物库

包含32种动物，涵盖：
- 雨林奇珍（雪鸮、蓝闪蝶、树蛙...）
- 海洋巨兽（座头鲸、海龟、小丑鱼...）
- 极地动物（帝企鹅、北极熊...）
- 丛林猛兽（孟加拉虎、熊猫、长颈鹿...）
- 沙漠生灵（阿拉伯骆驼、耳廓狐...）

## ⚙️ 配置说明

### 环境变量

|变量名|说明|必填|
|---|---|---|
|`SILICONFLOW_API_KEY`|SiliconFlow API密钥|✅|

### 添加新动物

编辑 `main.py` 中的 `ANIMAL_DATABASE`：

```python
{"zh": "动物中文名", "en": "学名", "img": "图片URL", "tag": "特色标签"}
```

## 📄 开源协议

本项目基于 MIT 协议开源

## 📜 版权声明

本项目使用的所有资源均来自免费可商用的公开来源：

| 资源类型 | 来源 | 许可证 |
|---------|------|-------|
| 图片 | Unsplash | Unsplash License（免费商用） |
| 音频 | WikiMedia Commons | CC0 / Public Domain |
| 音频 | Soundjay | CC0 |

**详细版权信息**：请查看 [RESOURCES_LICENSE.md](RESOURCES_LICENSE.md)

### 使用须知

- ✅ 可免费用于个人和商业项目
- ✅ 无需署名
- ❌ 不得单独售卖资源文件
- ❌ 不得用于商标或商业标识

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系

有问题？欢迎在 Issues 中讨论

---

**让每个孩子都能听见大自然的低语** 🌿🐾
