%# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
<head>
    <title>weatherSearch</title>
</head>
<body>
    <header><h1>How's the weather in...</h1></header>
    <section>
        <p>
            Format: City Province(optional) Country(optional)<br>
            (e.g. New York NY USA)<br>
        </p>
        <form action="/weatherSearch" method="GET"  autocomplete="ON">
            <input type="text" size="100" maxlength="100" name="address">
            <input type="submit" name="search" value="search">
            <input type="submit" name="backToStartMenu" value="backToStartMenu">
        </form>
        <p>
            %for i in result:
                {{i}}<br>
            %end
        </p>
    </section>
    <footer></footer>
</body>
</html>