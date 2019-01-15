<!DOCTYPE html>
<html>
    <head>
        <title>Pub-Sub Phase 1</title>
        <meta http-equiv ="Content-Type" content = "text/html; charset=UTF-8">
        <meta name = "viewprot" content = "width = device-width, initial-scale =1" >
        <link href="http://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" media="screen">
    </head>
    <body>
        <div class = "jumbotron container">
        <br>
        <br>
        <h2>This is the Container Producer.</h2>
        <br>
        <p>
            NOTE : please put name as lowercase letter. As typing letter which has any capital letter, it will not run. Port have to be a number which is suggested as a number between 3000 and 9000. after runnung with the name and port, please connect to localhost:"Port_number"
        </p>
        <br>
            <form action="index.php"> 
                Name : <input class="form-control" type="text" name="name" placeholder="please type the name of image in docker"/>
                <br>
                Port : <input class="form-control" type="number" name="port" placeholder="please type the port number"/>
                <br>
                <button class="btn btn-default pull-right">Run</button>
            </form>
        </div>
    <?php
        if (isset($_GET["name"]) && isset($_GET["port"])){
            $name = $_GET["name"];
            $prt = $_GET["port"];  

            if ($name=="") {
                echo 'empty string is not accepted.';
    
            }else{
              $temp = "/usr/local/bin/docker build -t $name .";
              $output = shell_exec($temp);
              echo $temp;
              echo $output;
    
              $temp = "/usr/local/bin/docker run -d -p $prt:80 $name";
              $output = shell_exec($temp);
              echo "\n";
              echo "\n";
              echo "\n";
              echo $temp;
              echo $output;
            }  
        }  
    ?>
    </body>
    <footer>
        <div class ="container">
            <p><b>&copy; Junghwan Yim & Sangwoo Kim</b></p>
        </div>
    </footer>
</html>

