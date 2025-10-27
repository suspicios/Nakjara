from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuration
BOT_TOKEN = "8111267492:AAEqr7wwBf_ttmSRJ7QlEfJErNyp8-oeTco"
GROUP_CHAT_ID = -1002797887617# Replace with your group chat ID (negative for groups)
USER_ID_TO_ADD = 8111327106  # Replace with the user ID you want to add

async def add_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command to add a member to the group
    Usage: /addmember
    """
    try:
        # Create an invite link for the specific user
        invite_link = await context.bot.create_chat_invite_link(
            chat_id=GROUP_CHAT_ID,
            member_limit=1,  # Only 1 person can use this link
            name="Auto-generated invite"
        )
        
        # Send the invite link to the user
        await context.bot.send_message(
            chat_id=USER_ID_TO_ADD,
            text=f"You've been invited to join a group!\n\n{invite_link.invite_link}"
        )
        
        # Confirm in the group or to the admin
        await update.message.reply_text(
            f"✅ Invite link sent to user {USER_ID_TO_ADD}"
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def add_member_directly(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Alternative: Try to add member directly (requires bot to be admin)
    Usage: /addnow
    """
    try:
        # This requires the bot to have "Add Members" permission
        await context.bot.unban_chat_member(
            chat_id=GROUP_CHAT_ID,
            user_id=USER_ID_TO_ADD,
            only_if_banned=False
        )
        
        await update.message.reply_text(
            f"✅ User {USER_ID_TO_ADD} has been added to the group!"
        )
        
    except Exception as e:
        await update.message.reply_text(
            f"❌ Error: {str(e)}\n\n"
            f"Note: Bot needs 'Add Members' admin permission for this method."
        )

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("addmember", add_member))
    application.add_handler(CommandHandler("addnow", add_member_directly))
    
    # Start the bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
