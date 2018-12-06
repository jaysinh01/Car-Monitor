%# --------------------------------------------------
%# Name: Ang Li & Jaysinh Parmar
%# ID: 1550746 & 1532143
%# CMPUT 274, Fall 2018
%#
%# Project: Car monitor
%# ---------------------------------------------------
%# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
<head>
    <title>directions</title>
</head>
<body>
    <header><h1>Directions:</h1></header>
    <section>
        <fieldset>
            <!--Prints the distance & duration & directions-->
            <p>Distance: {{instructions["distance"]}}</p>
            <p>Duration: {{instructions["duration"]}}</p>
            %for directions in instructions["directions"]:
                <p>{{directions}}</p>
            %end
        </fieldset>
        <form action="/directions" method="GET">
            <!--
                The value of a given input 'inputName' could be accessed in server.py
                by calling request.GET.'inputName'
            -->
            <input type="submit" name="backToPrev" value="BackToPreviousPage">
            <input type="submit" name="backToStartMenu" value="BackToStartMenu"><br>
        </form>
    </section>
    <footer></footer>
</body>
</html>