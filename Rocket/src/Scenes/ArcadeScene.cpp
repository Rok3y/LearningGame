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
	:mWidth(width), mHeight(height), mRocket(Vec2D(100, 100), 25, 50), mGravity(Vec2D::Zero), mHeavyRocket(Vec2D(200, 100), 25, 50)
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

	// Earth's gravity force (mass times gravity acceleration 9.81 m/s^2
	mGravity.SetY(9.81);

	mRocket.SetCollideWithEdge(true);
	mRocket.SetScreenBoundary(mBoundary);
	mRocket.SetVelocity(Vec2D(-0.0f, 20.0f)); // Some random push
	mRocket.SetMass(1);

	mHeavyRocket.SetCollideWithEdge(true);
	mHeavyRocket.SetScreenBoundary(mBoundary);
	mHeavyRocket.SetVelocity(Vec2D(-0.0f, 20.0f)); // Some random push
	mHeavyRocket.SetMass(10);
}

void ArcadeScene::Update(uint32_t dt)
{
	Vec2D mRocketForce = Vec2D(mRocket.GetMass() * mGravity.GetX(), mRocket.GetMass() * mGravity.GetY());
	Vec2D mHeavyRocketForce = Vec2D(mHeavyRocket.GetMass() * mGravity.GetX(), mHeavyRocket.GetMass() * mGravity.GetY());

	mRocket.SetAcceleration(mRocketForce);
	mRocket.Update(dt);

	mHeavyRocket.SetAcceleration(mHeavyRocketForce);
	mHeavyRocket.Update(dt);
}

void ArcadeScene::Draw(Screen& screen)
{
	screen.Draw(mBoundary, Color::Red());

	mRocket.Draw(screen);
	mHeavyRocket.Draw(screen);

}

const std::string& ArcadeScene::GetSceneName() const
{
	static std::string sceneName = "Arcade";
	return sceneName;
}
