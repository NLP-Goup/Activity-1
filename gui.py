import dearpygui.dearpygui as dpg
import threading
import time
import random
from pyfiglet import Figlet
from ChatBot import MeowBot

class PixelCatGUI:
    def __init__(self):
        self.chatbot = MeowBot()
        self.is_cat_typing = False
        self.typing_animation_frames = 0
        self.chat_history = []
        
        # Cat cafe color palette (RGB values) note: you can just change thr RGB to change the color (187, 148, 87)
        self.colors = {
            'cream': (187, 148, 87),        # #EDE0D4 - lightest, main background
            'light_beige': (254, 250, 224),  # #E6CCB2 - secondary background
            'sandy_beige': (221, 161, 94),  # #DDB892 - accent color
            'warm_taupe': (176, 137, 104, 255),   # #B08968 - medium accent
            'rich_brown': (127, 85, 57, 255),     # #7F5539 - dark text
            'medium_brown': (156, 102, 68, 255),  # #9C6644 - secondary text
            'soft_white': (255, 250, 245, 255),   # Almost white for contrast
            'warm_orange': (210, 140, 90, 255), 
            'yellow': (221, 161, 94),# Derived warm accent
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
        
        # Setup Dear PyGui
        dpg.create_context()
        dpg.create_viewport(title="MeowBot", width=1350, height=690, resizable=False, max_width=1200, max_height=690, min_width=1200, min_height=690)
        dpg.setup_dearpygui()
        
        self.setup_theme()
        self.create_gui()
        
    def setup_theme(self):
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                # Warm cream background
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, self.colors['cream'])
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.colors['light_beige'])
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.colors['rich_brown'])
                
                # Button styling - warm and inviting
                dpg.add_theme_color(dpg.mvThemeCol_Button, self.colors['warm_taupe'])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, self.colors['sandy_beige'])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, self.colors['medium_brown'])
                
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
        
        #chat bubble themes
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
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 15)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)
                
        # Bot bubble theme (left side, warm cream with brown border)
        with dpg.theme() as self.bot_bubble_theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.colors['soft_white'])
                dpg.add_theme_color(dpg.mvThemeCol_Border, self.colors['medium_brown'])
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.colors['rich_brown'])
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 15)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)
                
        # System message theme (centered, warm orange tint)
        with dpg.theme() as self.system_bubble_theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, self.colors['light_beige'])
                dpg.add_theme_color(dpg.mvThemeCol_Border, self.colors['warm_orange'])
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.colors['rich_brown'])
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 15)
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)
     
    def create_input_border_theme(self):
        with dpg.theme() as input_border_theme:
            with dpg.theme_component(dpg.mvInputText):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, self.colors['soft_white'])
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, self.colors['cream'])
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, self.colors['light_beige'])
                dpg.add_theme_color(dpg.mvThemeCol_Border, self.colors['warm_taupe'])
                dpg.add_theme_color(dpg.mvThemeCol_Text, self.colors['rich_brown'])
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 2)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8)
        return input_border_theme
        
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
                    with dpg.child_window(width=828, height=500, tag="chat_history", no_scrollbar=False, horizontal_scrollbar=False):
                        # Initial welcome message
                        self.add_greetings_bubble("Hello! Welcome to our cozy cat cafe! I'm your friendly pixel cat companion. What would you like to chat about today? ☕🐱")
                    
                    # Input area
                    dpg.add_spacer(height=6)
                    with dpg.group(horizontal=True):
                        dpg.add_input_text(hint="Share your thoughts with our cafe cat...", 
                                         width=750, height=30, tag="user_input",
                                         callback=self.on_enter_pressed, multiline=True,
                                         on_enter=True)
                        dpg.bind_item_theme(dpg.last_item(), self.input_border_theme)
                        dpg.add_button(label="SEND", callback=self.send_message, height=30, width=70)
                    
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
        with dpg.group(parent="chat_history", horizontal=True):
            # Push content to the right
            dpg.add_spacer(width=320)
            
            with dpg.child_window(width=475, height=0, autosize_y=True, 
                                no_scrollbar=True, border=True):
                dpg.add_text("☕ YOU", color=self.colors['medium_brown'])
                dpg.add_text(message, color=self.colors['rich_brown'], wrap=380)
                
            bubble_id = dpg.last_item()
            dpg.bind_item_theme(bubble_id, self.user_bubble_theme)
        
        dpg.add_spacer(height=10, parent="chat_history")
        
        # Single scroll to bottom
        self.scroll_to_bottom()

    def add_bot_bubble(self, message):
        with dpg.child_window(width=475, height=0, autosize_y=True,
                            no_scrollbar=True, border=True, parent="chat_history"):
            dpg.add_text("🐱 MEOWBOT", color=self.colors['medium_brown'])
            dpg.add_text(message, color=self.colors['rich_brown'], wrap=380)
            
        bubble_id = dpg.last_item()
        dpg.bind_item_theme(bubble_id, self.bot_bubble_theme)

        dpg.add_spacer(height=10, parent="chat_history")
        
        self.scroll_to_bottom()

    def add_greetings_bubble(self, message):
        with dpg.child_window(width=380, height=0, autosize_y=True,
                            no_scrollbar=True, border=True, parent="chat_history"):
            dpg.add_text("🐱 MEOWBOT", color=self.colors['medium_brown'])
            dpg.add_text(message, color=self.colors['rich_brown'], wrap=380)
            
        bubble_id = dpg.last_item()
        dpg.bind_item_theme(bubble_id, self.bot_bubble_theme)
        
        dpg.add_spacer(height=10, parent="chat_history")
        
        self.scroll_to_bottom()

    def add_system_bubble(self, message):
        with dpg.group(parent="chat_history", horizontal=True):
            # Center the bubble
            dpg.add_spacer(width=110)
            
            with dpg.child_window(width=400, height=0, autosize_y=True, 
                                no_scrollbar=True, border=True):
                dpg.add_text("☕ CAFE SYSTEM", color=self.colors['warm_orange'])
                dpg.add_text(message, color=self.colors['rich_brown'], wrap=480)
                
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
        """Handle Enter key press"""
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
                    dpg.set_value("cat_typing_display", f"~ {typing_text} ~")
                
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
                stats_text += f"  {key}: {value}\n"
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