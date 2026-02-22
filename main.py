from fastapi import FastAPI, Response, Query
from fastapi.staticfiles import StaticFiles
import os
import httpx
import random
import logging
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI() 

api_key = os.getenv("SILICONFLOW_API_KEY")
client = AsyncOpenAI(api_key=api_key, base_url="https://api.siliconflow.cn/v1")

# ==========================================
# 🐾 动物数据库
# 资源说明：
# - 图片：Unsplash License（免费商用，无需署名）
# - 音频：Archive.org Public Domain（美国鱼类和野生动物管理局录音）
# 详细版权信息见 RESOURCES_LICENSE.md
# 你可以按这个格式无限往下加新动物！
# ==========================================
ANIMAL_DATABASE = [
    {"zh": "红狐狸", "en": "Vulpes vulpes", "img": "https://images.unsplash.com/photo-1516934024742-b461fba47600?w=600", "tag": "森林猎人", "fallback": "毛茸茸的红狐狸🦊是大自然的精灵！",
     "fallback_audio": "https://archive.org/download/animalsounds1/11wolfhowls.mp3",
     "audio_source": "Archive.org Public Domain"},
    {"zh": "变色龙", "en": "Chamaeleonidae", "img": "https://images.unsplash.com/photo-1617540021016-72023b487e99?w=600", "tag": "伪装大师", "fallback": "变色龙是神奇的魔术师🎨！能随着心情变换皮肤颜色🌈。",
     "fallback_audio": "https://archive.org/download/animalsounds1/19frogsandsuch.mp3",
     "audio_source": "Archive.org Public Domain"},
    {"zh": "阿拉伯骆驼", "en": "Camelus dromedarius", "img": "https://images.unsplash.com/photo-1553983658-0d7afeb5c53f?w=600", "tag": "沙漠之舟", "fallback": "温柔的沙漠旅伴🐪！圆圆的驼峰像小沙发🛋️，存满能量不怕渴！",
     "fallback_audio": "https://archive.org/download/animalsounds1/52elkbellow.mp3",
     "audio_source": "Archive.org Public Domain"},
    {"zh": "火烈鸟", "en": "Phoenicopterus", "img": "https://images.unsplash.com/photo-1497206365907-f5e630693df0?w=600", "tag": "粉红天鹅", "fallback": "粉红的羽毛像晚霞🌅，长腿优雅踩水花💦。爱吃小虾变红妆！",
     "fallback_audio": "https://archive.org/download/animalsounds1/15redwingblackbird.mp3",
     "audio_source": "Archive.org Public Domain"},
    {"zh": "孟加拉虎", "en": "Panthera tigris", "img": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=600", "tag": "森林王者", "fallback": "威武的大老虎🐯！穿着漂亮的黑黄条纹大衣🧥，其实是爱干净的大猫！",
     "fallback_audio": "https://archive.org/download/animalsounds1/25alligatorhiss.mp3",
     "audio_source": "Archive.org Public Domain"},
    {"zh": "雪鸮", "en": "Bubo scandiacus", "img": "https://images.unsplash.com/photo-1553792843-99aa085309df?w=600", "tag": "极地精灵", "fallback": "雪鸮是雪地小天使✨，披着白绒绒的棉花糖大衣，金黄圆眼睛滴溜溜转🦉！",
     "fallback_audio": "https://archive.org/download/animalsounds1/30goldfinch.mp3",
     "audio_source": "Archive.org Public Domain"},
    {"zh": "蓝金刚鹦鹉", "en": "Ara ararauna", "img": "https://images.unsplash.com/photo-1573017714589-b40123679bf5?w=600", "tag": "彩虹羽翼", "fallback": "披着蓝黄相间的华丽外衣🦜，它是丛林里最闪亮的飞行家！",
     "fallback_audio": "https://archive.org/download/animalsounds1/35indigobunting.mp3",
     "audio_source": "Archive.org Public Domain"},
    {"zh": "帝企鹅", "en": "Aptenodytes forsteri", "img": "https://images.unsplash.com/photo-1551986782-d0169b3f8fa7?w=600", "tag": "冰雪绅士", "fallback": "穿着黑白燕尾服的南极小绅士🐧！它们在冰雪里互相拥抱取暖❄️。",
     "fallback_audio": "https://archive.org/download/animalsounds1/44loons.mp3",
     "audio_source": "Archive.org Public Domain"},
    {"zh": "梦幻水母", "en": "Medusozoa", "img": "https://images.unsplash.com/photo-1628944682084-831f35256163?w=600", "tag": "深海幽灵", "fallback": "像水下小星星✨，透明裙摆轻轻飘~没有骨头，晚上还会发光💡！",
     "fallback_audio": "https://archive.org/download/animalsounds1/39tundraswans.mp3",
     "audio_source": "Archive.org Public Domain"},
    {"zh": "非洲象", "en": "Loxodonta", "img": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=600", "tag": "陆地巨无霸", "fallback": "扇着像地图一样的大耳朵🐘，用长长的鼻子喷水洗澡🚿！最温柔的家族。",
     "fallback_audio": "https://archive.org/download/animalsounds1/53elkbellow2.mp3",
     "audio_source": "Archive.org Public Domain"}
]

