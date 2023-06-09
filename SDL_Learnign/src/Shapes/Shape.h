#ifndef SHAPES_SHAPE_H
#define SHAPES_SHAPE_H

#include "Vec2D.h"
#include <vector>

class Shape
{
public:
	virtual Vec2D GetCenterPoint() const = 0; // pure virtual method
	virtual ~Shape() {}
	inline virtual std::vector<Vec2D> GetPoints() const { return mPoints; }
	void MoveBy(const Vec2D& deltaOffset);
	virtual void MoveTo(const Vec2D& p) = 0;

protected:
	std::vector<Vec2D> mPoints;
};

#endif /* SHAPES_SHAPE_H */