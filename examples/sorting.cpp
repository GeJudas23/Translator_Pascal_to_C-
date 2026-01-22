#include <iostream>
#include <string>
#include <cmath>

using namespace std;

void swap(int& a, int& b);

void bubbleSort(int a[], int size);

void printArray(int a[], int size);

int main() {
    int arr[10];
    int n;
    int i;

    cout << "Введите количество элементов (1-10): ";
    cin >> n;
    if (((n < 1) || (n > 10))) {
        {
            cout << "Ошибка: количество должно быть от 1 до 10" << endl;
        }
    } else {
        {
            cout << "Введите " << n << " элементов:" << endl;
            for (int i = 1; i <= n; i++) {
                {
                    cout << "arr[" << i << "] = ";
                    cin >> arr[(i - 1)];
                }
            }
            cout << "Исходный массив: ";
            printArray(arr, n);
            bubbleSort(arr, n);
            cout << "Отсортированный массив: ";
            printArray(arr, n);
        }
    }
    return 0;
}

void swap(int& a, int& b) {
    int temp;

    temp = a;
    a = b;
    b = temp;
}

void bubbleSort(int a[], int size) {
    int i;
    int j;
    bool swapped;

    for (int i = 1; i <= (size - 1); i++) {
        {
            swapped = false;
            for (int j = 1; j <= (size - i); j++) {
                {
                    if ((a[(j - 1)] > a[((j + 1) - 1)])) {
                        {
                            swap(a[(j - 1)], a[((j + 1) - 1)]);
                            swapped = true;
                        }
                    }
                }
            }
            if (!(swapped)) {
                break;
            }
        }
    }
}

void printArray(int a[], int size) {
    int i;

    for (int i = 1; i <= size; i++) {
        cout << a[(i - 1)] << ' ';
    }
    cout << endl;
}
