#include <iostream>
#include <SDL.h>

#include "Color.h"
#include "Screen.h"
#include "Line2D.h"
#include "Vec2D.h"
#include "DynamicIntArray.h"
#include "Utils.h"
#include "Star.h"

using namespace std;

const int SCREEN_WIDTH = 224;
const int SCREEN_HEIGHT = 288;
const int MAGNIFICATION = 3;

int main(int argc, char* argv[]) 
{
    Screen theScreen;
    theScreen.Init(SCREEN_WIDTH, SCREEN_HEIGHT, MAGNIFICATION);

    Vec2D p1 = Vec2D(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2);
    Vec2D p2 = Vec2D(SCREEN_WIDTH, SCREEN_HEIGHT);
    Line2D line = { p1, p2 };

    theScreen.Draw(line, Color::White());

    //theScreen.Draw(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, Color::Yellow());
    theScreen.SwapScreen();



    // Pentagon
    //int size = 20;
    //Vec2D center = Vec2D(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2);
    //float radRotate = DegToRad(72);

    //Vec2D pp1 = Vec2D(center.GetX(), center.GetY() - size);
    //Vec2D pp2 = pp1.RotationResult(radRotate, center);
    //Vec2D pp3 = pp2.RotationResult(radRotate, center);
    //Vec2D pp4 = pp3.RotationResult(radRotate, center);
    //Vec2D pp5 = pp4.RotationResult(radRotate, center);

    //theScreen.Draw(pp1, Color::Yellow());
    //theScreen.Draw(pp2, Color::Yellow());
    //theScreen.Draw(pp3, Color::Yellow());
    //theScreen.Draw(pp4, Color::Yellow());
    //theScreen.Draw(pp5, Color::Yellow());

    //Line2D line1 = Line2D(pp1, pp3);
    //Line2D line2 = Line2D(pp3, pp5);
    //Line2D line3 = Line2D(pp5, pp2);
    //Line2D line4 = Line2D(pp2, pp4);
    //Line2D line5 = Line2D(pp4, pp1);

    //theScreen.Draw(line1, Color::Yellow());
    //theScreen.Draw(line2, Color::Yellow());
    //theScreen.Draw(line3, Color::Yellow());
    //theScreen.Draw(line4, Color::Yellow());
    //theScreen.Draw(line5, Color::Yellow());

    Vec2D starPosition = Vec2D(SCREEN_WIDTH / 2 + 50, SCREEN_HEIGHT / 2);
    Star star(starPosition, 20);
    std::vector<Line2D> starLines = star.GetLines();

    for (int i = 0; i < starLines.size(); i++)
    {
        theScreen.Draw(starLines.at(i), Color::Blue());
    }

    theScreen.SwapScreen();

    SDL_Event sdlEvent;
    bool running = true;

    while (running)
    {
        while (SDL_PollEvent(&sdlEvent))
        {
            switch (sdlEvent.type)
            {
            case SDL_QUIT:
                running = false;
                break;
            }
        }

        // Rotating line
        /*line.SetP1(line.GetP1().RotationResult(0.001, p1));
        theScreen.Draw(line, Color::White());*/

        // Rotating line
        line.SetP1(line.GetP1().RotationResult(0.005, p1));
        theScreen.Draw(line, Color::White());

        // Draw star
        for (int i = 0; i < star.GetLines().size(); i++)
        {
            theScreen.Draw(star.GetLines().at(i), Color::Blue());
        }
        star.Rotate(0.005, p1);

        theScreen.SwapScreen();
    }

    return 0;
}