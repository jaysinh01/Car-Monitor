%# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
<head>
    <title>musicPlayer</title>
</head>
<body>
    <header>
        <h1>Music Player</h1>
    </header>
    <section>
        <fieldset>
            <legend>Now playing...</legend>
            <!--Prints the name of the playing song-->
            <p>{{playlist[0]}}<br></p>
            <!--
                Accesses the .mp3 by referring its corresponding URL
                e.g. file 'whatever.mp3' could be accessed from URL
                http://localhost:8080/static/whatever.mp3
            -->
            <!--
                autoPlay:
                    Song would be auto played at the beginning
            -->
            <audio id="player" controls="controls" {{autoPlay}}>
                %source = "http://localhost:8080/static/" + playlist[0]
                <source src={{source}}/>
                <!--Displays when browsers do not support the <audio> element-->
                Your browser does not support the audio element.
            </audio>
            <form form action="/musicPlayer" method="GET">
                <!--
                    The value of a given input 'inputName' could be accessed in server.py
                    by calling request.GET.'inputName'
                -->
                <!--
                    checked:
                        Checks the radio button
                -->
                %checkedAttribute = ["", ""]
                %if autoPlay == "":
                    %checkedAttribute[0] = "checked"
                %else:
                    %checkedAttribute[1] = "checked"
                %end
                <input type="radio" name="autoPlaySelect" id="autoPlaySelect0" value="" {{checkedAttribute[0]}}>Don't wanna Auto Play<br>
                <input type="radio" name="autoPlaySelect" id="autoPlaySelect1" value="autoPlay" {{checkedAttribute[1]}}>Auto Play<br>
                <!--Invisible button 'refresh'-->
                <input type="submit" name="refresh" id="refresh" value="refresh" style="display: none"><br>
                <input type="submit" name="prevSong" value="previousSong">
                <input type="submit" name="next" value="skip/next">
                <input type="submit" name="preference" value="sortByPreference">
                <input type="submit" name="backToStartMenu" value="backToStartMenu"><br>
                <p>Playlist</p>
                <!--
                    Uses scroll bar to adjust the playlist to fits the web page
                    if it's too long
                -->
                <div style="overflow-y: auto;">
                    <!--Prints the playlist-->
                    <input type="radio" name="song" value="0" checked>{{playlist[0]}}<br>
                %for i in range(1, len(playlist)):
                    <input type="radio" name="song" value={{str(i)}}>{{playlist[i]}}<br>
                %end
                <input type="submit" name="goTo" value="tryThis">
                </div>
            </form>
            <!--
                If a song has been played, clicks the 'refresh' button
                to allow the info to be sent back to server.py
            -->
            <script type="text/javascript">
                var player = document.getElementById("player");
                player.onended = function() {
                    document.getElementById("refresh").click();
                };
            </script>
        </fieldset>
    </section>
    <footer></footer>
</body>
</html>