/*
* Utils
*/

#define _USE_MATH_DEFINES

#include "Utils.h"
#include <math.h>
#include <cmath>

/*
* Checks if two floats are equal to some measure
*/
bool IsEqual(float x, float y)
{
	return fabsf(x - y) < EPSILON;
}

bool IsGreaterOrEqual(float x, float y)
{
	return x > y || IsEqual(x, y);
}

bool IsLessThanOrEqual(float x, float y)
{
	return x < y || IsEqual(x, y);
}

float DegToRad(int degree)
{
	return degree * M_PI / 180;
}

float MillisecondsToSeconds(unsigned int milliseconds)
{
	return static_cast<float>(milliseconds) / 1000.0f;
}