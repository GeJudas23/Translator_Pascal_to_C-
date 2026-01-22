#include <iostream>
#include <string>
#include <cmath>

using namespace std;

int main() {
    int arr[10];
    int i;
    int sum;
    int max;

    cout << "Введите 10 чисел:" << endl;
    for (int i = 1; i <= 10; i++) {
        {
            cout << "arr[" << i << "] = ";
            cin >> arr[(i - 1)];
        }
    }
    sum = 0;
    for (int i = 1; i <= 10; i++) {
        sum = (sum + arr[(i - 1)]);
    }
    max = arr[(1 - 1)];
    for (int i = 2; i <= 10; i++) {
        if ((arr[(i - 1)] > max)) {
            max = arr[(i - 1)];
        }
    }
    cout << "Сумма элементов: " << sum << endl;
    cout << "Максимальный элемент: " << max << endl;
    cout << "Среднее значение: " << (sum / 10) << endl;
    return 0;
}
