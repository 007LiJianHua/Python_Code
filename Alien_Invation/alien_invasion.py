'''
外星人入侵的主文件，设置屏幕的大小，颜色
'''
import pygame
import sys
from settings import Settings
from ship import Ship
import game_functions as gf
from alien import Alien
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard
def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))    #创建一个1200像素高，800像素宽的屏幕
    pygame.display.set_caption("Alien Invation")    #显示屏幕框的文字。
    play_button = Button(ai_settings=ai_settings,screen=screen,msg="Play")
    #创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings=ai_settings)
    sb = ScoreBoard(ai_settings=ai_settings,screen=screen,stats=stats)
    ship = Ship(screen,ai_settings)  #创建一个飞船
    bullets = Group()   #创建一个用于存储子弹的编组
    aliens = Group()    #创建一个存储外星人的编组
    gf.create_fleet(ai_settings,screen,aliens,ship=ship)
    alien = Alien(ai_settings=ai_settings,screen=screen)    #创建一个外星人实例
    while True:
        gf.check_events(ship=ship,ai_settings=ai_settings,screen=screen,bullets=bullets,stats=stats,
                        play_button=play_button,aliens=aliens)   #为了代码整洁，将函数写在了gf中。#相应键盘和鼠标事件
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets=bullets,aliens=aliens,ai_settings=ai_settings,screen=screen,ship=ship,sb=sb,stats=stats)
            gf.update_aliens(aliens=aliens,ai_settings=ai_settings,ship=ship,stats=stats,screen=screen,bullets=bullets)
        gf.update_screen(ai_settings=ai_settings,screen=screen,ship=ship,bullets=bullets,aliens=aliens,play_button=play_button,stats=stats,sb=sb)
        
run_game()  