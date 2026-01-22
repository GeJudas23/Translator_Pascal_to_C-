#include <iostream>
#include <string>
#include <cmath>

using namespace std;

int fib(int x);

int fibIterative(int x);

int main() {
    int n;

    cout << "Введите номер числа Фибоначчи: ";
    cin >> n;
    if ((n < 0)) {
        cout << "Ошибка: число должно быть неотрицательным" << endl;
    } else {
        {
            cout << "Рекурсивный метод: F(" << n << ") = " << fib(n) << endl;
            cout << "Итеративный метод: F(" << n << ") = " << fibIterative(n) << endl;
        }
    }
    return 0;
}

int fib(int x) {
    int fib_result;

    if ((x <= 1)) {
        fib_result = x;
    } else {
        fib_result = (fib((x - 1)) + fib((x - 2)));
    }
    return fib_result;
}

int fibIterative(int x) {
    int fibIterative_result;
    int i;
    int prev;
    int curr;
    int temp;

    if ((x <= 1)) {
        fibIterative_result = x;
    } else {
        {
            prev = 0;
            curr = 1;
            for (int i = 2; i <= x; i++) {
                {
                    temp = curr;
                    curr = (prev + curr);
                    prev = temp;
                }
            }
            fibIterative_result = curr;
        }
    }
    return fibIterative_result;
}
