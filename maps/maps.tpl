<!--
    https://www.w3schools.com
-->
%# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
<head>
    <title>maps</title>
</head>
<body>
    <header><h1>What you gonna do...</h1></header>
    <section>
        <form action="/maps" method="GET">
            <fieldset>
                <p>Search nearby:</p>
                <input type="radio" name="nearby" value="Restuarant" checked>Restuarant<br>
                <input type="radio" name="nearby" value="ShoppingMalls">Shopping Malls<br>
                <input type="radio" name="nearby" value="GasStations">Gas Stations<br>
                <input type="radio" name="nearby" value="Hospital">Hospital<br>
                <input type="radio" name="nearby" value="ParkingSpots">Parking Spots<br><br>
                <input type="submit" name="searchNearby" value="search"><br>
                <p>Find a destination:</p>
                Address<input type="text" size="60" maxlength="20" name="address">
                City<input type="text" size="20" maxlength="20" name="city">
                Country<input type="text" size="20" maxlength="60" name="country">
                <input type="submit" name="findDestination" value="FindDestination"><br>
                %if suggestedAddress != '':
                    <p>Suggested address: {{suggestedAddress}}</p>
                    <input type="submit" name="goBySuggestion" value="GoBySuggestion"><br>
                %end
            </fieldset>
            <input type="submit" name="backToStartMenu" value="Back To Start Menu">
        </form>
    </section>
    <footer></footer>
</body>
</html>