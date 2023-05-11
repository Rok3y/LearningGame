#ifndef GAME_GAMEOBJECT_H_
#define GAME_GAMEOBJECT_H_

#include "Vec2D.h"

enum Edge {
	LEFT_EDGE = 0,
	RIGHT_EDGE,
	TOP_EDGE,
	BOTTOM_EDGE
};

class GameObject
{
public:
	virtual void SetPosition(const Vec2D& pos) = 0;
	virtual void SetVelocity(const Vec2D& vel) = 0;
	virtual void SetAcceleration(const Vec2D& acc) = 0;
	virtual void SetMass(float mass) = 0;

	inline const Vec2D& GetPosition() const { return mPosition; }
	inline const Vec2D& GetVelocity() const { return mVelocity; }
	inline const Vec2D& GetAcceleration() const { return mAcceleration; }
	inline const float GetMass() const { return mMass; }


	// Calculate new direction vector as mVelocity
	// Bouncing fomrula -v(n*(v.n)*2)
	inline Vec2D CalculateReflectingVector(const Vec2D& edgeNorm) const
	{
		return (mVelocity - (edgeNorm * mVelocity.Dot(edgeNorm) * 2));
	}

protected:
	Vec2D mPosition;
	Vec2D mVelocity; // For now velocity and direction properties are combined
	Vec2D mAcceleration;
	float mMass;
};

#endif /* GAME_GAMEOBJECT_H_ */