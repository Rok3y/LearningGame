#ifndef SHAPES_CHESSBOARD_H_
#define SHAPES_CHESSBOARD_H_

#include <vector>

class ChessPiece;

class ChessBoard
{
public:
	ChessBoard();
	void RemovePiece(const ChessPiece& piece);

private:
	std::vector<ChessPiece> mPieces;
};

#endif /* SHAPES_CHESSBOARD_H_ */
