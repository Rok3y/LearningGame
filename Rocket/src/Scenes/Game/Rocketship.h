#ifndef GAME_ROCKETSHIP_H_
#define GAME_ROCKETSHIP_H_

#include "GameObject.h"
#include "Rocket.h"
#include "AARectangle.h"
#include "Vec2D.h"
#include <stdint.h>

class Screen;

class Rocketship : public GameObject
{
public:
	Rocketship(const Vec2D& pos, uint32_t width, uint32_t height, uint32_t tipRocket);
	inline Rocket GetRocket() const { return mRocket; }
	void SetPosition(const Vec2D& pos) override;
	void SetVelocity(const Vec2D& vel) override;
	void SetAcceleration(const Vec2D& acc) override;
	void Rotate(float rad);
	inline void SetScreenBoundary(const AARectangle& boundary) { mBoundary = boundary; }
	inline void SetCollideWithEdge(bool collide) { mCollideWithEdge = collide; }

	void Update(uint32_t dt);
	void Draw(Screen& screen);

private:
	bool mCollideWithEdge;
	AARectangle mBoundary;
	Rocket mRocket;
};

#endif /* GAME_ROCKETSHIP_H_ */