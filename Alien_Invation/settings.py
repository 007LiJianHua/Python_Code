'''
将外星人入侵的所有设置都放在这里
'''
class Settings():
    def __init__(self):
        #外星人入侵的一些基本设置
        self.screen_width = 1000
        self.screen_height = 700
        self.bg_color = (230,230,230)
        self.ship_speed_factor = 1.5    #以像素为单位
        #子弹的一些设置
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 10