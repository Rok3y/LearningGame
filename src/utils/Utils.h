#ifndef UTILS_UTILS_H_
#define UTILS_UTILS_H_

static const float EPSILON = 0.0001f;

bool IsEqual(float x, float y);

bool IsGreaterOrEqual(float x, float y);

bool IsLessThanOrEqual(float x, float y);

float DegToRad(int degree);

#endif /* UTILS_UTILS_H_ */