program Factorial;

var
    n, result: integer;

function fact(x: integer): integer;
begin
    if x <= 1 then
        fact := 1
    else
        fact := x * fact(x - 1)
end;

procedure printResult(value: integer);
begin
    writeln('Factorial = ', value)
end;

begin
    write('Enter a number: ');
    readln(n);
    
    if n < 0 then
    begin
        writeln('Error: negative number');
    end
    else
    begin
        result := fact(n);
        printResult(result);
    end
end.