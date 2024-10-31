#include "Rocketship.h"
#include "Utils.h"
#include "Screen.h"
#include "Color.h"

Rocketship::Rocketship(const Vec2D& pos, uint32_t width, uint32_t height, uint32_t tipRocket)
	: mRocket(pos, width, height, tipRocket)
{
	mVelocity = Vec2D::Zero;
	mAcceleration = Vec2D::Zero;
}

void Rocketship::SetPosition(const Vec2D& pos)
{
	mRocket.MoveTo(pos);
}

void Rocketship::SetVelocity(const Vec2D& vel)
{
	mVelocity = vel;
}

void Rocketship::SetAcceleration(const Vec2D& acc)
{
	mAcceleration = acc;
}

void Rocketship::Update(uint32_t dt)
{
	// Modify velocity by acceleration

	Vec2D dx = mVelocity * MillisecondsToSeconds(dt);
	mRocket.MoveBy(dx);


	for each (Vec2D point in mRocket.GetPoints())
	{
		//Rocket tip with left side wall
		if (point.GetX() < mBoundary.GetTopLeftPoint().GetX())
		{
			uint32_t offset = mBoundary.GetTopLeftPoint().GetX() - point.GetX();
			mRocket.MoveBy(Vec2D(offset, 0));

			Vec2D leftEdgeNormal = Vec2D(1, 0);
			mVelocity = CalculateReflectingVector(leftEdgeNormal);
			return;
		}

		// Rocket tip with right side wall
		if (point.GetX() > mBoundary.GetBottomRightPoint().GetX())
		{
			int offset = mBoundary.GetBottomRightPoint().GetX() - point.GetX();
			mRocket.MoveBy(Vec2D(offset, 0));

			Vec2D rightEdgeNormal = Vec2D(-1, 0);
			mVelocity = CalculateReflectingVector(rightEdgeNormal);
			return;
		}

		// Rocket tip with top border
		if (point.GetY() < mBoundary.GetTopLeftPoint().GetY())
		{
			uint32_t offset = mBoundary.GetTopLeftPoint().GetY() - point.GetY();
			mRocket.MoveBy(Vec2D(0, offset));


			Vec2D topEdgeNormal = Vec2D(0, 1);
			mVelocity = CalculateReflectingVector(topEdgeNormal);
			return;
		}

		// Rocket tip with bottom edge
		if (point.GetY() > mBoundary.GetBottomRightPoint().GetY())
		{
			int offset = mBoundary.GetBottomRightPoint().GetY() - point.GetY();
			mRocket.MoveBy(Vec2D(0, offset));


			Vec2D bottomEdgeNormal = Vec2D(0, -1);
			mVelocity = CalculateReflectingVector(bottomEdgeNormal);
			return;
		}
	}
}

void Rocketship::Rotate(float rad)
{
	mRocket.RotateAroundCenter(rad);
}

void Rocketship::Draw(Screen& screen)
{
	screen.Draw(mRocket, Color::Cyan(), true, Color::Blue());
}