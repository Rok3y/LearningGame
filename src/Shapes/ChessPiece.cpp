#include "ChesePiece.h"

ChessPiece::ChessPiece(uint8_t id) : mId(id)
{

}

bool ChessPiece::operator==(const ChessPiece& other) const
{
	return (this->mPieceColor == other.mPieceColor) &&
		(this->mPieceName == other.mPieceName) &&
		(this->mId == other.mId);
}