import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
def check_keydown_events(event,ship,screen,ai_settings,bullets):
    #相应按键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings=ai_settings,screen=screen,ship=ship,bullets=bullets)
    elif event.key == pygame.K_q:
        sys.quit()

def fire_bullet(ai_settings,screen,ship,bullets):
    "如果没有达到限制，就发射一颗子弹"
    #创建新子弹，并将其加入到编组bullets中。
    if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings=ai_settings,screen=screen,ship=ship)
            bullets.add(new_bullet)
def check_up_events(event,ship):
    #相应松开
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ship,ai_settings,screen,bullets,stats,play_button,aliens,sb):
    #相应键盘和鼠标事件
    for event in pygame.event.get():    #用来获取用户的键盘输入
            if event.type == pygame.QUIT:   #如果用户点击了屏幕的退出按钮，调用sys方法退出
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event=event,ship=ship,ai_settings=ai_settings,screen=screen,bullets=bullets)
            elif event.type == pygame.KEYUP:
                check_up_events(event=event,ship=ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y = pygame.mouse.get_pos()    #获取玩家点击到的鼠标位置
                check_play_button(stats=stats,play_button=play_button,mouse_x=mouse_x,mouse_y=mouse_y,
                                  ai_settings=ai_settings,screen=screen,ship=ship,aliens=aliens,bullets=bullets,sb=sb)

def check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,screen,ship,aliens,bullets,sb):
    "在玩家点击Play开始新的游戏，并重置所有游戏信息"
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)     #当光标位于游戏窗口时，将其隐藏。
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        #重置记分牌图像
        sb.prep_score()
        sb.prep_level()
        sb.prep_high_score()
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings=ai_settings,screen=screen,aliens=aliens,ship=ship)
        ship.center_ship()

def update_screen(ai_settings,screen,ship,bullets,aliens,play_button,stats,sb):
    screen.fill(ai_settings.bg_color)   #每次循环的时候重新绘制屏幕，只接受一个颜色参数
    "在飞船和外星人后面重新绘制所有子弹"
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()   #将飞船显示在屏幕前
    aliens.draw(screen)  #显示外星人
    sb.show_score()     #显示得分数
    "如果游戏处于非活动状态，就绘制Play按钮"
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()   #在每一次while循环结束后，刷新新的screen像素点位。

def update_bullets(bullets,aliens,ai_settings,screen,ship,sb,stats):
    "更新子弹的位置，并删除已经消失的子弹"
    #更新子弹的位置
    bullets.update()
    "消除已经消失的子弹"
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets,sb,stats)

def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets,sb,stats):
    "检查是否有子弹击中外星人，如果击中，就删除相应的子弹和外星人"
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:  #如果发生了外星人和子弹的碰撞，进行假分数的操作。
        "确保一个外星人50分，而不是一个子弹50分"
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()     #实时显示分数
        check_high_score(stats=stats,sb=sb)

    if len(aliens) == 0:
        #如果外星人都被消灭，则调用create_fleet()，再次生成一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings=ai_settings,screen=screen,ship=ship,aliens=aliens)

def get_number_aliens_x(ai_settings,alien_width):
    "计算一行可以容纳多少个外星人"
    available_space_x = ai_settings.screen_width - 2* alien_width
    number_alien_x = int(available_space_x / (2* alien_width))
    return number_alien_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    "创建一个外星人并将其放到当前行"
    alien = Alien(ai_settings=ai_settings,screen=screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x      #外星人的x坐标
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number       #外星人的y坐标
    aliens.add(alien)

def create_fleet(ai_settings,screen,aliens,ship):
    "创建外星人群"
    alien = Alien(ai_settings=ai_settings,screen=screen)
    number_aliens_x = get_number_aliens_x(ai_settings=ai_settings,alien_width=alien.rect.width)
    number_rows = get_number_rows(ai_settings=ai_settings,ship_height=ship.rect.height,alien_height=alien.rect.height)
    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #创建第一个外星人并将其加入到当前行
            create_alien(ai_settings=ai_settings,screen=screen,aliens=aliens,alien_number=alien_number,row_number=row_number)

def get_number_rows(ai_settings,ship_height,alien_height):
    avaliable_space_y = (ai_settings.screen_width - (3* alien_height) - ship_height)
    number_rows = int(avaliable_space_y / (4*alien_height))
    return number_rows

def check_fleet_edges(ai_settings,aliens):
    "有外星人到达边缘做相应的措施"
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings=ai_settings,aliens=aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    "将所有外星人向下移动，并改变他们的方向"
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings,aliens,ship,stats,screen,bullets,sb):
    "检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"
    check_fleet_edges(ai_settings=ai_settings,aliens=aliens)
    aliens.update()
    "spritecollideany(),接受两个实参，一个精灵，一个编组，将精灵与编组中的每个元素检查是否碰撞，未碰撞None,碰撞True"
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings=ai_settings,stats=stats,screen=screen,ship=ship,aliens=aliens,bullets=bullets,sb=sb)
    check_aliens_bottom(ai_settings=ai_settings,stats=stats,screen=screen,ship=ship,aliens=aliens,bullets=bullets,sb=sb)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb):
    "相应被外星人撞到的飞船"
    if stats.ships_left > 0:
        stats.ships_left -= 1   #撞到了就-1
        #更新记分牌
        sb.prep_ships()
        "清空外星人列表和飞船列表"
        aliens.empty()
        bullets.empty()
        "创建一群新的外星人，并将飞船放到屏幕低端中央"
        create_fleet(ai_settings=ai_settings,screen=screen,aliens=aliens,ship=ship)
        ship.center_ship()
        "暂停"
        sleep(0.5)
    else:
        stats.game_active = False
        #在游戏结束时，显示光标，让玩家能够继续点击Play
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb):
    "检查是否有外星人到达了屏幕低端"
    screen_rect = screen.get_rect()
    "遍历aliens编组中的所有精灵（外星人）"
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            "像飞船被撞到一样处理"
            ship_hit(ai_settings=ai_settings,stats=stats,screen=screen,ship=ship,aliens=aliens,bullets=bullets,sb=sb)
            break
def check_high_score(stats,sb):
    """检查是否获得了最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()