#ifndef SHAPES_LINE2D_H_
#define SHAPES_LINE2D_H_

#include "Vec2D.h"

class Line2D
{
public:
	Line2D();
	Line2D(float x0, float y0, float x1, float y1);
	Line2D(const Vec2D& p0, const Vec2D& p1);

	inline const Vec2D& GetP0() const { return mP0; }
	inline const Vec2D& GetP1() const { return mP1; }

	inline void SetP0(const Vec2D& p0) { mP0 = p0; }
	inline void SetP1(const Vec2D& p1) { mP1 = p1; }

	bool operator==(const Line2D& line) const;

	/*
	* Gets a distance from closest point on a line to point p
	*/
	float MinDistanceFrom(const Vec2D& p, bool limitToSegment = false) const;

	/*
	* Gets point on a line that is closest to given point p. 
	* Given point p is projected on a line with dot product. Vector from p0 on a line to given point p is created
	* Line segment goes from p0 to p1 on the line
	*/
	Vec2D ClosestPoint(const Vec2D& p, bool limitToSegment = false) const;

	/*
	* Get the middle point of the line
	*/
	Vec2D MidPoint() const;

	/*
	* Gets slope coefficient (dy / dx)
	*/
	float Slope() const;

	/*
	* Gets length of the line between two points
	*/
	float Length() const;

private:
	Vec2D mP0;
	Vec2D mP1;
};

#endif /* SHAPES_LINE2D_H_ */