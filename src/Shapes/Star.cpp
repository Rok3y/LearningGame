#include "Star.h"
#include "Utils.h"
#include "Vec2D.h"

Star::Star()
	: mPosition(Vec2D(0, 0)), mSize(1), mStarPoints(), mStarLines()
{

}

Star::Star(const Vec2D& position, int size)
	: mPosition(position), mSize(size), mStarPoints(), mStarLines()
{
    Vec2D center = position;
    float radRotate = DegToRad(72);

    mStarPoints.push_back(Vec2D(center.GetX(), center.GetY() - mSize));
    mStarPoints.push_back(mStarPoints.at(0).RotationResult(radRotate, center));
    mStarPoints.push_back(mStarPoints.at(1).RotationResult(radRotate, center));
    mStarPoints.push_back(mStarPoints.at(2).RotationResult(radRotate, center));
    mStarPoints.push_back(mStarPoints.at(3).RotationResult(radRotate, center));

    Line2D line1 = Line2D(mStarPoints.at(0), mStarPoints.at(2));
    Line2D line2 = Line2D(mStarPoints.at(2), mStarPoints.at(4));
    Line2D line3 = Line2D(mStarPoints.at(4), mStarPoints.at(1));
    Line2D line4 = Line2D(mStarPoints.at(1), mStarPoints.at(3));
    Line2D line5 = Line2D(mStarPoints.at(3), mStarPoints.at(0));

    mStarLines.push_back(line1);
    mStarLines.push_back(line2);
    mStarLines.push_back(line3);
    mStarLines.push_back(line4);
    mStarLines.push_back(line5);
}


void Star::RotateAroundCenter(float angle)
{
    Rotate(angle, mPosition);
}

void Star::Rotate(float angle, const Vec2D& aroundPoint)
{
    mStarPoints.at(0).Rotate(angle, aroundPoint);
    mStarPoints.at(1).Rotate(angle, aroundPoint);
    mStarPoints.at(2).Rotate(angle, aroundPoint);
    mStarPoints.at(3).Rotate(angle, aroundPoint);
    mStarPoints.at(4).Rotate(angle, aroundPoint);

    mStarLines.at(0).SetP0(mStarPoints.at(0));
    mStarLines.at(0).SetP1(mStarPoints.at(2));

    mStarLines.at(1).SetP0(mStarPoints.at(2));
    mStarLines.at(1).SetP1(mStarPoints.at(4));

    mStarLines.at(2).SetP0(mStarPoints.at(4));
    mStarLines.at(2).SetP1(mStarPoints.at(1));

    mStarLines.at(3).SetP0(mStarPoints.at(1));
    mStarLines.at(3).SetP1(mStarPoints.at(3));

    mStarLines.at(4).SetP0(mStarPoints.at(3));
    mStarLines.at(4).SetP1(mStarPoints.at(0));
}