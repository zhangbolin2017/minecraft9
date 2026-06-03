import math
TERRAIN_SEED=9031
BASE_GROUND_HEIGHT=4
HEIGHT_VARIATION=2
WORLD_HEIGHT=16

def h(x,z):
    wave_a=math.sin((x+TERRAIN_SEED)*0.11)*2.7
    wave_b=math.cos((z-TERRAIN_SEED)*0.08)*1.9
    wave_c=math.sin((x+z)*0.045)*1.6
    height=BASE_GROUND_HEIGHT+wave_a+wave_b+wave_c
    return max(3, min(WORLD_HEIGHT-4, int(round(height+HEIGHT_VARIATION*0.35))))

for z in range(3, 14):
    print(" ".join([f"{h(x,z):2d}" for x in range(3, 14)]))
