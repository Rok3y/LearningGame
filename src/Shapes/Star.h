#ifndef SHAPES_STAR_H_
#define SHAPES_STAR_H_

#include <vector>

#include "Vec2D.h"
#include "Line2D.h"


class Star
{
public:
	Star();
	Star(const Vec2D& position, int size);

	inline const Vec2D& GetCenterPosition() const { return mPosition; }
	inline const int GetSize() const { return mSize; }
	inline const std::vector<Line2D> GetLines() const { return mStarLines; }
	inline const std::vector<Vec2D> GetPoints() const { return mStarPoints; }

	inline void SetCenterPosition(const Vec2D& newPosition) { mPosition = newPosition; }
	inline void SetSize(const int newSize) { mSize = newSize; }


	void RotateAroundCenter(float angle);

	void Rotate(float angle, const Vec2D& aroundPoint);

private:

	std::vector<Line2D> mStarLines;
	std::vector<Vec2D> mStarPoints;
	Vec2D mPosition;
	int mSize;
};

#endif /* SHAPES_STAR_H_ */