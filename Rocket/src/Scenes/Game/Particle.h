#ifndef GAME_RECT_H_
#define GAME_RECT_H_

#include "GameObject.h"
#include "AARectangle.h"
#include "Vec2D.h"
#include <stdint.h>

class Screen;

class Particle : public GameObject
{
public:
	Particle(const Vec2D& pos, uint32_t width, uint32_t height);
	inline AARectangle GetRectangle() const { return mRect; }
	void SetPosition(const Vec2D& pos) override;
	void SetVelocity(const Vec2D& vel) override;
	void SetAcceleration(const Vec2D& acc) override;
	void SetMass(float mass) override;
	inline void SetScreenBoundary(const AARectangle& boundary) { mBoundary = boundary; }
	inline void SetCollideWithEdge(bool collide) { mCollideWithEdge = collide; }

	void Update(uint32_t dt);
	void Draw(Screen& screen);

private:
	bool mCollideWithEdge;
	AARectangle mBoundary;
	AARectangle mRect;
};

#endif /* GAME_RECT_H_ */