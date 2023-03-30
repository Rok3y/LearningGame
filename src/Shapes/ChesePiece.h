#ifndef SHAPES_CHESSPIECE_H_
#define SHAPES_CHESSPIECE_H_

#include "Vec2D.h"
#include <stdint.h>
#include "Shape.h"

class ChessPiece : public Shape
{
public:

	enum PieceColor
	{
		Black = 0,
		White
	};

	enum PieceName
	{
		King = 0,
		Queen,
		Bishop,
		Knight,
		Rook,
		Pawn
	};

	ChessPiece(uint8_t id, PieceColor color, PieceName name, Vec2D position, uint8_t size);
	ChessPiece(const ChessPiece&) = delete; // Deleted copy-constructor
	ChessPiece& operator=(const ChessPiece&) = delete; // Deleted copy-assignment operator

	ChessPiece(ChessPiece&&) = delete; // Delete rvalue copy-constructor
	ChessPiece& operator =(ChessPiece&&) = default; // Delete rvalue copy-assignment operator

	virtual Vec2D GetCenterPoint() const override = 0;
	virtual ~ChessPiece() {}
	virtual void MoveTo(const Vec2D& p) override = 0;

	inline const Vec2D GetBoardPosition() const { return mBoardPosition; };
	inline const PieceColor GetPieceColor() const { return mPieceColor; }
	inline const PieceName GetPieceName() const { return mPieceName; }
	inline const uint8_t GetPieceId() const { return mId; }

	bool operator==(const ChessPiece& other) const;

protected:
	uint8_t mId;
	PieceColor mPieceColor;
	PieceName mPieceName;
	Vec2D mBoardPosition;
	uint8_t mSize;
};

#endif /* SHAPES_CHESSPIECE_H_ */