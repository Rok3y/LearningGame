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
	:mBoard(nullptr)
{

}

void ArcadeScene::Init()
{
	mBoard = std::make_unique<ChessBoard>();
	mBoard->Init();

	//uint32_t rectWidth = mWidth / 8;
	//uint32_t rectHeight = mHeight / 8;
	
	//for (int i = 0; i < 8; i++)
	//{
	//	for (int j = 0; j < 8; j++)
	//	{
	//		//mRectangles.push_back(AARectangle(Vec2D((mTopLeftStartingPosition.GetX() + rectWidth * i), (mTopLeftStartingPosition.GetY() + rectHeight * j)), rectWidth, rectHeight));
	//		mRectangles.emplace_back(AARectangle(Vec2D(i, j), 0, 0));
	//	}
	//}

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
	std::vector<AARectangle> boardPositions = mBoard->GetBoardRectangles();

	int counter = 0;
	int fillPolly = false;
	for (const AARectangle& rect : boardPositions)
	{
		theScreen.Draw(rect.GetCenterPoint(), Color::Red());
		theScreen.Draw(rect, Color::Blue(), fillPolly, Color::White());
		counter++;

		if (counter % 8 == 0)
		{
			continue;
		}

		fillPolly = ~fillPolly;

	}

	auto pieces = mBoard->GetPieces();
	if (pieces.empty())
	{
		return;
	}
	std::shared_ptr<ChessPiece> piece1 = pieces[0][0];
	theScreen.Draw(piece1, Color::Magenta(), true, Color::Cyan());

	Vec2D piecePoint = piece1->GetCenterPoint();
	theScreen.Draw(piecePoint, Color::Red());

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