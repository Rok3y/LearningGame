#include "DynamicIntArray.h"

DynamicIntArray::~DynamicIntArray()
{
	delete[] moptrData;
	moptrData = nullptr;
}

DynamicIntArray::DynamicIntArray(const DynamicIntArray& otherArray)
{
	if (!moptrData)
	{

	}
}

bool DynamicIntArray::Init(size_t capacity)
{
	if (capacity == 0)
	{
		return false;
	}

	if (mCapacity == capacity)
	{
		return true;
	}

	if (moptrData)
	{
		delete[] moptrData;
		moptrData = nullptr;
		mSize = 0;
		mCapacity = 0;
	}

	moptrData = new int[capacity];
	if (!moptrData)
	{
		return false;
	}

	mSize = 0;
	mCapacity = capacity;
	return true;
}

bool DynamicIntArray::Reserve(size_t capacity)
{
	if (mCapacity < capacity)
	{
		int* oldData = moptrData;

		moptrData = new int[capacity];
		if (!moptrData)
		{
			moptrData = oldData;
			return false;
		}

		for (size_t i = 0; i < mSize; i++)
		{
			moptrData[i] = oldData[i];
		}

		delete[] oldData;
	}

	return true;
}

bool DynamicIntArray::Resize(size_t newSize)
{
	if (mCapacity < newSize)
	{
		bool reserveResult = Reserve(newSize);
		if (!reserveResult)
		{
			return reserveResult;
		}
	}

	for (size_t i = mSize; i < newSize; i++)
	{
		moptrData[i] = 0;
	}

	mSize = newSize;

	return true;
}

bool DynamicIntArray::PushBack(int newVal)
{
	assert(moptrData && "Has not been initialized - call Init()"); // Only for debug mode
	if (!moptrData)
	{
		return false;
	}

	if (mSize + 1 > mCapacity)
	{
		bool resizeResult = Reserve(mCapacity * RESIZE_MULTIPLIER);
		if (!resizeResult)
		{
			return resizeResult;
		}
	}

	moptrData[mSize++] = newVal;

	return true;
}

bool DynamicIntArray::PopBack(int& value)
{
	assert(moptrData && "Has not been initialized - call Init()"); // Only for debug mode
	if (!moptrData)
	{
		return false;
	}

	if (mSize > 0)
	{
		value = moptrData[--mSize];
		return true;
	}

	return false;
}

const int& DynamicIntArray::operator[](size_t index) const
{
	assert(moptrData && index < mSize);
	return moptrData[index];
}

int& DynamicIntArray::operator[](size_t index)
{
	assert(moptrData && index < mSize);
	return moptrData[index];
}
