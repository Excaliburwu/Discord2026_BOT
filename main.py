import os
import discord
from discord.ext import commands

from myserver  import server_on



# 1. ตั้งค่า Intents เพื่อให้บอทมองเห็นข้อความที่คนพิมพ์มา
intents = discord.Intents.default()
intents.message_content = True

# 2. สร้างตัวแปรบอทและกำหนด Prefix (ในที่นี้ใช้ '!' นำหน้าคำสั่ง)
bot = commands.Bot(command_prefix='!', intents=intents)

# 3. Event เมื่อบอทออนไลน์และพร้อมทำงาน
@bot.event
async def on_ready():
    print(f'🟢 ล็อกอินสำเร็จในชื่อ {bot.user}')
    print('พร้อมรับคำสั่งแล้ว!')

# 4. คำสั่งทั่วไป (ตัวอย่าง: พิมพ์ !hello บอทจะตอบกลับ)
@bot.command()
async def hello(ctx):
    await ctx.send(f'สวัสดีครับคุณ {ctx.author.name}! มีอะไรให้ผมช่วยไหมครับ? 👋')

# 5. คำสั่งเคลียร์ช่องแชท (ตัวอย่าง: พิมพ์ !clear 10 เพื่อลบ 10 ข้อความ)
@bot.command()
@commands.has_permissions(manage_messages=True) # บังคับว่าคนพิมพ์ต้องมีสิทธิ์จัดการข้อความ
async def clear(ctx, amount: int = 5):
    # ลบข้อความตามจำนวนที่ระบุ + 1 (รวมตัวข้อความคำสั่ง !clear ที่ผู้ใช้เพิ่งพิมพ์มาด้วย)
    deleted = await ctx.channel.purge(limit=amount + 1)
    
    # แจ้งเตือนว่าลบเสร็จแล้ว และตั้งเวลาลบข้อความแจ้งเตือนนี้ทิ้งใน 3 วินาที
    await ctx.send(f'🗑️ ทำการลบข้อความจำนวน {len(deleted)-1} ข้อความเรียบร้อยแล้ว!', delete_after=3.0)

# 6. แจ้งเตือน Error กรณีที่ผู้ใช้ไม่มีสิทธิ์ใช้คำสั่ง !clear
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ คุณไม่มีสิทธิ์ `Manage Messages` ในการใช้งานคำสั่งนี้ครับ", delete_after=5.0)


server_on()

# รันบอท
bot.run(os.getenv('TOKEN'))