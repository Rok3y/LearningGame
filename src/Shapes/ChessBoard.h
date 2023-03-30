#ifndef SHAPES_CHESSBOARD_H_
#define SHAPES_CHESSBOARD_H_

#include <vector>
#include <memory>
#include "AARectangle.h"

class ChessPiece;

class ChessBoard
{
public:
	ChessBoard(uint32_t width, uint32_t height);
	~ChessBoard();
	void Init();
	void RemovePiece(const ChessPiece* piece);
	inline const std::vector<ChessPiece*>& GetPieces() const { return mPieces; }
	inline const std::vector<AARectangle>& GetBoardRectangles() const { return mRectangles; }

private:
	std::vector<ChessPiece*> mPieces;
	std::vector<AARectangle> mRectangles;
	uint8_t mPieceSize;
	uint32_t mWidth;
	uint32_t mHeight;
};

#endif /* SHAPES_CHESSBOARD_H_ */
