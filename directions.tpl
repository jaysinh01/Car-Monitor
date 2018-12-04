<!DOCTYPE html>
<html>
<head>
    <title> directions</title>
</head>
<body>
    <header><h1>Step-Step Directions</h1></header>
    <section>
        <form action="/directions" method="GET">
        % for step in instructions:
            <input type="sumbit" name="place" value= {{step}}><br><br>
        %end
            <input type="button" name="back" value="Back to previous page">
            <input type="button" name="backToStartMenu" value="Back To Start Menu"><br><br>
        </form>
    </section>
    <footer></footer>
</body>
</html>