import bpy
import numpy as np
import functools


assets = [o for o in bpy.data.objects if o.asset_data]  # Select all object assets
assets.extend([m for m in bpy.data.materials if m.asset_data])  # Select all material assets

def sleep_until_previews_are_done(assets, callback):
    while assets:  # Check if all previews have been generated
        preview = assets[0].preview
        if preview is None:            
            assets[0].asset_generate_preview()
            return 0.2
        # If the preview is all black, means it was not generated :
        arr = np.zeros((preview.image_size[0] * preview.image_size[1]) * 4, dtype=np.float32)
        preview.image_pixels_float.foreach_get(arr)
        if np.all((arr == 0)):            
            assets[0].asset_generate_preview()
            return 0.2
        else:
            assets.pop(0)
    callback()
    return None

def message_end():
    def draw(self, context):
        self.layout.label(text="All previews have been generated !")
    bpy.context.window_manager.popup_menu(draw, title="Generation Finished")

if __name__ == "__main__":
    bpy.app.timers.register(
        functools.partial(
            sleep_until_previews_are_done, 
            assets, 
            message_end
        )
    )