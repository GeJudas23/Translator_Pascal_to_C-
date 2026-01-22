program Fibonacci;

var
    n: integer;

{ Рекурсивная функция Фибоначчи }
function fib(x: integer): integer;
begin
    if x <= 1 then
        fib := x
    else
        fib := fib(x - 1) + fib(x - 2)
end;

{ Итеративная версия для сравнения }
function fibIterative(x: integer): integer;
var
    i, prev, curr, temp: integer;
begin
    if x <= 1 then
        fibIterative := x
    else
    begin
        prev := 0;
        curr := 1;
        for i := 2 to x do
        begin
            temp := curr;
            curr := prev + curr;
            prev := temp;
        end;
        fibIterative := curr;
    end
end;

begin
    write('Введите номер числа Фибоначчи: ');
    readln(n);
    
    if n < 0 then
        writeln('Ошибка: число должно быть неотрицательным')
    else
    begin
        writeln('Рекурсивный метод: F(', n, ') = ', fib(n));
        writeln('Итеративный метод: F(', n, ') = ', fibIterative(n));
    end
end.