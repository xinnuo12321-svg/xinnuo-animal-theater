from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import httpx
import random
import logging
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI() 

api_key = os.getenv("SILICONFLOW_API_KEY")
client = AsyncOpenAI(api_key=api_key, base_url="https://api.siliconflow.cn/v1")

ANIMAL_DATABASE = [
    {"zh": "红狐狸", "en": "Vulpes vulpes", "img": "https://images.unsplash.com/photo-1516934024742-b461fba47600?w=800", "tag": "森林猎人", "fallback": "毛茸茸的红狐狸🦊是大自然的精灵！"},
    {"zh": "变色龙", "en": "Chamaeleonidae", "img": "https://images.unsplash.com/photo-1538991383142-36c4edeaffde?w=800", "tag": "伪装大师", "fallback": "变色龙是神奇的魔术师🎨！能随着心情变换皮肤颜色🌈。"},
    {"zh": "阿拉伯骆驼", "en": "Camelus dromedarius", "img": "https://images.unsplash.com/photo-1588185542898-0cc25eb16d1f?w=800", "tag": "沙漠之舟", "fallback": "温柔的沙漠旅伴🐪！圆圆的驼峰像小沙发🛋️，存满能量不怕渴！"},
    {"zh": "火烈鸟", "en": "Phoenicopterus", "img": "https://images.unsplash.com/photo-1496886007421-2a106f3db1d5?w=800", "tag": "粉红天鹅", "fallback": "粉红的羽毛像晚霞🌅，长腿优雅踩水花💦。爱吃小虾变红妆！"},
    {"zh": "孟加拉虎", "en": "Panthera tigris", "img": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?w=800", "tag": "森林王者", "fallback": "威武的大老虎🐯！穿着漂亮的黑黄条纹大衣🧥，其实是爱干净的大猫！"},
    {"zh": "雪鸮", "en": "Bubo scandiacus", "img": "https://images.unsplash.com/photo-1517424168866-261537230491?w=800", "tag": "极地精灵", "fallback": "雪鸮是雪地小天使✨，披着白绒绒的棉花糖大衣，金黄圆眼睛滴溜溜转🦉！"},
    {"zh": "蓝金刚鹦鹉", "en": "Ara ararauna", "img": "https://images.unsplash.com/photo-1552728089-57105a8e7ce6?w=800", "tag": "彩虹羽翼", "fallback": "披着蓝黄相间的华丽外衣🦜，它是丛林里最闪亮的飞行家！"},
    {"zh": "帝企鹅", "en": "Aptenodytes forsteri", "img": "https://images.unsplash.com/photo-1513628253939-010e64ac66cd?w=800", "tag": "冰雪绅士", "fallback": "穿着黑白燕尾服的南极小绅士🐧！它们在冰雪里互相拥抱取暖❄️。"},
    {"zh": "梦幻水母", "en": "Medusozoa", "img": "https://images.unsplash.com/photo-1509070016581-915214674abc?w=800", "tag": "深海幽灵", "fallback": "像水下小星星✨，透明裙摆轻轻飘~没有骨头，晚上还会发光💡！"},
    {"zh": "非洲象", "en": "Loxodonta", "img": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=800", "tag": "陆地巨无霸", "fallback": "扇着像地图一样的大耳朵🐘，用长长的鼻子喷水洗澡🚿！最温柔的家族。"}
]

@app.get("/api/animal")
async def get_animal():
    animal = random.choice(ANIMAL_DATABASE)
    
    # 【修复1】：声音抓取时间放宽到 12 秒，并且不挑剔音质，只要有就拿！
    async def fetch_audio():
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
                res = await client.get("https://xeno-canto.org/api/2/recordings", params={"query": animal['en']}, headers=headers)
                if res.status_code == 200:
                    recs = res.json().get("recordings", [])
                    if recs:
                        # 撕掉“只拿A级”的愚蠢标签，直接拿第一条关联度最高的真实录音
                        best_rec = recs[0]
                        temp_url = best_rec.get("file", "")
                        return f"https:{temp_url}" if temp_url.startswith("//") else temp_url
        except Exception as e:
            logger.error(f"声音获取失败: {e}")
        return ""

    # 【修复2】：大模型生成文案，给足 10 秒思考时间
    async def fetch_story():
        try:
            completion = await client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",
                messages=[{"role": "user", "content": f"介绍动物【{animal['zh']}】，写一段50字以内适合幼儿的温柔科普文案，带emoji，富有美感。"}],
                timeout=10.0
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"大模型超时: {e}")
            return animal.get("fallback")

    # 并发执行两项任务
    audio_url, story = await asyncio.gather(fetch_audio(), fetch_story())

    return {
        "name": animal['zh'],
        "image": animal['img'],
        "audio": audio_url,
        "story": story,
        "tag": animal.get('tag', '')
    }

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)