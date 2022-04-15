from email.headerregistry import Address
from shutil import move
import socket
import threading
from tkinter import Y
from turtle import ycor

from numpy import true_divide


class TicTacToe:
    def __init__(self):
        self.board = [[" "," "," "],[" "," "," "],[" "," "," "]]
        self.turn = "X"
        self.you = "X"
        self.opponent = "O"
        self.winner = None
        self.gameover = False

        self.counter = 0
    def host_game(self,host,port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client, addr = server.accept()

        self.you = "X"
        self.opponent = "O"
        threading.Thread (target=self.handle_connection, args=(client,)).start()
        server.close()

    def connect_to_game (self,host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        self.you = 'o'
        self.opponent = 'X'
        threading.Thread (target=self.handle_connection, args=(client,)).start()

    def handle_connection(self,client):
        while not self.gameover:
            if self.turn == self.you:
                move = input("enter a move (row,column): ")
                if self.check_valid_move(move.split(',')):
                    client.send(move.encode('utf-8'))
                    self.apply_move(move.split(','),self.you)
                    self.turn = self.opponent
                    
                else:
                    print("invalid move")
            else:
                data = client.recv(1024)
                if not data:
                    
                    break
                else:
                    self.apply_move(data.decode('utf-8').split(','), self.opponent)
                    self.turn = self.you
            
        client.close()
    
    def apply_move(self, move, player):
        if self.gameover:
            return
        self.counter += 1
        self.board[int(move[0])][int(move[1])] = player
        self.print_board()
        if self.check_if_won():
            if self.winner == self.you:
                print("you win!")
                exit()
            elif self.winner == self.opponent:
                print("you lose!")
                exit()

        else:
            if self.counter == 9:
                print("it is a tie!")
                exit()
    def check_valid_move(self,move):
        print("invalid move")
        return self.board[int(move[0])][int(move[1])] == " "

    def check_if_won(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.gameover = True
                return True
        
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                self.gameover = True
                return True

        if self.board [0][0] == self.board [1][1] == self.board [2][2] != " ":
            self.winner = self.board[0][0]
            self.gameover = True
            return True
        
        if self.board [0][2] == self.board [1][1] == self.board [2][0] != " ":
            self.winner = self.board[0][2]
            self.gameover = True
            return True
        
        return False

    def print_board(self):
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row != 2:
                print("-------------")
        


game = TicTacToe()
game.host_game('localhost',9999)

