# Chess-Project
A Python implementation of a variation of chess

## Project timeline and technologies used

I coded this chess game over the course of two weeks to showcase my technical skillset.
The chess game is entirely in Python and I utilized GitHub for version control.

## Description

The chess game and the chess pieces are represented as objects in the program, so the details about either the game or the pieces are obtained through get methods that return the desired private data members. A method in the chess game class is used to move pieces around the board by the starting square and destination square coordinates string parameters. The method moves the pieces recursivley and checks the legality of the move in each recursive call. In addition, the game state and turn system is updated by this method as well.

The chess pieces are represented in one class and the data members are modified based on the name of the piece given to the initializer method, including a move sets and movement limits to be used by the chess game object. This variation of chess also features fairy pieces such as the hunter and the falcon which uses a method to check that the piece is able to be played (after losing a special chess piece and must be initialized on the two home ranks).

Currently the board is displayed to the user as a string. However, there may be plans to improve the user interface of the chess game.
