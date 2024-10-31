#include "Particle.h"
#include "Utils.h"
#include "Screen.h"
#include "Color.h"

Particle::Particle(const Vec2D& pos, uint32_t width, uint32_t height)
	: mRect(pos, width, height)
{
	mVelocity = Vec2D::Zero;
	mAcceleration = Vec2D::Zero;
}

void Particle::SetPosition(const Vec2D& pos)
{
	mRect.MoveTo(pos);
}

void Particle::SetVelocity(const Vec2D& vel)
{
	mVelocity = vel;
}

void Particle::SetAcceleration(const Vec2D& acc)
{
	mAcceleration = acc;
}

void Particle::SetMass(float mass)
{
	mMass = mass;
}

void Particle::Update(uint32_t dt)
{
	// Modify velocity by acceleration

	Vec2D acceleration = 

	mVelocity += mAcceleration;

	Vec2D dx = mVelocity * MillisecondsToSeconds(dt);
	mRect.MoveBy(dx);

	// Check boundary
	if (mRect.GetTopLeftPoint().GetX() < mBoundary.GetTopLeftPoint().GetX())
	{
		uint32_t offset = mBoundary.GetTopLeftPoint().GetX() - mRect.GetTopLeftPoint().GetX();
		mRect.MoveBy(Vec2D(offset, 0));

		Vec2D leftEdgeNormal = Vec2D(1, 0);
		mVelocity = CalculateReflectingVector(leftEdgeNormal);
	}

	if (mRect.GetTopLeftPoint().GetY() < mBoundary.GetTopLeftPoint().GetY())
	{
		uint32_t offset = mBoundary.GetTopLeftPoint().GetY() - mRect.GetTopLeftPoint().GetY();
		mRect.MoveBy(Vec2D(0, offset));


		Vec2D topEdgeNormal = Vec2D(0, 1);
		mVelocity = CalculateReflectingVector(topEdgeNormal);
	}

	if (mRect.GetBottomRightPoint().GetX() > mBoundary.GetBottomRightPoint().GetX())
	{
		int offset = mBoundary.GetBottomRightPoint().GetX() - mRect.GetBottomRightPoint().GetX();
		mRect.MoveBy(Vec2D(offset, 0));

		Vec2D rightEdgeNormal = Vec2D(-1, 0);
		mVelocity = CalculateReflectingVector(rightEdgeNormal);
	}

	if (mRect.GetBottomRightPoint().GetY() > mBoundary.GetBottomRightPoint().GetY())
	{
		int offset = mBoundary.GetBottomRightPoint().GetY() - mRect.GetBottomRightPoint().GetY();
		mRect.MoveBy(Vec2D(0, offset));


		Vec2D bottomEdgeNormal = Vec2D(0, -1);
		mVelocity = CalculateReflectingVector(bottomEdgeNormal);
	}
}

void Particle::Draw(Screen& screen)
{
	screen.Draw(mRect, Color::Cyan(), true, Color::Blue());
}