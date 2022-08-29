import Funcs
import pygame, sys
from pygame.locals import *
import io
from urllib.request import urlopen

# initialize the window settings and pygame
pygame.init()
DISPLAYSURF = pygame.display.set_mode((1000, 750))
DISPLAYSURF.fill((255,255,255))
pygame.display.set_caption('High and Low Boxd')
silver = (192,192,192)
alive = False

# title
title_font = pygame.font.SysFont('Corbel',100)
title_text = title_font.render('High and Low Boxd', True, (0,0,0))
title_rect = title_text.get_rect()
title_rect.center = (500,200)
DISPLAYSURF.blit(title_text, title_rect)

# author
author_font = pygame.font.SysFont('Corbel', 50)
author_text = author_font.render('By: Franklin Dai', True, (0,0,0))
author_rect = author_text.get_rect()
author_rect.center = (500,275)
DISPLAYSURF.blit(author_text, author_rect)

# play button
menufont = pygame.font.SysFont('Corbel',70)
pygame.draw.rect(DISPLAYSURF, silver, (350,400, 300, 75))
play_text = menufont.render('Start Game', True, (0,0,0))
play_text_rect = play_text.get_rect()
play_text_rect.center = (500, 437.5)
DISPLAYSURF.blit(play_text, play_text_rect)

# how to play button
pygame.draw.rect(DISPLAYSURF, silver, (350,500, 300, 75))
instructions_text = menufont.render('How to Play', True, (0,0,0))
instructions_text_rect = instructions_text.get_rect()
instructions_text_rect.center = (500,537.5)
DISPLAYSURF.blit(instructions_text, instructions_text_rect)
instructions_font = pygame.font.SysFont('Corbel', 28)


# lower and higher button fonts
lowerfont = pygame.font.SysFont('corbel', 55)
lowertext = lowerfont.render('Lower', True, (0,0,0))
lowertext_rect = lowertext.get_rect()
lowertext_rect.center = (640,625)

higherfont = pygame.font.SysFont('corbel', 50)
highertext = higherfont.render('Higher', True, (0,0,0))
highertext_rect = highertext.get_rect()
highertext_rect.center = (810,625)

# score counter
c = 0
scorefont = pygame.font.SysFont('courier', 80)
highscore = 0

# initialize two example movies to avoid errors in the game loop
movie1 = ('Shrek (2001)', '3.99', 'https://image.tmdb.org/t/p/w300_and_h450_bestv2/iB64vpL3dIObOtMZgX3RqdVdQDc.jpg')
movie2 = ('Scott Pilgrim vs. the World (2010)', '3.87', 'https://image.tmdb.org/t/p/w300_and_h450_bestv2/g5IoYeudx9XBEfwNL0fHvSckLBz.jpg')

