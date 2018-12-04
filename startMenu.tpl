<!--
    https://www.w3schools.com
-->
%# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
<head>
    <title>startMenu</title>
</head>
<body>
    <header><h1>Start Menu</h1></header>
    <section>
        <form action="/startMenu" method="GET" autocomplete="ON">
            <input type="radio" name="functions" value="weatherSearch">Weather Search<br>
            <input type="radio" name="functions" value="musicPlayer">Music Player<br>
            <input type="radio" name="functions" value="maps">Maps<br>
            <input type="submit" name="search" value="Next"><br>
        </form>
    </section>
    <footer></footer>
</body>
</html>
