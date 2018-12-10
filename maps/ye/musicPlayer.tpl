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
            <p>{{playlist[0]}}<br></p>
            <audio id="player" controls="controls" {{autoPlay}}>
                %source = "http://localhost:8080/static/" + playlist[0]
                <source src={{source}}/>
                <!--Displays when browsers do not support the <audio> element-->
                Your browser does not support the audio element.
            </audio>
            <form form action="/musicPlayer" method="GET">
                %checkedAttribute = ["", ""]
                %if autoPlay == "":
                    %checkedAttribute[0] = "checked"
                %else:
                    %checkedAttribute[1] = "checked"
                %end
                <input type="radio" name="autoPlaySelect" id="autoPlaySelect0" value="" {{checkedAttribute[0]}}>Don't wanna Auto Play<br>
                <input type="radio" name="autoPlaySelect" id="autoPlaySelect1" value="autoPlay" {{checkedAttribute[1]}}>Auto Play<br>
                <input type="submit" name="refresh" id="refresh" value="refresh" style="display: none"><br>
                <input type="submit" name="prevSong" value="previousSong">
                <input type="submit" name="next" value="skip/next">
                <input type="submit" name="preference" value="sortByPreference">
                <input type="submit" name="backToStartMenu" value="backToStartMenu"><br>
                <p>Playlist</p>
                <div style="overflow-y: auto;">
                    <input type="radio" name="song" value="0" checked>{{playlist[0]}}<br>
                %for i in range(1, len(playlist)):
                    <input type="radio" name="song" value={{str(i)}}>{{playlist[i]}}<br>
                %end
                <input type="submit" name="goTo" value="tryThis">
                </div>
            </form>
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