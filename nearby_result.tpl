<!DOCTYPE html>
<html>
<head>
    <title> near_result</title>
</head>
<body>
    <header><h1>Nearby Results</h1></header>
    <section>
        <form action="/nearby/results" method="GET">
        % for name in result:
            <input type="sumbit" name="place" value= {{name}}><br><br>
        %end
            <input type="button" name="back" value="Back to previous page">
            <input type="button" name="backToStartMenu" value="Back To Start Menu"><br><br>
        </form>
    </section>
    <footer></footer>
</body>
</html>