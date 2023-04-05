#ifndef SHAPES_PAWN_H_
#define SHAPES_PAWN_H_

#include "ChesePiece.h"
#include "Line2D.h"

class Pawn : public ChessPiece
{
public:
	Pawn(uint8_t id, PieceColor color, PieceName name, Vec2D position, uint8_t size);

	virtual Vec2D GetCenterPoint() const override;
	virtual void MoveTo(const Vec2D& p) override;

};

#endif /* SHAPES_PAWN_H_ */
