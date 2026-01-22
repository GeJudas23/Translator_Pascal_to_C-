program BubbleSort;

var
    arr: array[1..10] of integer;
    n, i: integer;

{ Процедура для обмена двух элементов }
procedure swap(var a, b: integer);
var
    temp: integer;
begin
    temp := a;
    a := b;
    b := temp;
end;

{ Процедура сортировки пузырьком }
procedure bubbleSort(var a: array[1..10] of integer; size: integer);
var
    i, j: integer;
    swapped: boolean;
begin
    for i := 1 to size - 1 do
    begin
        swapped := false;
        for j := 1 to size - i do
        begin
            if a[j] > a[j + 1] then
            begin
                swap(a[j], a[j + 1]);
                swapped := true;
            end;
        end;
        
        { Если не было обменов, массив уже отсортирован }
        if not swapped then
            break;
    end
end;

{ Процедура вывода массива }
procedure printArray(a: array[1..10] of integer; size: integer);
var
    i: integer;
begin
    for i := 1 to size do
        write(a[i], ' ');
    writeln;
end;

begin
    write('Введите количество элементов (1-10): ');
    readln(n);
    
    if (n < 1) or (n > 10) then
    begin
        writeln('Ошибка: количество должно быть от 1 до 10');
    end
    else
    begin
        writeln('Введите ', n, ' элементов:');
        for i := 1 to n do
        begin
            write('arr[', i, '] = ');
            readln(arr[i]);
        end;
        
        write('Исходный массив: ');
        printArray(arr, n);
        
        bubbleSort(arr, n);
        
        write('Отсортированный массив: ');
        printArray(arr, n);
    end
end.