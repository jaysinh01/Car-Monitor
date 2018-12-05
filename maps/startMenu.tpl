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
        <form action="/startMenu" method="GET">
            <input type="radio" name="functions" value="weatherSearch">Weather Search<br>
            <input type="radio" name="functions" value="musicPlayer">Music Player<br>
            <input type="radio" name="functions" value="maps">Maps<br>
            <input type="submit" name="search" value="CheckThis"><br>
        </form>
    </section>
    <footer></footer>
</body>
</html>