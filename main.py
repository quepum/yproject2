import sqlite3
import pygame
from pygame.locals import *
from classes import Rocket, Asteroid, Bullet, Explosion


def main():
    pygame.mixer.init()
    pygame.init()
    size = width, height = 500, 500
    font = pygame.font.Font('freesansbold.ttf', 30)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('The spaceship')

    rocket = Rocket(size)

    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(rocket)
    ast1 = pygame.USEREVENT + 1
    ast2 = pygame.USEREVENT + 2
    ast3 = pygame.USEREVENT + 3
    ast4 = pygame.USEREVENT + 4
    ast5 = pygame.USEREVENT + 5
    pygame.time.set_timer(ast1, 2000)
    pygame.time.set_timer(ast2, 6000)
    pygame.time.set_timer(ast3, 10000)
    pygame.time.set_timer(ast4, 15000)
    pygame.time.set_timer(ast5, 20000)

    start_img = pygame.image.load('start.jpg')
    restart_img = pygame.image.load('restart.png')
    bg = pygame.image.load('black.png')

    score = 0
    game = 0
    running = True
    gameStarted = False
    gameOver = False

    while running:
        if not gameStarted:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        gameStarted = True
                if gameOver:
                    # после окончания игры каждый раз выводится лучший результат игрока
                    screen.blit(restart_img, (0, 0))
                    db = sqlite3.connect('data.db')
                    sql = db.cursor()
                    sql.execute(f"""SELECT MAX(score) FROM users""")
                    res = sql.fetchone()
                    best_score = res[0]
                    db.commit()
                    text_best = font.render('BEST SCORE : ' + str(best_score), 1, (200, 255, 0))
                    screen.blit(text_best, (130, 270))

                else:
                    screen.blit(start_img, (0, 0))
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        pos = rocket.rect[:2]
                        bullet = Bullet(pos, rocket.comms, size)
                        bullets.add(bullet)
                        all_sprites.add(bullet)
                    if event.key == K_q:
                        rocket.rotate_left()
                    if event.key == K_e:
                        rocket.rotate_right()

                elif event.type == ast1:
                    ast = Asteroid(1, size)
                    asteroids.add(ast)
                    all_sprites.add(ast)
                elif event.type == ast2:
                    ast = Asteroid(2, size)
                    asteroids.add(ast)
                    all_sprites.add(ast)
                elif event.type == ast3:
                    ast = Asteroid(3, size)
                    asteroids.add(ast)
                    all_sprites.add(ast)
                elif event.type == ast4:
                    ast = Asteroid(4, size)
                    asteroids.add(ast)
                    all_sprites.add(ast)
                elif event.type == ast5:
                    ast = Asteroid(5, size)
                    asteroids.add(ast)
                    all_sprites.add(ast)

            pressed_keys = pygame.key.get_pressed()
            rocket.update(pressed_keys)

            asteroids.update()
            bullets.update()
            explosions.update()

            screen.blit(bg, (0, 0))
            explosions.draw(screen)

            for sprite in all_sprites:
                screen.blit(sprite.surf, sprite.rect)
            screen.blit(rocket.surf, rocket.rect)

            if pygame.sprite.spritecollideany(rocket, asteroids):
                # если ракета сталкивается с астероидом, то в бд записывается счёт, все переменные обнуляются
                rocket.kill()
                game += 1
                db = sqlite3.connect('data.db')
                sql = db.cursor()
                sql.execute(f"""INSERT INTO users 
                                                 VALUES (?, ?)""", (game, score))
                db.commit()
                score = 0
                for sprite in all_sprites:
                    sprite.kill()
                all_sprites.empty()
                rocket = Rocket(size)
                all_sprites.add(rocket)
                gameStarted = False
                gameOver = True

            for bullet in bullets:
                collision = pygame.sprite.spritecollide(bullet, asteroids, True)
                if collision:
                    # при столкновении пули и астероида происходит анимация взрыва, игроку начисляются очки
                    pos = bullet.rect[:2]
                    explosion = Explosion(pos)
                    explosions.add(explosion)
                    score += 1
                    bullet.kill()
                    bullets.remove(bullet)

            text = font.render('SCORE : ' + str(score), 1, (200, 255, 0))
            screen.blit(text, (330, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    main()
