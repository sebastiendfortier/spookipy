#include <vector>
#include <algorithm>
#include <iostream>
#include <cmath>
using namespace std;

struct calc_wind_modulus : binary_function<float, float, float>
{
    float operator()(const float & uu, const float & vv) const
    {
        return pow((pow(uu,2)+pow(vv,2)),0.5);
    }
};

vector<float> cpp_function (const vector<float> a, const vector<float> b)
{
    vector<float> results;
    transform(a.begin(), a.end(), b.begin(), back_inserter(results), calc_wind_modulus());
    return results;
}

// int main()
// {
//     // Get the vector
//     vector<float> a = { 1, 45, 54, 71, 76, 12 };
//     vector<float> b = { 2, 3, 4, 5, 6, 7 };
//     vector<float> res;
    
//     cout << "Vector a: ";
//     for (size_t i = 0; i < a.size(); i++)
//         cout << a[i] << " ";
//     cout << endl;
    
//     cout << "Vector b: ";
//     for (size_t i = 0; i < b.size(); i++)
//         cout << b[i] << " ";
//     cout << endl;
    
    
//     res = cpp_function(a,b);
//     // Print the vector
//     cout << "result: ";
//     for (size_t i = 0; i < res.size(); i++)
//         cout << res[i] << " ";
//     cout << endl;

//     return 0;
// }
