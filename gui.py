import dearpygui.dearpygui as dpg
import threading
import time
import random
from pyfiglet import Figlet
from ChatBot import MeowBot
import os

print("Current working directory:", os.getcwd())
print("Font exists?", os.path.exists("Assets/fonts/SuperAdorable.ttf"))

class PixelCatGUI:
    def __init__(self):
        self.chatbot = MeowBot()
        self.is_cat_typing = False
        self.typing_animation_frames = 0
        self.chat_history = []

        self.colors = {
            'cream': (187, 148, 87),       # #EDE0D4 - lightest, main background
            'light_beige': (254, 250, 224),  # #E6CCB2 - secondary background
            'sandy_beige': (221, 161, 94),  # #DDB892 - accent color
            'warm_taupe': (176, 137, 104, 255),   # #B08968 - medium accent
            'rich_brown': (127, 85, 57, 255),     # #7F5539 - dark text
            'medium_brown': (156, 102, 68, 255),  # #9C6644 - secondary text
            'soft_white': (255, 250, 245, 255),   # Almost white for contrast
            'warm_orange': (210, 140, 90, 255), 
            'yellow': (221, 161, 94),# Derived warm accent
            'dark_orange': (255, 140, 0, 255),

            'roman_coffee': (120, 85, 71, 255),
            'pearl_lusta': (252, 237, 214, 255),
            'white': (255, 255, 255, 255),
            'pastel_brown': (200, 180, 160, 255)

        }
        
        # Pixel cat ASCII art frames for animation
        self.cat_idle = r"""
   /\_/\ 
  ( o.o )
   > ^ < 
        """
        
        self.cat_typing_frames = [
            r"""
   /\_/\ 
  ( -.o )
   > ^ < 
    |||  
        """,
            r"""
   /\_/\ 
  ( o.- )
   > ^ < 
   |||   
        """,
            r"""
   /\_/\ 
  ( -.- )
   > ^ < 
  |||    
        """
        ]
        
        self.figlet = Figlet(font='small')
        
        dpg.create_context()
        dpg.create_viewport(title="MeowBot", width=1350, height=690, resizable=False, max_width=1200, max_height=690, min_width=1200, min_height=690)
        dpg.setup_dearpygui()
        
        self.super_adorable_font_path = "Assets/fonts/Super Adorable.ttf"   
        self.bright_aura_font_path = "Assets/fonts/Bright Aura.ttf"      

        self.setup_fonts()
        self.setup_theme()
        self.create_profile_images()
        self.create_gui()

    def setup_fonts(self):
        """Loads and sets up custom fonts."""
        with dpg.font_registry():
            if os.path.exists(self.super_adorable_font_path):
                self.super_adorable_font = dpg.add_font(self.super_adorable_font_path, 20) 
            else:
                print(f"Warning: SuperAdorable font not found at {self.super_adorable_font_path}. Using default.")
                self.super_adorable_font = None

            if os.path.exists(self.bright_aura_font_path):
                self.bright_aura_font = dpg.add_font(self.bright_aura_font_path, 18) 
            else:
                print(f"Warning: BrightAura font not found at {self.bright_aura_font_path}. Using default.")
                self.bright_aura_font = None

    def create_profile_images(self):
        """Load profile images from JPG files"""
        with dpg.texture_registry():
            try:
                if os.path.exists("user_avatar.jpg"):
                    width, height, channels, data = dpg.load_image("user_avatar.jpg")
                    dpg.add_static_texture(width=width, height=height, default_value=data, tag="user_avatar")
                else:
                    print("user_avatar.jpg not found. Please add a user avatar image.")
                    self.create_default_user_avatar()
                
                if os.path.exists("bot_avatar.jpg"):
                    width, height, channels, data = dpg.load_image("bot_avatar.jpg")
                    dpg.add_static_texture(width=width, height=height, default_value=data, tag="bot_avatar")
                else:
                    print("bot_avatar.jpg not found. Please add a bot avatar image.")
                    self.create_default_bot_avatar()
                    
            except Exception as e:
                print(f"Error loading avatar images: {e}")
                print("Creating default avatars...")
                self.create_default_user_avatar()
                self.create_default_bot_avatar()
    
    def create_default_user_avatar(self):
        """Create default user avatar if JPG file is not found"""
        user_image_data = []
        for y in range(50):
            row = []
            for x in range(50):
                center_x, center_y = 25, 25
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                
                if distance <= 23:
                    if 15 <= y <= 35 and 18 <= x <= 32:
                        if (15 <= y <= 25 and (x == 18 or x == 32)) or (25 < y <= 35 and 18 <= x <= 32):
                            row.extend([255, 255, 255, 255])
                        else:
                            row.extend([70, 130, 180, 255])
                    else:
                        row.extend([70, 130, 180, 255])
                else:
                    row.extend([0, 0, 0, 0])
            user_image_data.extend(row)
        
        dpg.add_raw_texture(50, 50, user_image_data, tag="user_avatar", format=dpg.mvFormat_Float_rgba)
    
    def create_default_bot_avatar(self):
        """Create default bot avatar if JPG file is not found"""
        bot_image_data = []
        for y in range(50):
            row = []
            for x in range(50):
                center_x, center_y = 25, 25
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                
                if distance <= 23:
                    if (10 <= y <= 15 and 15 <= x <= 18) or (10 <= y <= 15 and 32 <= x <= 35):
                        row.extend([0, 0, 0, 255])
                    elif 25 <= y <= 28 and 23 <= x <= 27:
                        row.extend([255, 105, 180, 255])
                    elif y == 32 and (x == 20 or x == 25 or x == 30):
                        row.extend([0, 0, 0, 255])
                    else:
                        row.extend([255, 165, 0, 255])
                else:
                    row.extend([0, 0, 0, 0])
            bot_image_data.extend(row)
        
        dpg.add_raw_texture(50, 50, bot_image_data, tag="bot_avatar", format=dpg.mvFormat_Float_rgba)
        
    def setup_theme(self):
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                # Warm cream background
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, self.colors['cream'])
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.colors['pearl_lusta'])
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.colors['rich_brown'])
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 4, 4)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 4, 4)
                
                # Button styling - warm and inviting
                dpg.add_theme_color(dpg.mvThemeCol_Button, self.colors['warm_taupe'])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.colors['sandy_beige'])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.colors['medium_brown'])
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.colors['soft_white'])

                
                # Input field styling - soft and warm
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, self.colors['soft_white'])
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, self.colors['cream'])
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, self.colors['light_beige'])
                
                # Scrollbar styling
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, self.colors['light_beige'])
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, self.colors['warm_taupe'])
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, self.colors['sandy_beige'])
                
                # Separator color
                dpg.add_theme_color(dpg.mvThemeCol_Separator, self.colors['rich_brown'])
                
        dpg.bind_theme(global_theme)
        
        if self.super_adorable_font:
            dpg.bind_font(self.super_adorable_font)
        
        # Chat bubble themes
        self.create_bubble_themes()
        
        self.input_border_theme = self.create_input_border_theme()
        
    def create_bubble_themes(self):
        """Create themed styles for chat bubbles"""
        # User bubble theme (right side, slightly darker beige)
        with dpg.theme() as self.user_bubble_theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.colors['sandy_beige'])
                dpg.add_theme_color(dpg.mvThemeCol_Border, self.colors['warm_taupe'])
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.colors['rich_brown'])
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 25) 
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 10, 10) # Padding inside bubble

        # Bot bubble theme
        with dpg.theme() as self.bot_bubble_theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.colors['soft_white'])
                dpg.add_theme_color(dpg.mvThemeCol_Border, self.colors['medium_brown'])
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.colors['rich_brown'])
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 25)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 10, 10) 
        # System message theme
        with dpg.theme() as self.system_bubble_theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.colors['light_beige'])
                dpg.add_theme_color(dpg.mvThemeCol_Border, self.colors['warm_orange'])
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.colors['rich_brown'])
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 25)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 10, 10) 

    def create_input_border_theme(self):
        with dpg.theme() as input_border_theme:
            with dpg.theme_component(dpg.mvInputText):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, self.colors['soft_white'])
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, self.colors['cream'])
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, self.colors['light_beige'])
                dpg.add_theme_color(dpg.mvThemeCol_Border, self.colors['warm_taupe'])
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.colors['rich_brown'])
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 2)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 40)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 12)   
        return input_border_theme
    
    def calculate_text_size(self, text, wrap_width=400):
        """Calculate approximate text size for better bubble sizing"""
        font_height_approx = 22 
        wrap_factor = 7.5      
        
        lines = text.split('\n')
        total_lines = 0
        
        
        for line in lines:
            if len(line) == 0:
                total_lines += 1
            else:
                chars_per_line = wrap_width // 8   
                line_count = max(1, (len(line) + chars_per_line - 1) // chars_per_line)
                total_lines += line_count
        
        estimated_height = max(70, total_lines * 22 + 50)
        return min(estimated_height, 350)  
        
    def auto_scroll_to_bottom(self):
        """Helper function to properly scroll to bottom with delay"""
        def scroll_after_delay():
            time.sleep(0.1)
            if dpg.does_item_exist("chat_history"):
                dpg.set_y_scroll("chat_history", 1.0)
        
        threading.Thread(target=scroll_after_delay, daemon=True).start()
        
    def create_gui(self):
        with dpg.window(label="☕ MeowBot Cat Cafe ☕", tag="primary_window"):
            dpg.add_spacer(height=6)
            with dpg.group(horizontal=True):
                
                dpg.add_spacer(width=1)
                # Left side - Pixel cat display
                with dpg.child_window(width=300, height=615, tag="cat_display"):
                    dpg.add_text("MEOWBOT STATUS", color=self.colors['medium_brown'])
                    dpg.add_separator()
                    
                    # Cat ASCII art display
                    with dpg.group(horizontal=True):
                        dpg.add_spacer(width=100)
                        dpg.add_text(self.cat_idle, tag="cat_ascii", color=self.colors['yellow'])
                    
                    dpg.add_separator()
                    dpg.add_text("Meowbot whispers:", color=self.colors['medium_brown'])
                    dpg.add_text("Purr... Welcome to our cozy cat chat room! ", tag="cat_status", 
                                  color=self.colors['rich_brown'], wrap=380)
                    
                    # Cat typing animation area
                    dpg.add_separator()
                    dpg.add_text("", tag="cat_typing_display", color=self.colors['warm_taupe'])
                    
                # Right side - Chat interface
                with dpg.child_window(width=843, height=615, tag="chat_area", no_scrollbar=True, no_scroll_with_mouse=True):
                    dpg.add_text("Cozy Chat Corner:", color=self.colors['medium_brown'])
                    
                    # Chat history display
                    with dpg.child_window(width=828, height=470, tag="chat_history", no_scrollbar=False, horizontal_scrollbar=False):
                        # Initial welcome message
                        self.add_greetings_bubble("Hello! Welcome to our cozy cat cafe! I'm your friendly pixel cat companion. What would you like to chat about today? ☕🐱")
                    
                    # Input area
                    dpg.add_spacer(height=8)
                    with dpg.group(horizontal=True):
                        dpg.add_input_text(hint="Share your thoughts with our cafe cat...", 
                                             width=720, height=45, tag="user_input",
                                             callback=self.on_enter_pressed, multiline=False,
                                             on_enter=True)
                        dpg.bind_item_theme(dpg.last_item(), self.input_border_theme)
                        dpg.add_button(label="SEND", callback=self.send_message, height=45, width=90)
                    
                    # Control buttons
                    dpg.add_spacer(height=3)
                    with dpg.group(horizontal=True):
                        dpg.add_spacer(width=230)
                        dpg.add_button(label="🧠 MEMORY", callback=self.show_memory_stats)
                        dpg.add_spacer(width=10)
                        dpg.add_button(label="🧹 CLEAR MEMORY", callback=self.clear_memory)
                        dpg.add_spacer(width=10)
                        dpg.add_button(label="🗑️ CLEAR CHAT", callback=self.clear_chat)
                    dpg.add_spacer(height=6)
        
        dpg.set_primary_window("primary_window", True)
        
        self.start_animation_thread()
        
    def add_user_bubble(self, message):
        """Add user message bubble with profile photo"""
        bubble_height = self.calculate_text_size(message, 380)
        
        with dpg.group(parent="chat_history", horizontal=True):
            # Push content to the right for user messages
            dpg.add_spacer(width=230)
            
            # Chat bubble (now on the left of the avatar)
            with dpg.child_window(width=450, height=bubble_height, 
                                  no_scrollbar=True, border=True):
                dpg.add_text("☕ YOU", color=self.colors['medium_brown'])
                user_text_id = dpg.add_text(message, color=self.colors['rich_brown'], wrap=400)
                # Apply bright aura font to conversation text if available
                if self.bright_aura_font:
                    dpg.bind_item_font(user_text_id, self.bright_aura_font)
                
            bubble_id = dpg.last_item()
            dpg.bind_item_theme(bubble_id, self.user_bubble_theme)

            dpg.add_spacer(width=8) # Spacer between bubble and avatar
            # User avatar (now on the right)
            dpg.add_image("user_avatar", width=50, height=50)
            
        dpg.add_spacer(height=10, parent="chat_history")
        
        # Single scroll to bottom
        self.scroll_to_bottom()

    def add_bot_bubble(self, message):
        """Add bot message bubble with profile photo"""
        bubble_height = self.calculate_text_size(message, 380)
        
        with dpg.group(parent="chat_history", horizontal=True):
            # Bot avatar on the left (larger size)
            dpg.add_image("bot_avatar", width=50, height=50)
            dpg.add_spacer(width=8)
            
            with dpg.child_window(width=450, height=bubble_height,
                                  no_scrollbar=True, border=True):
                dpg.add_text("🐱 MEOWBOT", color=self.colors['medium_brown'])
                bot_text_id = dpg.add_text(message, color=self.colors['rich_brown'], wrap=400)
                if self.bright_aura_font:
                    dpg.bind_item_font(bot_text_id, self.bright_aura_font)
                
            bubble_id = dpg.last_item()
            dpg.bind_item_theme(bubble_id, self.bot_bubble_theme)

        dpg.add_spacer(height=10, parent="chat_history")
        
        self.scroll_to_bottom()

    def add_greetings_bubble(self, message):
        """Add greeting message bubble with bot profile photo"""
        bubble_height = self.calculate_text_size(message, 380)
        
        with dpg.group(parent="chat_history", horizontal=True):
            # Bot avatar on the left (larger size)
            dpg.add_image("bot_avatar", width=50, height=50)
            dpg.add_spacer(width=8)
            
            with dpg.child_window(width=450, height=bubble_height,
                                  no_scrollbar=True, border=True):
                dpg.add_text("🐱 MEOWBOT", color=self.colors['medium_brown'])
                greetings_text_id = dpg.add_text(message, color=self.colors['rich_brown'], wrap=400)
                if self.bright_aura_font:
                    dpg.bind_item_font(greetings_text_id, self.bright_aura_font)
                
            bubble_id = dpg.last_item()
            dpg.bind_item_theme(bubble_id, self.bot_bubble_theme)
        
        dpg.add_spacer(height=10, parent="chat_history")
        
        self.scroll_to_bottom()

    def add_system_bubble(self, message):
        """Add system message bubble centered"""
        bubble_height = self.calculate_text_size(message, 480)
        
        with dpg.group(parent="chat_history", horizontal=True):
            # Center the bubble
            dpg.add_spacer(width=150)
            
            with dpg.child_window(width=400, height=bubble_height, 
                                  no_scrollbar=True, border=True):
                dpg.add_text("☕ CAFE SYSTEM", color=self.colors['warm_orange'])
                system_text_id = dpg.add_text(message, color=self.colors['rich_brown'], wrap=480)
                if self.bright_aura_font:
                    dpg.bind_item_font(system_text_id, self.bright_aura_font)
                
            bubble_id = dpg.last_item()
            dpg.bind_item_theme(bubble_id, self.system_bubble_theme)
        
        dpg.add_spacer(height=10, parent="chat_history")
        
        # Single scroll to bottom
        self.scroll_to_bottom()
        
    def scroll_to_bottom(self):
        def delayed_scroll():
            time.sleep(0.1)
            dpg.set_y_scroll("chat_history", -1.0)
        
        threading.Thread(target=delayed_scroll, daemon=True).start()
        
    def on_enter_pressed(self, sender, app_data):
        """Handle Enter key press to send message"""
        self.send_message()
        
    def send_message(self):
        user_input = dpg.get_value("user_input")
        if not user_input.strip():
            return
            
        dpg.set_value("user_input", "")
        
        self.add_user_bubble(user_input)
        
        self.start_cat_typing()
        
        threading.Thread(target=self.process_message, args=(user_input,), daemon=True).start()
        
    def process_message(self, user_input):
        time.sleep(random.uniform(1, 2))

        response = self.chatbot.get_response(user_input)
        
        # Stop cat typing animation
        self.stop_cat_typing()
        
        self.add_bot_bubble(response)
        
        # Update cat status
        dpg.set_value("cat_status", f"Just purred: {response[:50]}{'...' if len(response) > 50 else ''} ☕")
        
    def start_cat_typing(self):
        self.is_cat_typing = True
        dpg.set_value("cat_status", "Thinking... *purr purr* ☕🐾")
        
    def stop_cat_typing(self):
        self.is_cat_typing = False
        dpg.set_value("cat_ascii", self.cat_idle)
        dpg.set_value("cat_typing_display", "")
        
    def animate_cat(self):
        while dpg.is_dearpygui_running():
            if self.is_cat_typing:
                # Cycle through typing animation frames
                frame_index = self.typing_animation_frames % len(self.cat_typing_frames)
                dpg.set_value("cat_ascii", self.cat_typing_frames[frame_index])
                
                # Show typing text animation with figlet
                typing_dots = "." * ((self.typing_animation_frames % 4) + 1)
                typing_text = f"Purring{typing_dots}"
                try:
                    figlet_text = self.figlet.renderText(typing_text)
                    dpg.set_value("cat_typing_display", figlet_text)
                except:
                    dpg.set_value("cat_typing_display", f"~ {typing_dots}")
                
                self.typing_animation_frames += 1
            else:
                # Reset to idle state
                dpg.set_value("cat_ascii", self.cat_idle)
                self.typing_animation_frames = 0
                
            time.sleep(0.5) 
            
    def start_animation_thread(self):
        animation_thread = threading.Thread(target=self.animate_cat, daemon=True)
        animation_thread.start()
           
    def show_memory_stats(self):
        memory = self.chatbot.data_manager.load_conversation_memory()
        user_context = memory.get("user_context", {})
        conversation_count = len(memory.get("conversations", []))
        
        stats_text = f"📊 CAFE MEMORY STATS:\n"
        stats_text += f"Conversations shared: {conversation_count}\n"
        stats_text += f"Current visit: {self.chatbot.session_id}\n"
        
        if user_context:
            stats_text += f"What our cafe cat remembers about you:\n"
            for key, value in user_context.items():
                stats_text += f"   {key}: {value}\n"
        else:
            stats_text += "You're a new visitor to our cafe! Tell me about yourself! ☕"
            
        self.add_system_bubble(stats_text)
        dpg.set_value("cat_status", "Shared what I remember about you! 📊☕")
        
    def clear_memory(self):
        self.chatbot.data_manager.save_conversation_memory({
            "conversations": [],
            "user_context": {},
            "session_count": 0
        })
        self.add_system_bubble("Memory cleared! Starting fresh like a new cafe visit. 🧹☕")
        dpg.set_value("cat_status", "Memory cleared! Fresh start like a new cafe day! 🧹☕")
        
    def clear_chat(self):
        self.chat_history = []
        dpg.delete_item("chat_history", children_only=True)
        self.add_bot_bubble("Chat cleared! Ready for new cozy conversations! ☕🐱")
        
    def run(self):
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

def main():
    print("☕ Starting Cozy Cat Cafe MeowBot GUI...")
    
    try:
        gui = PixelCatGUI()
        gui.run()
    except Exception as e:
        print(f"Error running GUI: {e}")
        print("Make sure you have the required dependencies:")
        print("pip install dearpygui pyfiglet")

if __name__ == "__main__":
    main()