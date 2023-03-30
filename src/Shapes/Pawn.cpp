#include "Pawn.h"
#include "Line2D.h"
#include "Utils.h"

Pawn::Pawn(uint8_t id, PieceColor color, PieceName name, Vec2D position, uint8_t size)
	: ChessPiece(id, color, name, position, size)
{

	Vec2D center = position - Vec2D(5, 3);
	
	mPoints.push_back(Vec2D(center.GetX() + (0  * mSize), center.GetY() - (0 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (10 * mSize), center.GetY() - (0 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (10 * mSize), center.GetY() - (1 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (9 * mSize), center.GetY() -  (2 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (7 * mSize), center.GetY() -  (3 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (6 * mSize), center.GetY() -  (6 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (8 * mSize), center.GetY() -  (6 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (8 * mSize), center.GetY() -  (7 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (2 * mSize), center.GetY() -  (7 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (2 * mSize), center.GetY() -  (6 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (4 * mSize), center.GetY() -  (6 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (3 * mSize), center.GetY() -  (3 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (1 * mSize), center.GetY() -  (2 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (0 * mSize),  center.GetY() - (1 * mSize)));
	mPoints.push_back(Vec2D(center.GetX() + (0  * mSize),  center.GetY() -(0 * mSize)));


	int currPointSize = mPoints.size();

	// Connect lines to make a pawn shape
	for (int i = 0; i < currPointSize - 1; i++)
	{
		mLines.push_back(Line2D(mPoints.at(i), mPoints.at(i+1)));
	}
	mLines.push_back(Line2D(mPoints.at(mPoints.size()-1), mPoints.at(0)));


	// Pawn's head (a circle)
	float radRotate = DegToRad(-12);
	Vec2D headCenter = { center.GetX() + (5 * mSize), center.GetY() - (9 * mSize) };

	auto first = (headCenter + Vec2D((4 + mSize), 5));
	mPoints.push_back(first);

	mPoints.push_back(mPoints.at(mPoints.size()-1).RotationResult(radRotate, headCenter));
	mLines.push_back(Line2D(mPoints.at(mPoints.size() - 2), mPoints.at(mPoints.size() - 1)));

	for (int i = 0; i < 20; i++)
	{
		mPoints.push_back(mPoints.at(mPoints.size() - 1).RotationResult(radRotate, headCenter));
		mLines.push_back(Line2D(mPoints.at(mPoints.size() - 2), mPoints.at(mPoints.size() - 1)));
	}
}

Vec2D Pawn::GetCenterPoint() const
{
	return Vec2D::Zero;
}

void Pawn::MoveTo(const Vec2D& p)
{

}