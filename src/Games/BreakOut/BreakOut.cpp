#include "BreakOut.h"
#include <iostream>

/*

	Paddle
		- Can move side to side (by the user)
		- Stops at the edge of the screen
		- Width and Height
		- Bounces the ball
			- Bounces the ball differentlybased on the position that was hit on the paddle

	 Ball
		- Bounces off the walls and the paddle and the block
		- Width and height
		- Velocity position

	Block
		- part of the level
		- Has HP - One hit by the ball is -1 HP
		- Color and position, Width and height (AARectangle)
		- Bounces the ball

	Level
		- Container that holds all of the blck
		- Should be able to load a level from the levels.txt file
		- Handle collisions of the blocks?
		- Contain the walls/edges of the screens
		- Reset the level

	Game
		- Contains all of the objects (Paddle, Ball, Levels)
		- Player which has 3 lives
		- States - Serve the ball, In Game, Game Over
		- Reset the game

*/

void BreakOut::Init(GameController& controller)
{
	std::cout << "Break Out Game Init()" << std::endl;
}

void BreakOut::Update(uint32_t dt)
{
	std::cout << "Break Out Game Update()" << std::endl;
}

void BreakOut::Draw(Screen& screen)
{
	std::cout << "Break Out Game Draw()" << std::endl;
}

std::string BreakOut::GetName() const
{
	return "Break out!";
}
