#include <iostream>
#include <string>
#include <cmath>

using namespace std;

int factorial(int n);

int power(int base, int exponent);

int sum(int n);

int gcd(int a, int b);

bool isPalindrome(int n, int original);

int main() {
    int n;

    cout << "Введите целое число: ";
    cin >> n;
    if ((n < 0)) {
        cout << "Ошибка: число должно быть положительным" << endl;
    } else {
        {
            cout << "Факториал " << n << "! = " << factorial(n) << endl;
            cout << "2 в степени " << n << " = " << power(2, n) << endl;
            cout << "Сумма от 1 до " << n << " = " << sum(n) << endl;
            cout << "НОД(" << n << ", " << (n * 2) << ") = " << gcd(n, (n * 2)) << endl;
        }
    }
    return 0;
}

int factorial(int n) {
    int factorial_result;

    if ((n <= 1)) {
        factorial_result = 1;
    } else {
        factorial_result = (n * factorial((n - 1)));
    }
    return factorial_result;
}

int power(int base, int exponent) {
    int power_result;

    if ((exponent = 0)) {
        power_result = 1;
    } else {
        if ((exponent = 1)) {
            power_result = base;
        } else {
            power_result = (base * power(base, (exponent - 1)));
        }
    }
    return power_result;
}

int sum(int n) {
    int sum_result;

    if ((n <= 0)) {
        sum_result = 0;
    } else {
        sum_result = (n + sum((n - 1)));
    }
    return sum_result;
}

int gcd(int a, int b) {
    int gcd_result;

    if ((b = 0)) {
        gcd_result = a;
    } else {
        gcd_result = gcd(b, (a % b));
    }
    return gcd_result;
}

bool isPalindrome(int n, int original) {
    bool isPalindrome_result;
    int lastDigit;

    if ((n < 10)) {
        {
            if ((original < 10)) {
                isPalindrome_result = true;
            } else {
                if ((n = (original % 10))) {
                    isPalindrome_result = isPalindrome((original / 10), (original / 10));
                } else {
                    isPalindrome_result = false;
                }
            }
        }
    } else {
        isPalindrome_result = false;
    }
    return isPalindrome_result;
}
