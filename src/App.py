import random
import pygame
from src.Cell import Cell
from src.Board import Board
from src.Robot import Robot
from src.Player import Player
from src.consts import *
pygame.init()
class App:

    font1 = pygame.font.SysFont(None, 64)
    font2 = pygame.font.SysFont(None, 24)
    images_for_cell_coordinate =[pygame.font.SysFont(None, 48).render(str(i), True,(0,0,0)) for i in range(9)]

    def __init__(self, colors_map, targets_map, required_mail, number_robot_per_player, player_colors) -> None:

        self.screen = pygame.display.set_mode((DEFAULT_IMAGE_SIZE[0]*28, DEFAULT_IMAGE_SIZE[1]*11)) 
        pygame.display.set_caption('Robotics Board Game') 
        self.running = True 

        self.board = Board(colors_map, targets_map)
        self.required_mail = required_mail
        self.number_robot_per_player = number_robot_per_player
        self.number_players = len(player_colors)

        robot_cells_init = random.sample(self.board.white_cells, k = self.number_robot_per_player*len(player_colors))
        self.players = [Player(robot_cells_init[self.number_robot_per_player*i:self.number_robot_per_player*i+self.number_robot_per_player], player_color) 
                        for i, player_color in enumerate(player_colors)]

    def run(self):
        self.screen.fill((255, 255, 255))
        chosen_player = self.players[0]
        game_over = False
        while self.running:  
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    self.running = False
                
                if event.type == pygame.KEYDOWN and not game_over:

                    if event.key == pygame.K_f:
                        self.screen.fill((255, 255, 255))
                        if not any([robot.pos.color == "b" and robot.battery == MAXIMUM_ROBOT_BATTERY and robot.allowed_step_per_turn != 0 for robot in chosen_player.robots]):        
                            #change player: next player turn
                            chosen_player = self.players[(self.players.index(chosen_player)+1)%self.number_players]
                            for robot in chosen_player.robots:
                                robot.allowed_step_per_turn = 1
                        else:
                            img = self.font2.render("You can't skip your turn if you haven't moved all fully charged robot from blue cell", True,(0,0,0))
                            self.screen.blit(img, (9*DEFAULT_IMAGE_SIZE[0]+(18*DEFAULT_IMAGE_SIZE[0]-img.get_width())/2, 7*DEFAULT_IMAGE_SIZE[0]))

                    #it doesn't do anything if chosen_player is a Player
                    chosen_player.move(self.board)

                    if event.key == pygame.K_1 and self.number_robot_per_player >= 1:
                        chosen_player.chosen_robot = chosen_player.robots[0]

                    if event.key == pygame.K_2 and self.number_robot_per_player >= 2:
                        chosen_player.chosen_robot = chosen_player.robots[1]

                    if event.key == pygame.K_3 and self.number_robot_per_player >= 3:
                        chosen_player.chosen_robot = chosen_player.robots[2]

                    if event.key == pygame.K_4 and self.number_robot_per_player >= 4:
                        chosen_player.chosen_robot = chosen_player.robots[3]

                    if event.key == pygame.K_5 and self.number_robot_per_player >= 5:
                        chosen_player.chosen_robot = chosen_player.robots[4]

                    if event.key == pygame.K_UP:
                        if chosen_player.chosen_robot.move_up():
                            for blue_cell in self.board.blue_cells:
                                if blue_cell.robot:
                                    if blue_cell.robot is not chosen_player.chosen_robot:
                                        blue_cell.robot.charge() 

                    if event.key == pygame.K_DOWN:
                        if chosen_player.chosen_robot.move_down():
                            for blue_cell in self.board.blue_cells:
                                if blue_cell.robot:
                                    if blue_cell.robot is not chosen_player.chosen_robot:
                                        blue_cell.robot.charge() 

                    if event.key == pygame.K_RIGHT:
                        if chosen_player.chosen_robot.move_right():
                            for blue_cell in self.board.blue_cells:
                                if blue_cell.robot:
                                    if blue_cell.robot is not chosen_player.chosen_robot:
                                        blue_cell.robot.charge() 

                    if event.key == pygame.K_LEFT:
                        if chosen_player.chosen_robot.move_left():
                            for blue_cell in self.board.blue_cells:
                                if blue_cell.robot:
                                    if blue_cell.robot is not chosen_player.chosen_robot:
                                        blue_cell.robot.charge() 

            if chosen_player.count_mail == self.required_mail:
                game_over = True
                img = self.font1.render(f"Player {Robot.colors_map[chosen_player.color]} win", True, Cell.colors[chosen_player.color])
                self.screen.blit(img, (9*DEFAULT_IMAGE_SIZE[0]+(18*DEFAULT_IMAGE_SIZE[0]-img.get_width())/2, 0))

            for i in range(self.board.size):
                for j in range(self.board.size):
                    self.board[i][j].display(self.screen)

            for i in range(self.board.size):     
                    self.screen.blit(self.images_for_cell_coordinate[i], ((i+1)*DEFAULT_IMAGE_SIZE[0]+(DEFAULT_IMAGE_SIZE[0]-self.images_for_cell_coordinate[i].get_width())/2, 
                                                                          (DEFAULT_IMAGE_SIZE[1]-self.images_for_cell_coordinate[i].get_height())/2))
                    self.screen.blit(self.images_for_cell_coordinate[i], ((DEFAULT_IMAGE_SIZE[0]-self.images_for_cell_coordinate[i].get_width())/2, 
                                                                          (i+1)*DEFAULT_IMAGE_SIZE[1]+(DEFAULT_IMAGE_SIZE[1]-self.images_for_cell_coordinate[i].get_height())/2))

            for j in range(self.number_players*self.number_robot_per_player):
                for i in range(MAXIMUM_ROBOT_BATTERY+1):
                    rect = pygame.Rect(11*DEFAULT_IMAGE_SIZE[0]+i*CELL_BATTERY_SIZE[0], 
                                      (DEFAULT_IMAGE_SIZE[1]*11 - CELL_BATTERY_SIZE[1]*self.number_robot_per_player*self.number_players)/2 +j*CELL_BATTERY_SIZE[1], 
                                      CELL_BATTERY_SIZE[0], 
                                      CELL_BATTERY_SIZE[1])   
                    pygame.draw.rect(self.screen, (255,255,255), rect) 
                    pygame.draw.rect(self.screen, (0,0,0), rect, 1) 
            
            for i, player in enumerate(self.players):
                for robot in player.robots:
                    pygame.draw.circle(self.screen, Cell.colors[robot.color], 
                                       (11*DEFAULT_IMAGE_SIZE[0]+(robot.battery)*CELL_BATTERY_SIZE[0]+CELL_BATTERY_SIZE[0]/2,
                                       (DEFAULT_IMAGE_SIZE[1]*11 - CELL_BATTERY_SIZE[1]*self.number_robot_per_player*self.number_players)/2+(i*self.number_robot_per_player+robot.index-1)*CELL_BATTERY_SIZE[1]+CELL_BATTERY_SIZE[1]/2), 
                                       CELL_BATTERY_SIZE[0]/2*0.8, 0)
            
            pygame.draw.rect(self.screen, (255,0,0), ((chosen_player.chosen_robot.pos.x+1)*DEFAULT_IMAGE_SIZE[0], 
                                                    (chosen_player.chosen_robot.pos.y+1)*DEFAULT_IMAGE_SIZE[1], 
                                                    DEFAULT_IMAGE_SIZE[0], 
                                                    DEFAULT_IMAGE_SIZE[1]), 2) 
            pygame.display.update()
        