# game loop
while True:
    mouse = pygame.mouse.get_pos()
    if movie1[1] > movie2[1]:
        answer = "Lower"
    else:
        answer = "Higher"
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # click the play button and start the game
            if 350 <= mouse[0] <= 650 and 400 <= mouse[1] <= 475 and not alive:
                # reset the screen
                pygame.draw.rect(DISPLAYSURF, (255, 255, 255), (0, 0, 1000, 750))

                # lower button
                pygame.draw.rect(DISPLAYSURF, (50,205,50), (575, 600, 130, 50))
                DISPLAYSURF.blit(lowertext, lowertext_rect)

                # higher button
                pygame.draw.rect(DISPLAYSURF, (220,20,60), (745, 600, 130, 50))
                DISPLAYSURF.blit(highertext, highertext_rect)

                # get movie1 and poster
                movie1 = Funcs.get_movie(
                    "https://letterboxd.com/joeibanez/list/the-100-most-watched-films-on-letterboxd/by/shuffle/")
                img1 = urlopen(movie1[2]).read()
                image_file1 = io.BytesIO(img1)
                image1 = pygame.image.load(image_file1)
                image1 = pygame.transform.scale(image1, (300, 450))

                # get movie2 and poster
                movie2 = Funcs.get_movie(
                    "https://letterboxd.com/joeibanez/list/the-100-most-watched-films-on-letterboxd/by/shuffle/")
                while movie2[0] == movie1[0] or movie2[1] == movie1[1]:
                    movie2 = Funcs.get_movie(
                        "https://letterboxd.com/joeibanez/list/the-100-most-watched-films-on-letterboxd/by"
                        "/shuffle/")
                img2 = urlopen(movie2[2]).read()
                image_file2 = io.BytesIO(img2)
                image2 = pygame.image.load(image_file2)
                image2 = pygame.transform.scale(image2, (300, 450))

                # calculate movie1 fontsize based on text length
                if len(movie1[0]) > 35:
                    fontsize1 = 20
                else:
                    fontsize1 = 55 - len(movie1[0])
                movie1font = pygame.font.SysFont('Corbel', fontsize1)
                movie1text = movie1font.render(movie1[0], True, (0, 0, 0))
                movie1rect = movie1text.get_rect()
                movie1rect.center = (275, 550)

                # calculate movie2 fontsize based on text length
                if len(movie2[0]) > 35:
                    fontsize2 = 20
                else:
                    fontsize2 = 55 - len(movie2[0])
                movie2font = pygame.font.SysFont('ariel', fontsize2)
                movie2text = movie2font.render(movie2[0], True, (0, 0, 0))
                movie2rect = movie2text.get_rect()
                movie2rect.center = (725, 550)

                # rating
                ratingfont = pygame.font.SysFont('ariel', 30)
                ratingtext = ratingfont.render("Rating:" + movie1[1], True, (0, 0, 0))
                rating_rect = ratingtext.get_rect()
                rating_rect.center = (275, 625)

                # put the first two movies and their titles on the screen
                DISPLAYSURF.blit(image1, (125, 50))
                DISPLAYSURF.blit(movie1text, movie1rect)
                DISPLAYSURF.blit(image2, (575, 50))
                DISPLAYSURF.blit(movie2text, movie2rect)

                # put movie 1's rating on the screen
                DISPLAYSURF.blit(ratingtext, rating_rect)

                # score counter
                scoretext = scorefont.render(str(c), True, (0, 0, 0))
                scoretext_rect = scoretext.get_rect()
                scoretext_rect.center = (500,50)
                DISPLAYSURF.blit(scoretext, scoretext_rect)
                exited_start_menu = False
                alive = True
            # click lower and correct
            if 575 <= mouse[0] <= 705 and 600 <= mouse[1] <= 650 and answer == "Lower" and alive:
                # blot out the entire screen to add new values for everything
                pygame.draw.rect(DISPLAYSURF, (255, 255, 255), (0, 0, 1000, 750))
                # update the scorecard
                c += 1
                scoretext = scorefont.render(str(c), True, (0, 0, 0))
                scoretext_rect = scoretext.get_rect()
                scoretext_rect.center = (500,50)
                DISPLAYSURF.blit(scoretext, scoretext_rect)

                # lower button
                pygame.draw.rect(DISPLAYSURF, (50, 205, 50), (575, 600, 130, 50))
                DISPLAYSURF.blit(lowertext, lowertext_rect)

                # higher button
                pygame.draw.rect(DISPLAYSURF, (220, 20, 60), (745, 600, 130, 50))
                DISPLAYSURF.blit(highertext, highertext_rect)

                # update movie2 to be the new movie1
                movie1 = movie2
                img1 = urlopen(movie1[2]).read()
                image_file1 = io.BytesIO(img1)
                image1 = pygame.image.load(image_file1)
                image1 = pygame.transform.scale(image1, (300, 450))

                if len(movie1[0]) > 35:
                    fontsize1 = 20
                else:
                    fontsize1 = 55 - len(movie1[0])
                movie1font = pygame.font.SysFont('Corbel', fontsize1)
                movie1text = movie1font.render(movie1[0], True, (0, 0, 0))
                movie1rect = movie1text.get_rect()
                movie1rect.center = (275, 550)

                DISPLAYSURF.blit(image1, (125, 50))
                DISPLAYSURF.blit(movie1text, movie1rect)

                ratingtext = ratingfont.render("Rating:" + movie1[1], True, (0, 0, 0))
                rating_rect = ratingtext.get_rect()
                rating_rect.center = (275, 625)
                DISPLAYSURF.blit(ratingtext, rating_rect)

                # now get a new movie2
                movie2 = Funcs.get_movie(
                    "https://letterboxd.com/joeibanez/list/the-100-most-watched-films-on-letterboxd/by/shuffle/")
                while movie2[0] == movie1[0] or movie2[1] == movie1[1]:
                    movie2 = Funcs.get_movie(
                        "https://letterboxd.com/joeibanez/list/the-100-most-watched-films-on-letterboxd/by"
                        "/shuffle/")

                img2 = urlopen(movie2[2]).read()
                image_file2 = io.BytesIO(img2)
                image2 = pygame.image.load(image_file2)
                image2 = pygame.transform.scale(image2, (300, 450))

                if len(movie2[0]) > 35:
                    fontsize2 = 20
                else:
                    fontsize2 = 55 - len(movie2[0])
                movie2font = pygame.font.SysFont('ariel', fontsize2)
                movie2text = movie2font.render(movie2[0], True, (0, 0, 0))
                movie2rect = movie2text.get_rect()
                movie2rect.center = (725, 550)

                DISPLAYSURF.blit(image2, (575, 50))
                DISPLAYSURF.blit(movie2text, movie2rect)
            # click higher and correct
            if 745 <= mouse[0] <= 875 and 600 <= mouse[1] <= 650 and answer == "Higher" and alive:
                # blot out the entire screen to add new values for everything
                pygame.draw.rect(DISPLAYSURF, (255, 255, 255), (0, 0, 1000, 750))
                # update the scorecard
                c += 1
                scoretext = scorefont.render(str(c), True, (0, 0, 0))
                scoretext_rect = scoretext.get_rect()
                scoretext_rect.center = (500, 50)
                DISPLAYSURF.blit(scoretext, scoretext_rect)

                # lower button
                pygame.draw.rect(DISPLAYSURF, (50, 205, 50), (575, 600, 130, 50))
                DISPLAYSURF.blit(lowertext, lowertext_rect)

                # higher button
                pygame.draw.rect(DISPLAYSURF, (220, 20, 60), (745, 600, 130, 50))
                DISPLAYSURF.blit(highertext, highertext_rect)

                # update movie2 to be the new movie1
                movie1 = movie2
                img1 = urlopen(movie1[2]).read()
                image_file1 = io.BytesIO(img1)
                image1 = pygame.image.load(image_file1)
                image1 = pygame.transform.scale(image1, (300, 450))

                if len(movie1[0]) > 35:
                    fontsize1 = 20
                else:
                    fontsize1 = 55 - len(movie1[0])
                movie1font = pygame.font.SysFont('Corbel', fontsize1)
                movie1text = movie1font.render(movie1[0], True, (0, 0, 0))
                movie1rect = movie1text.get_rect()
                movie1rect.center = (275, 550)

                DISPLAYSURF.blit(image1, (125, 50))
                DISPLAYSURF.blit(movie1text, movie1rect)

                ratingtext = ratingfont.render("Rating:" + movie1[1], True, (0, 0, 0))
                rating_rect = ratingtext.get_rect()
                rating_rect.center = (275, 625)
                DISPLAYSURF.blit(ratingtext, rating_rect)

                # now get a new movie2
                movie2 = Funcs.get_movie(
                    "https://letterboxd.com/joeibanez/list/the-100-most-watched-films-on-letterboxd/by/shuffle/")
                while movie2[0] == movie1[0] or movie2[1] == movie1[1]:
                    movie2 = Funcs.get_movie(
                        "https://letterboxd.com/joeibanez/list/the-100-most-watched-films-on-letterboxd/by"
                        "/shuffle/")

                img2 = urlopen(movie2[2]).read()
                image_file2 = io.BytesIO(img2)
                image2 = pygame.image.load(image_file2)
                image2 = pygame.transform.scale(image2, (300, 450))

                if len(movie2[0]) > 35:
                    fontsize2 = 20
                else:
                    fontsize2 = 55 - len(movie2[0])
                movie2font = pygame.font.SysFont('ariel', fontsize2)
                movie2text = movie2font.render(movie2[0], True, (0, 0, 0))
                movie2rect = movie2text.get_rect()
                movie2rect.center = (725, 550)

                DISPLAYSURF.blit(image2, (575, 50))
                DISPLAYSURF.blit(movie2text, movie2rect)
            # click lower and wrong
            if 575 <= mouse[0] <= 705 and 600 <= mouse[1] <= 650 and answer != "Lower" and alive:
                alive = False
                # blot out everything
                pygame.draw.rect(DISPLAYSURF, (255, 255, 255), (0, 0, 1000, 750))

                # display and reset the score
                final_score_text = menufont.render('Your Final Score:' + str(c), True, (0, 0, 0))
                final_score_rect = final_score_text.get_rect()
                final_score_rect.center = (500, 300)
                DISPLAYSURF.blit(final_score_text, final_score_rect)
                highscore = max(highscore, c)
                highscore_text = menufont.render('Your High Score:' + str(highscore), True, (0, 0, 0))
                highscore_rect = highscore_text.get_rect()
                highscore_rect.center = (500, 200)
                DISPLAYSURF.blit(highscore_text, highscore_rect)
                c = 0

                # display the play button again
                pygame.draw.rect(DISPLAYSURF, silver, (350, 400, 300, 75))
                DISPLAYSURF.blit(play_text, play_text_rect)

                # display the how to play button again
                pygame.draw.rect(DISPLAYSURF, silver, (350, 500, 300, 75))
                DISPLAYSURF.blit(instructions_text, instructions_text_rect)
            # click higher and wrong
            if 745 <= mouse[0] <= 875 and 600 <= mouse[1] <= 650 and answer != "Higher" and alive:
                alive = False
                # blot out everything
                pygame.draw.rect(DISPLAYSURF, (255, 255, 255), (0, 0, 1000, 750))

                # display and reset the score
                final_score_text = menufont.render('Your Final Score:' + str(c), True, (0, 0, 0))
                final_score_rect = final_score_text.get_rect()
                final_score_rect.center = (500, 300)
                DISPLAYSURF.blit(final_score_text, final_score_rect)
                highscore = max(highscore, c)
                highscore_text = menufont.render('Your High Score:' + str(highscore), True, (0, 0, 0))
                highscore_rect = highscore_text.get_rect()
                highscore_rect.center = (500, 200)
                DISPLAYSURF.blit(highscore_text, highscore_rect)
                c = 0

                # display the play button again
                pygame.draw.rect(DISPLAYSURF, silver, (350, 400, 300, 75))
                DISPLAYSURF.blit(play_text, play_text_rect)

                # display the how to play button again
                pygame.draw.rect(DISPLAYSURF, silver, (350, 500, 300, 75))
                DISPLAYSURF.blit(instructions_text, instructions_text_rect)
            # click the how to play button
            if 350 <= mouse[0] <= 650 and 500 <= mouse[1] <= 575 and not alive:
                # reset the screen
                pygame.draw.rect(DISPLAYSURF, (255, 255, 255), (0, 0, 1000, 750))

                # display text of instructions
                instruction1 = instructions_font.render("High and Low Boxd is a game to test your knowledge of films."
                                                        , True, (0,0,0))
                instruction2 = instructions_font.render("More specifically, test your knowledge of letterboxd's database"
                                                        " of films and ratings", True, (0,0,0))
                instruction3 = instructions_font.render('To play, click "Start Game"'
                                                        "and you'll be given two movies.", True, (0,0,0))
                instruction4 = instructions_font.render("The objective is to "
                                                        "determine if the movie on the right has a higher or lower "
                                                        "rating on letterboxd.com.", True, (0,0,0))
                DISPLAYSURF.blit(instruction1, (50, 100))
                DISPLAYSURF.blit(instruction2, (50, 175))
                DISPLAYSURF.blit(instruction3, (50, 250))
                DISPLAYSURF.blit(instruction4, (50, 325))

                # display the play button
                pygame.draw.rect(DISPLAYSURF, silver, (350, 400, 300, 75))
                DISPLAYSURF.blit(play_text, play_text_rect)
    pygame.display.update()
