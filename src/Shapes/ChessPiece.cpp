#include "ChesePiece.h"

ChessPiece::ChessPiece(uint8_t id, PieceColor color, PieceName name, Vec2D position, uint8_t size)
	:mId(id), mPieceColor(color), mPieceName(name), mBoardPosition(position), mSize(size)
{

}

bool ChessPiece::operator==(const ChessPiece& other) const
{
	return (this->mPieceColor == other.mPieceColor) &&
		(this->mPieceName == other.mPieceName) &&
		(this->mId == other.mId);
}