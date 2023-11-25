import os
import discord
from discord.ext import commands
import interactions
from interactions import Client
import openai
from openai import OpenAI
client = OpenAI()

# 设置你的 Discord bot 的 token 和 OpenAI API 密钥
TOKEN = '12345'
OPENAI_API_KEY = '12345'

# 创建 bot 实例时传递 intents 参数
intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
client = interactions.Client(intents=intents)
intents.members = True
intents.messages = True  # 启用消息事件

# 设置你的 ChatGPT 模型 ID
GPT_MODEL_ID = 'gpt-3.5-turbo'  # 例如："text-davinci-003"

# 创建 bot 实例
bot = commands.Bot(command_prefix='/', intents=intents)
interactions = Client(bot=bot)

# 设置 OpenAI API 密钥
openai.api_key = OPENAI_API_KEY

# 定义 /hello 命令
@interactions.slash_command(name='hello', description='Say hello to the user')
async def hello(ctx):
    await ctx.send("你吼辣么大声干什么嘛！")

# 定义 /bot_info 命令
@interactions.slash_command(name='bot_info', description='Provides information about the bot.')
async def bot_info(ctx):
    app_info = await bot.application_info()
    bot_info_embed = discord.Embed(
        title='Bot Information',
        description="Description: \n\n" + app_info.description,
        color=discord.Color.blue()
    )
    # 将作者作为 Embed 的作者
    bot_info_embed.set_author(name=app_info.owner.name, icon_url=app_info.owner.avatar.url)
    # 添加作者的头像到 Embed 中
    bot_info_embed.set_thumbnail(url=bot.user.avatar.url)
    await ctx.send(embed=bot_info_embed)

# 定义 /chatgpt 命令
@interactions.slash_command(name='chatgpt', description='Call ChatGPT')
async def chatgpt(ctx, *args):
    # 检查是否提供了输入文本
    if not args:
        await ctx.send("Please provide a message for ChatGPT.")
        return

    # 将输入文本连接成一个字符串
    input_text = ' '.join(args)

    # 调用 ChatGPT
    await chatgpt_call(ctx, input_text)

async def chatgpt_call(ctx, input_text):
    try:
        async with ctx.typing():  # 在等待期间显示"正在输入"状态
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": input_text,
                    },
                ],
                max_tokens=1000,
            )
        response_content = response.choices[0].message.content
        await ctx.send(response_content)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# 启动 bot
bot.run('YOUR_BOT_TOKEN')
