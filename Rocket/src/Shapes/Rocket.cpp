#include "Rocket.h"
#include "Utils.h"
#include "Vec2D.h"

Rocket::Rocket()
    : mPosition(Vec2D(0, 0)), mWidth(10), mHeight(10), mRocketTipHeight(10), mRocketLines()
{

}

Rocket::Rocket(const Vec2D& position, int width, int height, int tipHeight)
    : mPosition(position), mWidth(width), mHeight(height), mRocketTipHeight(tipHeight), mRocketLines()
{
    createGeometry();
}

void Rocket::MoveTo(const Vec2D& p)
{
}

void Rocket::RotateAroundCenter(float angle)
{
    Rotate(angle, mPoints.back()); // Last point is reserved for storing center of mass
}

void Rocket::Rotate(float angle, const Vec2D& aroundPoint)
{
    mPoints.at(0).Rotate(angle, aroundPoint);
    mPoints.at(1).Rotate(angle, aroundPoint);
    mPoints.at(2).Rotate(angle, aroundPoint);
    mPoints.at(3).Rotate(angle, aroundPoint);
    mPoints.at(4).Rotate(angle, aroundPoint);

    mRocketLines.at(0).SetP0(mPoints.at(0));
    mRocketLines.at(0).SetP1(mPoints.at(1));

    mRocketLines.at(1).SetP0(mPoints.at(1));
    mRocketLines.at(1).SetP1(mPoints.at(2));

    mRocketLines.at(2).SetP0(mPoints.at(2));
    mRocketLines.at(2).SetP1(mPoints.at(3));

    mRocketLines.at(3).SetP0(mPoints.at(3));
    mRocketLines.at(3).SetP1(mPoints.at(4));

    mRocketLines.at(4).SetP0(mPoints.at(4));
    mRocketLines.at(4).SetP1(mPoints.at(0));
}

void Rocket::calculateCenterOfMass()
{
    double area = 0.0;
    double Cx = 0.0;
    double Cy = 0.0;
    size_t n = mPoints.size();

    for (size_t i = 0; i < n; ++i) {
        double x0 = mPoints[i].GetX();
        double y0 = mPoints[i].GetY();
        double x1 = mPoints[(i + 1) % n].GetX();
        double y1 = mPoints[(i + 1) % n].GetY();

        double cross = x0 * y1 - x1 * y0;
        area += cross;
        Cx += (x0 + x1) * cross;
        Cy += (y0 + y1) * cross;
    }

    area *= 0.5;
    Cx /= (6.0 * area);
    Cy /= (6.0 * area);

    mCenterOfMass = Vec2D(Cx, Cy);
}

void Rocket::createGeometry()
{
    mRocketLines.clear();
    float leftSide = mPosition.GetX() - (mWidth / 2);
    float rightSide = mPosition.GetX() + (mWidth / 2);

    if (mPoints.empty())
    {
        mPoints.push_back(mPosition); // Tip of the rocket
        mPoints.push_back(Vec2D(leftSide, mPosition.GetY() - mRocketTipHeight));
        mPoints.push_back(Vec2D(leftSide, mPosition.GetY() - mHeight - mRocketTipHeight));
        mPoints.push_back(Vec2D(rightSide, mPosition.GetY() - mHeight - mRocketTipHeight));
        mPoints.push_back(Vec2D(rightSide, mPosition.GetY() - mRocketTipHeight));
    }

    Line2D line1 = Line2D(mPoints.at(0), mPoints.at(1));
    Line2D line2 = Line2D(mPoints.at(1), mPoints.at(2));
    Line2D line3 = Line2D(mPoints.at(2), mPoints.at(3));
    Line2D line4 = Line2D(mPoints.at(3), mPoints.at(4));
    Line2D line5 = Line2D(mPoints.at(4), mPoints.at(0));

    mRocketLines.push_back(line1);
    mRocketLines.push_back(line2);
    mRocketLines.push_back(line3);
    mRocketLines.push_back(line4);
    mRocketLines.push_back(line5);

    calculateCenterOfMass();
    mPoints.push_back(mCenterOfMass); // Last point in points vector will not contribute to drawing but to mass information
}