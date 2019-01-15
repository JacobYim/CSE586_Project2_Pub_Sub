<!DOCTYPE html>
<html>
    <head>
        <title>Pub-Sub Phase 1</title>
    </head>
    <body>
        <form action="index.php">
        <input type="text" name="name"/>
        <input type="submit">
        </form>
    <?php
        if ($_GET["name"]=="") {
            $output = shell_exec('/usr/local/bin/docker build -t friendlyhello .');
            echo $output;
            $output = shell_exec('/usr/local/bin/docker run -p 4000:80 friendlyhello');
            echo $output;
            $output = shell_exec('/usr/local/bin/docker start -p 4000:80 friendlyhello');
            echo $output;
            $output = "none";
            echo $output;
        }else{
            $output = $_GET["name"];
            echo $output;
        }
    ?>
    </body>
</html>