# ==========================================
# 🚀 核心 API 路由 (并发执行)
# ==========================================
@app.get("/api/animal")
async def get_animal():
    animal = random.choice(ANIMAL_DATABASE)
    
    # 音频直接使用 archive.org 公共领域音频（无需网络请求）
    audio_url = animal.get("fallback_audio", "")

    # 生成AI文案（失败时使用预设文案）
    try:
        completion = await client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[{"role": "user", "content": f"介绍动物【{animal['zh']}】，写一段50字以内适合幼儿的温柔科普文案，带emoji，富有美感。"}],
            timeout=8.0
        )
        story = completion.choices[0].message.content
    except Exception:
        story = animal.get("fallback")

    return {
        "name": animal['zh'],
        "image": animal['img'],
        "audio": audio_url,
        "story": story,
        "tag": animal.get('tag', '')
    }

# ==========================================
# 🛡️ 图片代理服务器：Render 服务端代理 Unsplash 图片（绕过防盗链）
# 音频不走代理（<audio> 标签直接加载，不受 CORS 限制）
# ==========================================
@app.get("/api/proxy")
async def proxy_media(url: str = Query(...)):
    # 根据URL源选择不同的Referer
    if 'wikimedia.org' in url:
        referer = 'https://commons.wikimedia.org/'
    elif 'unsplash.com' in url:
        referer = 'https://unsplash.com/'
    elif 'pixabay.com' in url:
        referer = 'https://pixabay.com/'
    else:
        referer = 'https://www.google.com/'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8',
        'Referer': referer,
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site'
    }
    
    for attempt in range(2):  # 重试 1 次
        try:
            async with httpx.AsyncClient(
                follow_redirects=True,
                timeout=30.0,
                verify=True
            ) as client:
                req = await client.get(url, headers=headers)
                
                if req.status_code == 200:
                    content_type = req.headers.get("content-type", "application/octet-stream")
                    logger.info(f"代理成功：{url[:80]}... ({len(req.content)} bytes, {content_type})")
                    return Response(content=req.content, media_type=content_type)
                else:
                    logger.warning(f"代理失败（尝试 {attempt + 1}/{2}）：{url[:80]}... 状态码={req.status_code}")
                    
        except httpx.TimeoutException:
            logger.warning(f"代理超时（尝试 {attempt + 1}/{2}）：{url[:80]}...")
        except Exception as e:
            logger.warning(f"代理异常（尝试 {attempt + 1}/{2}）：{url[:80]}... 错误: {type(e).__name__}")
    
    # 所有尝试都失败后，返回 404
    logger.error(f"代理彻底失败：{url[:80]}...")
    return Response(status_code=404)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)