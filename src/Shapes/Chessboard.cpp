#include "ChessBoard.h"
#include "Pawn.h"
#include <algorithm>

ChessBoard::ChessBoard()//uint32_t width, uint32_t height, Vec2D topLeftStartingPosition)
	: mPieces(8)//mPieceSize(1), mWidth(width), mHeight(height), mTopLeftStartingPosition(topLeftStartingPosition)
{
	//uint32_t rectWidth = mWidth / 8;
	//uint32_t rectHeight = mHeight / 8;

	//for (int i = 0; i < 8; i++)
	//{
	//	for (int j = 0; j < 8; j++)
	//	{
	//		//mRectangles.push_back(AARectangle(Vec2D((mTopLeftStartingPosition.GetX() + rectWidth * i), (mTopLeftStartingPosition.GetY() + rectHeight * j)), rectWidth, rectHeight));
	//		mRectangles.emplace_back(AARectangle(Vec2D(i, j), 0, 0));
	//	}
	//}
}

ChessBoard::~ChessBoard()
{
	if (!mPieces.empty())
	{
		for (auto vec : mPieces)
		{
			for (auto piece : vec)
			{
				piece.reset();
				piece = nullptr;
			}
		}
	}
}

void ChessBoard::Init()
{
	for (std::vector<std::shared_ptr<ChessPiece>>& vec : mPieces)
	{
		vec.reserve(8);
	}
	
	//uint32_t rectWidth = mWidth / 8;
	//uint32_t rectHeight = mHeight / 8;

	//for (int i = 0; i < 8; i++)
	//{
	//	mPieces.push_back(new Pawn(i, ChessPiece::White, ChessPiece::Pawn, Vec2D(rectWidth, ( + rectWidth * 1)), mPieceSize));
	//	mPieces.push_back(new Pawn(i+7, ChessPiece::Black, ChessPiece::Pawn, Vec2D(6, i), mPieceSize));
	//}

	//// White Rooks
	//mPieces.push_back(new Pawn(16, ChessPiece::White, ChessPiece::Rook, Vec2D(0, 0), mPieceSize));
	//mPieces.push_back(new Pawn(17, ChessPiece::White, ChessPiece::Rook, Vec2D(0, 7), mPieceSize));


	//// Black Rooks
	//mPieces.push_back(new Pawn(18, ChessPiece::Black, ChessPiece::Rook, Vec2D(7, 0), mPieceSize));
	//mPieces.push_back(new Pawn(19, ChessPiece::Black, ChessPiece::Rook, Vec2D(7, 7), mPieceSize));

	//// White Knights
	//mPieces.push_back(new Pawn(20, ChessPiece::White, ChessPiece::Knight, Vec2D(0, 1), mPieceSize));
	//mPieces.push_back(new Pawn(21, ChessPiece::White, ChessPiece::Knight, Vec2D(0, 6), mPieceSize));

	//// Black Knights
	//mPieces.push_back(new Pawn(22, ChessPiece::Black, ChessPiece::Knight, Vec2D(7, 1), mPieceSize));
	//mPieces.push_back(new Pawn(23, ChessPiece::Black, ChessPiece::Knight, Vec2D(7, 6), mPieceSize));

	//// White Bishop
	//mPieces.push_back(new Pawn(24, ChessPiece::White, ChessPiece::Bishop, Vec2D(0, 2), mPieceSize));
	//mPieces.push_back(new Pawn(25, ChessPiece::White, ChessPiece::Bishop, Vec2D(0, 5), mPieceSize));

	//// Black Bishop
	//mPieces.push_back(new Pawn(26, ChessPiece::Black, ChessPiece::Bishop, Vec2D(7, 2), mPieceSize));
	//mPieces.push_back(new Pawn(27, ChessPiece::Black, ChessPiece::Bishop, Vec2D(7, 5), mPieceSize));

	//// White Queen
	//mPieces.push_back(new Pawn(28, ChessPiece::White, ChessPiece::Queen, Vec2D(0, 3), mPieceSize));

	//// Black Queen
	//mPieces.push_back(new Pawn(29, ChessPiece::Black, ChessPiece::Queen, Vec2D(7, 3), mPieceSize));

	//// White Kingh
	//mPieces.push_back(new Pawn(30, ChessPiece::White, ChessPiece::King, Vec2D(0, 4), mPieceSize));

	//// Black King
	//mPieces.push_back(new Pawn(31, ChessPiece::Black, ChessPiece::King, Vec2D(7, 4), mPieceSize));
}

void ChessBoard::RemovePiece(std::shared_ptr<ChessPiece> piece)
{
	//for (auto p : mPieces)
	//{
	//	if (p == piece)
	//	{
	//		mPieces.erase(std::remove(mPieces.begin(), mPieces.end(), p), mPieces.end());
	//		std::cout << "Erase here" << std::endl;

	//		delete p;
	//		p = nullptr;
	//	}
	//}
}