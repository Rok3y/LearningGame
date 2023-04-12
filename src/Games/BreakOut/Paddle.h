#ifndef GAMES_BREAKOUT_PADDLE_H_
#define GAMES_BREAKOUT_PADDLE_H_

#include "Excluder.h"
#include <stdint.h>

class Screen;

enum PaddleDirection
{
	LEFT = 1 << 0, // 1
	RIGHT = 1 << 1 // 2
};

class Paddle : public Excluder
{
public:

	static const uint32_t PADDLE_WIDTH = 50;
	static const uint32_t PADDLE_HEIGHT = 10;

	void Init(const AARectangle& rect, const AARectangle& boundary);
	void Update(uint32_t dt);
	void Draw(Screen& screen);
	inline bool IsMovingLeft() const { return mDirection == PaddleDirection::LEFT; }
	inline bool IsMovingRight() const { return mDirection == PaddleDirection::RIGHT; }
	
	// ~00 --> 11
	// 0 | 1 = 1
	// 0 & 1 = 0
	// 1 & 1 = 1
	inline void SetMovementDirection(PaddleDirection dir) { mDirection |= dir; }
	inline void UnsetMovementDirection(PaddleDirection dir) { mDirection &= ~dir; }
	void StopMovement() { mDirection = 0; }

private:
	uint32_t mDirection; // direction we're moving
	AARectangle mBoundary; // Boundary that the paddle is confined to
	const float VELOCITY = 100.0f; // pixels/sec
};

#endif /* GAMES_BREAKOUT_PADDLE_H_ */