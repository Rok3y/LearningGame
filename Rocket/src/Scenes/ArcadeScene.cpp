#include "ArcadeScene.h"
#include "Screen.h"
#include "AARectangle.h"
#include "Triangle.h"
#include "Circle.h"
#include "Color.h"
#include "Line2D.h"
#include "GameController.h"
#include <iostream>

ArcadeScene::ArcadeScene(uint32_t width, uint32_t height)
	:mWidth(width), mHeight(height), mRect(Vec2D(100, 100), 50, 50)
{
	mBoundary.SetTopLeftPoint(Vec2D::Zero);
	mBoundary.SetBottomRightPoint(Vec2D(mWidth-1, mHeight-1));
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

	mRect.SetCollideWithEdge(true);
	mRect.SetScreenBoundary(mBoundary);
	mRect.SetVelocity(Vec2D(-100.0f, 20.0f));
}

void ArcadeScene::Update(uint32_t dt)
{
	mRect.Update(dt);
}

void ArcadeScene::Draw(Screen& screen)
{
	screen.Draw(mBoundary, Color::Red());

	mRect.Draw(screen);

}

const std::string& ArcadeScene::GetSceneName() const
{
	static std::string sceneName = "Arcade";
	return sceneName;
}
