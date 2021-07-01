import discord
import subprocess
import psutil
import datetime
from discord.ext import commands,tasks

Token = "NzA1NDk0ODc2ODM3NjQyMjcw.XqshTg.XBMKNMzfeoVUCcI4fqk6p9a92Rw"

class server:
    def __init__(self, start_bat, dir):
        self.start_bat = start_bat
        self.dir = dir
        self.last_boot = None
        self.status = False

    def start(self):
        self.minecraft_server = subprocess.Popen(self.start_bat, cwd=self.dir, shell=True, stdin=subprocess.PIPE)
        self.status = True

    def stop(self):
        self.command("stop")
        self.status = False
        self.minecraft_server.communicate()

    def command(self, command):
        self.minecraft_server.stdin.write(f"{command}\n".encode('utf-8'))

    def get_status(self):
        return self.status

client = commands.Bot(command_prefix=".")
client.remove_command("help")

def get_server_stats():
    server_data = {}
    grep_out = subprocess.check_output("java -version",shell=True,stderr=subprocess.STDOUT).decode("utf-8")
    java_version = grep_out.split(" ")[2].replace('"','')
    server_data["java_version"] = java_version
    server_data["core_count"] = psutil.cpu_count()
    server_data["cpu_temp"] = psutil.sensors_temperatures()["coretemp"][0].current
    return server_data

minecraft_server = server("java -Xms7G -Xmx7G -jar spigot-1.17.jar -nogui","/home/frank-server/minecraft")

server_data = get_server_stats()

@client.event
async def on_ready():
    print("punching a tree")

@client.command()
async def start_server(ctx):
    minecraft_mod = ctx.guild.get_role(859591710916214805)
    if minecraft_mod in ctx.message.author.roles:
        if not minecraft_server.get_status():
            minecraft_server.start()
            await ctx.message.channel.send("Starting the Server")
        else:
            await ctx.message.channel.send("Server's already up")
    else:
        await ctx.message.channel.send("Go as a minecraft mod, you peasant")

@client.command()
async def stop_server(ctx):
    minecraft_mod = ctx.guild.get_role(859591710916214805)
    if minecraft_mod in ctx.message.author.roles:
        if minecraft_server.get_status():
            await ctx.message.channel.send("Stopping the Server")
            minecraft_server.stop()
        else:
            await ctx.message.channel.send("Server's already down")
    else:
        await ctx.message.channel.send("Go ask a minecraft mod, you peasant")

@client.command()
async def stats(ctx):
    grep_out = subprocess.check_output("top -b -n1",shell=True).decode("utf-8")
    stats = grep_out.split("\n")[7].split(" ")
    cpu_load = stats[13]
    ram_usage = stats[14]
    Server_Embed = discord.Embed(colour=discord.Colour.red(),title="Server's status",description="**Sever Status** - ✅ Online")
    Server_Embed.add_field(name="**CPU Usage**",value=f"{cpu_load}%")
    Server_Embed.add_field(name="**RAM Usage**",value=f"{ram_usage}%")
    Server_Embed.add_field(name="**CPU Cores**",value=server_data["core_count"])
    Server_Embed.add_field(name="**CPU Temp**",value=server_data["cpu_temp"])
    Server_Embed.add_field(name="**Total RAM**",value="7.7GB")
    Server_Embed.add_field(name="**Java Version**",value=server_data["java_version"])
    await ctx.message.channel.send(embed=Server_Embed)

client.run(Token)
