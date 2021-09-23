#include <algorithm> // for transform
#include <functional> // for plus
#include <vector> // for plus
#include <iostream>
#include <cmath>

struct calc_wind_modulus : std::binary_function<float, float, float>
{
    float operator()(const float & uu, const float & vv) const
    {
        return pow((pow(uu,2)+pow(vv,2)),0.5);
    }
};

extern "C" float* wind_modulus_cpp (const float* a, const float* b, const int size)
{
    std::cout << __PRETTY_FUNCTION__ <<std::endl;
    float* results = new float[size];
    transform(a, a + size, b, results, calc_wind_modulus());
    // for(int i = 0; i < size; i++){
    //     std::cout << a[i] << "\t" << b[i] << "\t" << results[i] <<std::endl;
    // }
    return results;
}

