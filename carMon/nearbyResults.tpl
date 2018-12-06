%# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
<head>
    <title>nearbyResults</title>
</head>
<body>
    <header><h1>Nearby Results</h1><br>Sorted by distance:</header>
    <section>
        <form action="/nearbyResults" method="GET">
            <input type="radio" name="place" value= {{results[0]}} checked>{{results[0].replace("+", " ")}}<br>
        % for placeName in results[1:len(results)]:
            <input type="radio" name="place" value= {{placeName}}>{{placeName.replace("+", " ")}}<br>
        %end
            <input type="submit" name="direction" value="Direction"><br>
            <input type="submit" name="backToPrev" value="BackToPreviousPage">
            <input type="submit" name="backToStartMenu" value="BackToStartMenu">
        </form>
    </section>
    <footer></footer>
</body>
</html>