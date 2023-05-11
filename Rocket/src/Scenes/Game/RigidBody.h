#ifndef GAME_RIGIDBODY_H_
#define GAME_RIGIDBODY_H_

#include "GameObject.h"
#include "AARectangle.h"
#include "BoxShape.h"
#include "Vec2D.h"
#include <stdint.h>

class RigidBody : BoxShape
{
	RigidBody()

private:
	Vec2D mPosition;
	Vec2D mLinearVelocity;
	float mAngle;
	float mAngularVelocity;
	Vec2D mForce;
	float mTorque;
};

#endif /* GAME_RIGIDBODY_H_ */