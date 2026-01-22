program Recursion;

var
    n: integer;

{ Вычисление факториала }
function factorial(n: integer): integer;
begin
    if n <= 1 then
        factorial := 1
    else
        factorial := n * factorial(n - 1)
end;

{ Вычисление степени числа }
function power(base: integer; exponent: integer): integer;
begin
    if exponent = 0 then
        power := 1
    else if exponent = 1 then
        power := base
    else
        power := base * power(base, exponent - 1)
end;

{ Сумма чисел от 1 до n }
function sum(n: integer): integer;
begin
    if n <= 0 then
        sum := 0
    else
        sum := n + sum(n - 1)
end;

{ Вычисление НОД (наибольший общий делитель) }
function gcd(a: integer; b: integer): integer;
begin
    if b = 0 then
        gcd := a
    else
        gcd := gcd(b, a mod b)
end;

{ Проверка, является ли число палиндромом }
function isPalindrome(n: integer; original: integer): boolean;
var
    lastDigit: integer;
begin
    if n < 10 then
    begin
        if original < 10 then
            isPalindrome := true
        else if (n = original mod 10) then
            isPalindrome := isPalindrome(original div 10, original div 10)
        else
            isPalindrome := false
    end
    else
        isPalindrome := false
end;

begin
    write('Введите целое число: ');
    readln(n);

    if n < 0 then
        writeln('Ошибка: число должно быть положительным')
    else
    begin
        writeln('Факториал ', n, '! = ', factorial(n));
        writeln('2 в степени ', n, ' = ', power(2, n));
        writeln('Сумма от 1 до ', n, ' = ', sum(n));
        writeln('НОД(', n, ', ', n * 2, ') = ', gcd(n, n * 2));
    end
end.
