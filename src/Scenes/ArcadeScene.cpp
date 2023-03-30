#include "ArcadeScene.h"
#include "Screen.h"
#include "AARectangle.h"
#include "Triangle.h"
#include "Circle.h"
#include "Color.h"
#include "Line2D.h"
#include "GameController.h"
#include <iostream>
#include "ChessBoard.h"
#include "Pawn.h"

ArcadeScene::ArcadeScene()
{

}

void ArcadeScene::Init()
{
	ButtonAction action;
	action.key = GameController::ActionKey();
	action.action = [](uint32_t dt, InputState state)
	{
		if (GameController::IsPressed(state))
		{
			std::cout << "Action button was pressed" << std::endl;
		}
	};

	mGameController.AddInputActionForKey(action);


	MouseButtonAction mouseAction;
	mouseAction.mouseButton = GameController::LeftMouseButton();
	mouseAction.mouseInputAction = [](InputState state, const MousePosition& pos)
	{
		if (GameController::IsPressed(state))
		{
			std::cout << "Left mouse button pressed!" << std::endl;
		}
	};

	mGameController.AddMouseButtonAction(mouseAction);
	mGameController.SetMouseMovedAction([](const MousePosition& mousePosition)
		{
			std::cout << "Mouse position x: " << mousePosition.xPos << ", Y: " << mousePosition.yPos << std::endl;
		});
}

void ArcadeScene::Update(uint32_t dt)
{

}

void ArcadeScene::Draw(Screen& theScreen)
{
	//Line2D line = { Vec2D(0,0), Vec2D(theScreen.Width(), theScreen.Height()) };
	//Triangle triangle = { Vec2D(60, 10), Vec2D(10, 110), Vec2D(110, 110) };
	//AARectangle rect = { Vec2D(theScreen.Width() / 2 - 25, theScreen.Height() / 2 - 25), 50, 50 };
	//Circle circle = { Vec2D(theScreen.Width() / 2 + 50, theScreen.Height() / 2 + 50), 50 };

	//theScreen.Draw(line, Color::White());
	//theScreen.Draw(triangle, Color::Red(), true, Color::Red());
	//theScreen.Draw(rect, Color::Blue(), true, Color::Blue());
	//theScreen.Draw(circle, Color(0, 255, 0, 150), true, Color(0, 255, 0, 150));

	// Move creation out of draw method
	ChessBoard board = { theScreen.Width(), theScreen.Height()};

	int counter = 0;
	int fillPolly = false;
	for (const AARectangle& rect : board.GetBoardRectangles())
	{
		theScreen.Draw(rect, Color::White(), fillPolly, Color::White());
		counter++;

		if (counter % 8 == 0)
		{
			continue;
		}

		fillPolly = ~fillPolly;
	}

	board.Init();
	std::vector<Line2D> pawnLines = static_cast<Pawn*>(board.GetPieces().at(0))->GetLines();

	for (Line2D& line : pawnLines)
	{
		theScreen.Draw(line, Color::Magenta());
	}
	
}

const std::string& ArcadeScene::GetSceneName() const
{
	static std::string sceneName = "Arcade Sceen";
	return sceneName;
}

std::unique_ptr<Scene> ArcadeScene::GetScene(eGame game)
{
	switch (game)
	{
	case TETRIS:
		{

		}
		break;
	case BREAK_OUT:
		{

		}
		break;
	case ASTEROIDS:
		{

		}
		break;
	case PACMAN:
		{

		}
		break;
	case NUM_GAMES:
		{

		}
		break;
	default:
		{

		}
		break;
	}

	return nullptr;
}