from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import httpx
import random
import logging
from openai import AsyncOpenAI
from dotenv import load_dotenv

# 1. 基础配置与日志
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI() 

# 【修复 1】：给文案大模型充足的思考时间 (15秒)，绝不轻易掐断它！
api_key = os.getenv("SILICONFLOW_API_KEY")
client = AsyncOpenAI(
    api_key=api_key, 
    base_url="https://api.siliconflow.cn/v1",
    timeout=15.0 
)

# ==========================================
# 🐾 修复版：加入全球极速 CDN 代理的高清图库
# ==========================================
# 在图片链接前加上 https://wsrv.nl/?url= 可以让国内访问国外图片提速数倍
CDN = "https://wsrv.nl/?url="

ANIMAL_DATABASE = [
    {"zh": "红狐狸", "en": "Vulpes vulpes", "img": f"{CDN}images.unsplash.com/photo-1516934024742-b461fba47600&w=800", "tag": "森林猎人"},
    {"zh": "变色龙", "en": "Chamaeleonidae", "img": f"{CDN}images.unsplash.com/photo-1538991383142-36c4edeaffde&w=800", "tag": "伪装大师"},
    {"zh": "阿拉伯骆驼", "en": "Camelus dromedarius", "img": f"{CDN}images.unsplash.com/photo-1588185542898-0cc25eb16d1f&w=800", "tag": "沙漠之舟"},
    {"zh": "火烈鸟", "en": "Phoenicopterus", "img": f"{CDN}images.unsplash.com/photo-1496886007421-2a106f3db1d5&w=800", "tag": "粉红天鹅"},
    {"zh": "孟加拉虎", "en": "Panthera tigris", "img": f"{CDN}images.unsplash.com/photo-1561731216-c3a4d99437d5&w=800", "tag": "森林王者"},
    {"zh": "雪鸮", "en": "Bubo scandiacus", "img": f"{CDN}images.unsplash.com/photo-1517424168866-261537230491&w=800", "tag": "极地精灵"},
    {"zh": "蓝金刚鹦鹉", "en": "Ara ararauna", "img": f"{CDN}images.unsplash.com/photo-1552728089-57105a8e7ce6&w=800", "tag": "彩虹羽翼"},
    {"zh": "帝企鹅", "en": "Aptenodytes forsteri", "img": f"{CDN}images.unsplash.com/photo-1513628253939-010e64ac66cd&w=800", "tag": "冰雪绅士"},
    {"zh": "梦幻水母", "en": "Medusozoa", "img": f"{CDN}images.unsplash.com/photo-1509070016581-915214674abc&w=800", "tag": "深海幽灵"},
    {"zh": "非洲象", "en": "Loxodonta", "img": f"{CDN}images.unsplash.com/photo-1557050543-4d5f4e07ef46&w=800", "tag": "陆地巨无霸"}
]

# ==========================================
# 🚀 核心 API 路由 
# ==========================================
@app.get("/api/animal")
async def get_animal():
    animal = random.choice(ANIMAL_DATABASE)
    audio_url = ""
    is_fallback = False
    
    # 1. 抓取真实野外声音 (【修复 2】：耐心等 8 秒，应对国内网络)
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        async with httpx.AsyncClient(timeout=8.0) as h_client:
            xeno_res = await h_client.get(f"https://xeno-canto.org/api/2/recordings?query={animal['en']}", headers=headers)
            recs = xeno_res.json().get("recordings", [])
            if recs:
                good_recs = [r for r in recs if r.get('q') == 'A']
                best_rec = good_recs[0] if good_recs else recs[0]
                temp_url = best_rec.get("file", "")
                if temp_url.startswith("//"):
                    audio_url = "https:" + temp_url
                else:
                    audio_url = temp_url
            else:
                is_fallback = True
    except Exception as e:
        is_fallback = True
        logger.warning(f"声音获取太慢，跳过: {e}")

    # 2. 调用 DeepSeek V3 生成文案 (文案引擎，死死锁住)
    try:
        completion = await client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[{"role": "user", "content": f"介绍动物【{animal['zh']}】，写一段50字以内适合幼儿的温柔科普文案，带emoji，富有美感。"}]
        )
        story = completion.choices[0].message.content
    except Exception:
        story = f"AI大脑正在休息，{animal['zh']}的秘密稍后再来听吧 ✨"

    return {
        "name": animal['zh'],
        "image": animal['img'],
        "audio": audio_url,
        "story": story,
        "is_fallback": is_fallback,
        "tag": animal.get('tag', '')
    }

# 静态网页挂载
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)