#ifndef GAME_RIGIDBODY_H_
#define GAME_RIGIDBODY_H_

#include "GameObject.h"
#include "AARectangle.h"
#include "BoxShape.h"
#include "Vec2D.h"
#include <stdint.h>
#include <Utils.h>

class RigidBody : BoxShape
{
	RigidBody(Vec2D pos, float angle, Vec2D linearVelocity = Vec2D::Zero, float angualVelocity = 0)
		: mPosition(pos), mAngle(angle/360 * PI * 2), mLinearVelocity(linearVelocity), mAngularVelocity(angualVelocity), BoxShape(50, 50, 10)
	{
	}

private:
	Vec2D mPosition;
	Vec2D mLinearVelocity;
	float mAngle;
	float mAngularVelocity;
	Vec2D mForce;
	float mTorque;
};

#endif /* GAME_RIGIDBODY_H_ */