#ifndef SHAPES_CHESSBOARD_H_
#define SHAPES_CHESSBOARD_H_

#include <vector>
#include <memory>
#include "AARectangle.h"

class ChessPiece;

class ChessBoard
{
public:
	ChessBoard();//uint32_t width, uint32_t height, Vec2D topLeftStartingPosition);
	~ChessBoard();
	void Init();
	void RemovePiece(const std::shared_ptr<ChessPiece> piece);
	inline const std::vector<std::vector<std::shared_ptr<ChessPiece>>>& GetPieces() const { return mPieces; }
	//inline const std::vector<AARectangle>& GetBoardRectangles() const { return mRectangles; }

private:
	std::vector<std::vector<std::shared_ptr<ChessPiece>>> mPieces;
	//std::vector<AARectangle> mRectangles;
	//uint8_t mPieceSize;
	//uint32_t mWidth;
	//uint32_t mHeight;
	//Vec2D mTopLeftStartingPosition;
};

#endif /* SHAPES_CHESSBOARD_H_ */
