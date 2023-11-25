import os
import discord
from discord.ext import commands
import openai
from openai import OpenAI
client = OpenAI()

# 设置你的 Discord bot 的 token 和 OpenAI API 密钥
#DISCORD_TOKEN = ''
#OPENAI_API_KEY = ''

# 设置你的 ChatGPT 模型 ID
GPT_MODEL_ID = 'gpt-3.5-turbo'  # 例如："text-davinci-003"

# 创建 bot 实例时传递 intents 参数
intents = discord.Intents.all()
intents.members = True
intents.messages = True  # 启用消息事件

# 创建 bot 实例
bot = commands.Bot(command_prefix='/', intents=intents)
bot_ext = discord.ext.commands.Bot(command_prefix='/', intents=intents)

# 设置 OpenAI API 密钥
openai_api_key = os.environ.get('OPENAI_API_KEY')

# 设置 Discord密钥
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

# 当 bot 启动时打印信息
@bot.event
async def on_ready():
    bot_info = await bot.application_info() # 获取bot相关信息
    print(f"Bot Basic Info: \n {bot_info}")
    bot.owner_id = bot_info.owner.id
    await bot.change_presence(activity=discord.Game(name="Genshin Impact"))
    print(f'{bot.user.name} has connected to Discord!')
    # 获取指定的频道对象
    #channel_id = 924157831450603603  # 用你的频道 ID 替换
    #channel_id = 1176529369125097542  # 测试频道
    #channel = bot.get_channel(channel_id)
    
    #if channel:
        # 在指定频道发送一段话
        #await channel.send("Initializating %$^&*$&*&^*&%^ \n3,2,1......认知模块覆写中 \n亲爱的用户，你好，我是你爹。")
    return bot.owner_id

# 定义 /hello 命令
@bot.command(name='hello', description='Say hello to the user')
async def hello(ctx):
    await ctx.send("你吼辣么大声干什么嘛！")

# 定义 /bot_info 命令
@bot.command(name='bot_info', description='Provides information about the bot.')
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

# 定义命令处理函数
@bot.command(name='chatgpt', description='Call ChatGPT')
async def chatgpt(ctx, *args):
    # 检查是否提供了输入文本
    if not args:
        await ctx.send("Please provide a message for ChatGPT.")
        return

    # 将输入文本连接成一个字符串
    input_text = ' '.join(args)

    # 调用 ChatGPT
    # response = chatgpt_call(input_text)

    # 发送回应消息到频道
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

@bot.command(name='change_game', description='Change the game bot is playing')
async def change_presence(ctx, game_name):
    # 检查是否是 bot 的拥有者
    if ctx.author.id == bot.owner_id:
        await bot.change_presence(activity=discord.Game(name=game_name))
        # await ctx.send(f"Bot正在玩 {game_name}")
    else:
        await ctx.send("你没有权限执行此命令！")


# 启动 bot
bot.run(DISCORD_TOKEN)

'''
# 当 bot 启动时打印信息
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
     # 获取指定的频道对象
    channel_id = 924157831450603603  # 用你的频道 ID 替换
    channel = bot.get_channel(channel_id)
    
    if channel:
        # 在指定频道发送一段话
        await channel.send("Initializating %$^&*$&*&^*&%^ \n3,2,1......认知模块覆写中 \n亲爱的用户，你好，我是你爹。")


def chatgpt_call(input_text):
    # 调用 ChatGPT
    response = openai.chat.completions.create(
        model=GPT_MODEL_ID,
        messages=input_text,
        max_tokens=500  # 设置生成的最大标记数
    )

    return response['choices'][0]['text'].strip()
'''
