#ifndef SHAPES_PAWN_H_
#define SHAPES_PAWN_H_

#include "ChesePicese.h"

class Pawn : public ChessPiece
{
public:
	virtual Vec2D GetCenterPoint() const override;
	virtual void MoveTo(const Vec2D& p) = 0;
	virtual Vec2D GetBoardPosition() const override;
};

#endif /* SHAPES_PAWN_H_ */
