import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure bot intents - members intent is required for on_member_join event
intents = discord.Intents.default()
intents.members = True  # Required for detecting new member joins
intents.message_content = True  # Required for command processing

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration - You can customize these roles for your server
AVAILABLE_ROLES = {
    "🧑‍🎓": "🧑‍🎓24B TKJ",
    "🚹": "🚹Musang Jantan",
    "🚺": "🚺Musang Betina"
}


class RoleSelectionView(discord.ui.View):

    def __init__(self):
        super().__init__(
            timeout=1800)  # 30 minutes timeout for better user experience

    @discord.ui.button(label='🧑‍🎓 24B TKJ', style=discord.ButtonStyle.primary)
    async def tkj_button(self, interaction: discord.Interaction,
                         button: discord.ui.Button):
        await self.assign_role(interaction, "🧑‍🎓24B TKJ")

    @discord.ui.button(label='🚹 Musang Jantan',
                       style=discord.ButtonStyle.primary)
    async def male_button(self, interaction: discord.Interaction,
                          button: discord.ui.Button):
        await self.assign_role(interaction, "🚹Musang Jantan")

    @discord.ui.button(label='🚺 Musang Betina',
                       style=discord.ButtonStyle.primary)
    async def female_button(self, interaction: discord.Interaction,
                            button: discord.ui.Button):
        await self.assign_role(interaction, "🚺Musang Betina")

    async def assign_role(self, interaction: discord.Interaction,
                          role_name: str):
        try:
            # Check if we're in a guild
            if interaction.guild is None:
                await interaction.response.send_message(
                    "❌ Perintah ini hanya bisa digunakan di dalam server.",
                    ephemeral=True)
                return

            # Get the member object - interaction.user should be a Member in guild context
            if isinstance(interaction.user, discord.Member):
                member = interaction.user
            else:
                # Fallback: fetch member if needed
                try:
                    member = await interaction.guild.fetch_member(
                        interaction.user.id)
                except discord.NotFound:
                    await interaction.response.send_message(
                        "❌ Tidak dapat menemukan keanggotaan Anda di server ini.",
                        ephemeral=True)
                    return

            # Find the role in the server
            role = discord.utils.get(interaction.guild.roles, name=role_name)

            if role is None:
                await interaction.response.send_message(
                    f"❌ Role '{role_name}' tidak ada di server ini. Silakan hubungi admin untuk membuatnya.",
                    ephemeral=True)
                return

            # Check if user already has the role
            if role in member.roles:
                await interaction.response.send_message(
                    f"Anda sudah memiliki role {role_name}! ✅", ephemeral=True)
                return

            # Add the role to the user
            await member.add_roles(role)
            await interaction.response.send_message(
                f"✅ Anda telah diberikan role **{role_name}**! Selamat datang di komunitas!",
                ephemeral=True)

        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Saya tidak memiliki izin untuk memberikan role. Silakan hubungi admin.",
                ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Terjadi kesalahan saat memberikan role: {str(e)}",
                ephemeral=True)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} servers')

    # Set bot status
    # await bot.change_presence(
    #     activity=discord.Activity(type=discord.ActivityType.watching, name=""))


@bot.event
async def on_member_join(member):
    """Called when a new member joins the server"""

    # Create welcome embed
    embed = discord.Embed(
        title="🎉 Selamat Datang di Server!",
        description=
        f"Halo {member.mention}! Selamat datang di **{member.guild.name}**!\n\n"
        "Silakan pilih role Anda di bawah ini untuk mendapatkan akses ke channel server:",
        color=0x00ff00)

    embed.add_field(name="Role yang Tersedia:",
                    value="🧑‍🎓 **🧑‍🎓24B TKJ** - Untuk siswa kelas 24B TKJ\n"
                    "🚹 **🚹Musang Jantan** - Untuk anggota laki-laki\n"
                    "🚺 **🚺Musang Betina** - Untuk anggota perempuan",
                    inline=False)

    embed.set_footer(text="Klik tombol di bawah ini untuk memilih role Anda!")
    embed.set_thumbnail(
        url=member.avatar.url if member.avatar else member.default_avatar.url)

    # Create the role selection view
    view = RoleSelectionView()

    # Always post in a server channel to ensure interactions work properly
    welcome_channel = None

    # Look for common welcome channel names
    for channel in member.guild.text_channels:
        if any(name in channel.name.lower()
               for name in ['welcome', 'general', 'lobby', 'verification']):
            if channel.permissions_for(member.guild.me).send_messages:
                welcome_channel = channel
                break

    # If no specific channel found, use the first available text channel
    if welcome_channel is None:
        for channel in member.guild.text_channels:
            if channel.permissions_for(member.guild.me).send_messages:
                welcome_channel = channel
                break

    if welcome_channel:
        await welcome_channel.send(
            f"{member.mention}, silakan pilih role Anda untuk memulai:",
            embed=embed,
            view=view)
    else:
        print(
            f"Tidak dapat mengirim pesan selamat datang ke {member.name} - tidak ada channel yang cocok"
        )


# Admin command to create missing roles
@bot.command(name='setup_roles')
@commands.has_permissions(administrator=True)
async def setup_roles(ctx):
    """Admin command to create the verification roles if they don't exist"""
    created_roles = []
    existing_roles = []

    for role_name in AVAILABLE_ROLES.values():
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role is None:
            try:
                new_role = await ctx.guild.create_role(name=role_name,
                                                       mentionable=True)
                created_roles.append(new_role.name)
            except discord.Forbidden:
                await ctx.send("❌ Saya tidak memiliki izin untuk membuat role."
                               )
                return
        else:
            existing_roles.append(role.name)

    response = "**Pengaturan Role Selesai!**\n"
    if created_roles:
        response += f"✅ Role yang dibuat: {', '.join(created_roles)}\n"
    if existing_roles:
        response += f"ℹ️ Sudah ada: {', '.join(existing_roles)}\n"

    await ctx.send(response)


# Test command for verification
@bot.command(name='test_welcome')
@commands.has_permissions(administrator=True)
async def test_welcome(ctx, member: discord.Member = None):
    """Admin command to test the welcome message"""
    if member is None:
        if isinstance(ctx.author, discord.Member):
            member = ctx.author
        else:
            await ctx.send("❌ Silakan tentukan anggota untuk ditest.")
            return

    # Simulate the member join event
    await on_member_join(member)
    await ctx.send(
        f"✅ Pesan selamat datang test telah dikirim untuk {member.mention}")


# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "❌ Anda tidak memiliki izin untuk menggunakan perintah ini.")
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignore unknown commands
    else:
        print(f"Error: {error}")


# Run the bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token is None:
        print("❌ Variabel environment DISCORD_BOT_TOKEN tidak ditemukan!")
        print("Silakan atur token bot Discord Anda di file .env")
    else:
        bot.run(token)
