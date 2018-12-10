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
            <p>Distance: {{instructions["distance"]}}</p>
            <p>Duartion: {{instructions["duration"]}}</p>
            %for directions in instructions["directions"]:
                <p>{{directions}}</p>
            %end
        </fieldset>
        <form action="/directions" method="GET">
            <input type="submit" name="backToPrev" value="BackToPreviousPage">
            <input type="submit" name="backToStartMenu" value="BackToStartMenu"><br>
        </form>
    </section>
    <footer></footer>
</body>
</html>