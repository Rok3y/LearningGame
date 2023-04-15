#include "BreakOut.h"
#include <iostream>
#include "GameController.h"
#include "App.h"

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
	controller.ClearAll();
	ResetGame();

	ButtonAction leftKeyAction;
	leftKeyAction.key = GameController::LeftKey();
	leftKeyAction.action = [this](uint32_t dt, InputState state)
	{
		if (GameController::IsPressed(state))
		{
			mPaddle.SetMovementDirection(PaddleDirection::LEFT);
		}
		else
		{
			mPaddle.UnsetMovementDirection(PaddleDirection::LEFT);
		}
	};

	controller.AddInputActionForKey(leftKeyAction);

	ButtonAction rightKeyAction;
	rightKeyAction.key = GameController::RightKey();
	rightKeyAction.action = [this](uint32_t dt, InputState state)
	{
		if (GameController::IsPressed(state))
		{
			mPaddle.SetMovementDirection(PaddleDirection::RIGHT);
		}
		else
		{
			mPaddle.UnsetMovementDirection(PaddleDirection::RIGHT);
		}
	};

	controller.AddInputActionForKey(rightKeyAction);
}

void BreakOut::Update(uint32_t dt)
{
	mPaddle.Update(dt);
}

void BreakOut::Draw(Screen& screen)
{
	mPaddle.Draw(screen);
}

std::string BreakOut::GetName() const
{
	return "Break out!";
}

void BreakOut::ResetGame()
{
	AARectangle paddleRect = { Vec2D(App::Singleton().Width() / 2 - Paddle::PADDLE_WIDTH / 2, App::Singleton().height() - 3 * Paddle::PADDLE_HEIGHT), Paddle::PADDLE_WIDTH, Paddle::PADDLE_HEIGHT };
	AARectangle levelBoundary = { Vec2D::Zero, App::Singleton().Width(), App::Singleton().height() };

	mPaddle.Init(paddleRect, levelBoundary);
}