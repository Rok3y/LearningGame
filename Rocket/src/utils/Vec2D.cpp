#include "Vec2D.h"
#include "Utils.h"

#include <cassert>
#include <cmath>

const Vec2D Vec2D::Zero;

std::ostream& operator<<(std::ostream& consoleOut, const Vec2D& vec)
{
    std::cout << "X: " << vec.mX << ", Y: " << vec.mY << std::endl;
    return consoleOut;
}

Vec2D operator*(float scalar, const Vec2D& vec)
{
    return vec * scalar;
}

bool Vec2D::operator==(const Vec2D& vec) const
{
    return IsEqual(mX, vec.mX) && IsEqual(mY, vec.mY);
}

bool Vec2D::operator!=(const Vec2D& vec) const
{
    return !(*this == vec); // call operator== --> *this is current vec2d object comparing against other
}

Vec2D Vec2D::operator-() const
{
    return Vec2D(-mX, -mY);
}

Vec2D Vec2D::operator*(float scale) const
{
    return Vec2D(scale * mX, scale * mY);
}

Vec2D Vec2D::operator/(float scale) const
{
    assert(fabsf(scale) < EPSILON);
    return Vec2D(mX / scale, mY / scale);
}

Vec2D& Vec2D::operator*=(float scale)
{
    *this = *this * scale;
    return *this;
}

Vec2D& Vec2D::operator/=(float scale)
{
    assert(fabsf(scale) < EPSILON);
    *this = *this / scale;
    return *this;
}

Vec2D Vec2D::operator+(const Vec2D& vec) const
{
    return Vec2D(mX + vec.mX, mY + vec.mY);
}

Vec2D Vec2D::operator-(const Vec2D& vec) const
{
    return Vec2D(mX - vec.mX, mY - vec.mY);
}

Vec2D& Vec2D::operator+=(const Vec2D& vec)
{
    *this = *this + vec;
    return *this;
}

Vec2D& Vec2D::operator-=(const Vec2D& vec)
{
    *this = *this - vec;
    return *this;
}

float Vec2D::Mag2() const
{
    return Dot(*this); // a^2 + b^2 = c^2
}

float Vec2D::Mag() const
{
    return sqrt(Mag2());
}

Vec2D Vec2D::GetUnitVec() const
{
    float mag = Mag();
    if (mag > EPSILON)
    {
        return *this / mag;
    }

    return Vec2D::Zero;
}

Vec2D& Vec2D::Normalize()
{
    float mag = Mag();
    if (mag > EPSILON)
    {
        *this /= mag;
    }

    return *this;
}

float Vec2D::Distance(const Vec2D & vec) const
{
    return (vec - *this).Mag();
}

float Vec2D::Dot(const Vec2D& vec) const
{
    return mX * vec.mX + mY * vec.mY;
}

Vec2D Vec2D::ProjectOnto(const Vec2D& vec) const
{
    Vec2D unit = vec.GetUnitVec(); // Get a unit vector in a director of vec

    float dot = Dot(unit); // Get projection to *this vector

    return unit * dot; // Scale projected vector to the length of vec
}

float Vec2D::AngleBetween(const Vec2D& vec) const
{
    return acosf(GetUnitVec().Dot(vec.GetUnitVec()));   // cos(theta) = a * b  => bot a and be are unit vectors
}

Vec2D Vec2D::Reflect(const Vec2D& normal) const
{
    // v - 2 * (v dot n) * n

    return *this - 2 * ProjectOnto(normal);
}

void Vec2D::Rotate(float angle, const Vec2D& aroundPoint)
{
    float cosine = cosf(angle);
    float sine = sinf(angle);

    // first go to that point rotate and then go back
    Vec2D thisVec(mX, mY);
    thisVec -= aroundPoint;

    float xRot = thisVec.mX * cosine - thisVec.mY * sine;
    float yRot = thisVec.mX * sine + thisVec.mY * cosine;

    Vec2D rot = Vec2D(xRot, yRot);
    *this = rot + aroundPoint;
}

Vec2D Vec2D::RotationResult(float angle, Vec2D& aroundPoint) const
{
    float cosine = cosf(angle);
    float sine = sinf(angle);

    // first go to that point rotate and then go back
    Vec2D thisVec(mX, mY);
    thisVec -= aroundPoint;

    float xRot = thisVec.mX * cosine - thisVec.mY * sine;
    float yRot = thisVec.mX * sine + thisVec.mY * cosine;

    Vec2D rot = Vec2D(xRot, yRot);
    return rot + aroundPoint;
}

void Vec2D::Print() const
{
    printf("x: %f, y: %f\n", mX, mY);
}