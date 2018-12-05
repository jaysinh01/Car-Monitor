<!--
    https://www.w3schools.com
-->
%# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
<head>
    <title>directions</title>
</head>
<body>
    <header><h1>Step-Step Directions:</h1></header>
    <section>
        %for step in instructions:
            <p>{{step}}</p>
        %end
        <form action="/directions" method="GET">
            <input type="button" name="backTonPrev" value="BackToPreviousPage">
            <input type="button" name="backToStartMenu" value="BackToStartMenu"><br>
        </form>
    </section>
    <footer></footer>
</body>
</html>