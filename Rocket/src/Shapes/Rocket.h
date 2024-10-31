#ifndef SHAPES_ROCKET_H_
#define SHAPES_ROCKET_H_

#include <vector>

#include "Vec2D.h"
#include "Line2D.h"
#include "Shape.h"

class Rocket : public Shape
{
public:
	Rocket();
	Rocket(const Vec2D& position, int width, int height, int tipHeight);

	inline const Vec2D& GetCenterPosition() const { return mPosition; }
	inline const int GetWidth() const { return mWidth; }
	inline const int GetHeight() const { return mHeight; }
	inline const Vec2D& GetRocketTipPoint() const { return mPoints[0]; }
	inline const Vec2D& GetBottomLeftPoint() const { return mPoints[2]; }
	inline const Vec2D& GetBottomRightPoint() const { return mPoints[3]; }
	inline const std::vector<Line2D> GetLines() const { return mRocketLines; }

	inline void SetCenterPosition(const Vec2D& newPosition) { mPosition = newPosition; }
	//inline void SetSize(const int newSize) { mSize = newSize; }

	void MoveTo(const Vec2D& p) override;

	Vec2D GetCenterPoint() const override { return mCenterOfMass; }


	void RotateAroundCenter(float angle);

	void Rotate(float angle, const Vec2D& aroundPoint);

private:

	void calculateCenterOfMass();
	void createGeometry();

	std::vector<Line2D> mRocketLines;
	Vec2D mPosition;
	Vec2D mCenterOfMass;
	int mRocketTipHeight;
	int mWidth, mHeight;
};

#endif /* SHAPES_ROCKET_H_ */