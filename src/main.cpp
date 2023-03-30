#include <iostream>
#include "App.h"

#include "ChesePiece.h"
#include "ChessBoard.h"
#include "Pawn.h"

using namespace std;

const int SCREEN_WIDTH = 224;
const int SCREEN_HEIGHT = 288;
const int MAGNIFICATION = 3;

int main(int argc, char* argv[]) 
{
    if (App::Singleton().Init(SCREEN_WIDTH, SCREEN_WIDTH, MAGNIFICATION))
    {
        App::Singleton().Run();
    }

    //ChessBoard b;
    //b.Init();
    //b.GetPieces();

    //std::cout << "Pieces size: " << b.GetPieces().size() << std::endl;

    //auto pawn = b.GetPieces().at(0);

    //if (pawn)
    //{
    //    std::cout << "pawn alive: " << pawn->GetPieceId() << std::endl;
    //}

    //b.RemovePiece(pawn);

    //std::cout << "Pieces size: " << b.GetPieces().size() << std::endl;

    //if (pawn)
    //{
    //    std::cout << "pawn alive: " << pawn << std::endl;
    //}

    //

    return 0;
}