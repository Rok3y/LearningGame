/*
* Utils
*/

#include "Utils.h"
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