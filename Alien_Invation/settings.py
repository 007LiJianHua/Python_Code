'''
将外星人入侵的所有设置都放在这里
'''
class Settings():
    def __init__(self):
        "初始化的游戏的静态设置"
        #外星人入侵的一些基本设置
        self.screen_width = 1000
        self.screen_height = 800
        self.bg_color = (230,230,230)
        #飞船的设置
        self.ship_speed_factor = 1.5    #以像素为单位
        self.ship_limit = 3 #一开始就有三个飞船
        #子弹的一些设置
        self.bullet_speed_factor = 3
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 10
        #外星人的移动设置
        self.alien_speed_factor = 1 #左右移动的速度
        self.fleet_drop_speed = 50
        self.fleet_direction = 1    #1表示向右移动，-1表示向左移动
        #以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        #击杀外星人后，点数的提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        "初始化随游戏而进行变化的设置"
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        #1为向右边，-1 为向左边
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        "提高速度设置"
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points* self.score_scale)