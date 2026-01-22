program ArrayOperations;

var
    arr: array[1..10] of integer;
    i, sum, max: integer;

begin
    { Заполнение массива }
    writeln('Введите 10 чисел:');
    for i := 1 to 10 do
    begin
        write('arr[', i, '] = ');
        readln(arr[i]);
    end;
    
    { Вычисление суммы }
    sum := 0;
    for i := 1 to 10 do
        sum := sum + arr[i];
    
    { Поиск максимума }
    max := arr[1];
    for i := 2 to 10 do
        if arr[i] > max then
            max := arr[i];
    
    { Вывод результатов }
    writeln('Сумма элементов: ', sum);
    writeln('Максимальный элемент: ', max);
    writeln('Среднее значение: ', sum / 10);
end.