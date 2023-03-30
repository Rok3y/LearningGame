#ifndef SHAPES_CHESSPIECE_H_
#define SHAPES_CHESSPIECE_H_

#endif /* SHAPES_CHESSPIECE_H_ */

#include "Vec2D.h"
#include <stdint.h>

class Shape;

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

class ChessPiece : public Shape
{
public:
	ChessPiece(uint8_t id);

	ChessPiece(const ChessPiece&) = delete; // Deleted copy-constructor
	ChessPiece& operator=(const ChessPiece&) = delete; // Deleted copy-assignment operator

	ChessPiece(ChessPiece&&) = delete; // Delete rvalue copy-constructor
	ChessPiece& operator =(ChessPiece&&) = default; // Delete rvalue copy-assignment operator

	virtual Vec2D GetCenterPoint() const = 0;
	virtual ~ChessPiece() {}
	virtual void MoveTo(const Vec2D& p) = 0;
	virtual Vec2D GetBoardPosition() const = 0;

	inline const PieceColor GetPieceColor() const { return mPieceColor; }
	inline const PieceName GetPieceName() const { return mPieceName; }
	inline const uint8_t GetPieceId() const { return mId; }

	bool operator==(const ChessPiece& other) const;

private:
	uint8_t mId;
	PieceColor mPieceColor;
	PieceName mPieceName;
	Vec2D mBoardPosition;
};