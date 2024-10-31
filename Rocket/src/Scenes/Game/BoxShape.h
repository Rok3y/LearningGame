#ifndef GAME_BOXSHAPE_H_
#define GAME_BOXSHAPE_H_

#include "GameObject.h"

class Screen;

class BoxShape : GameObject
{
	BoxShape(float w, float h, float m)
		:mWidth(w), mHeight(h), mMass(m), mMomentOfInertia(0)
	{
		mMomentOfInertia = CalculateBoxInertia();
	}

protected:
	inline void CalculateBoxInertia() { mMomentOfInertia = mMass * (mWidth * mWidth + mHeight * mHeight) / 12; }

private:
	float mWidth;
	float mHeight;
	float mMass;
	float mMomentOfInertia;
};

#endif /* GAME_BOXSHAPE_H_ */