<?php
    
    $img = $_POST['image'];
    $folderPath = "upload/";
    $image_parts = explode(";base64,", $img);
    $image_type_aux = explode("image/", $image_parts[0]);
    $image_type = $image_type_aux[1];
  
    $image_base64 = base64_decode($image_parts[1]);
    $fileName = uniqid() . '.jpg';
    
    //$file = 'https://ichef.bbci.co.uk/news/624/cpsprodpb/36E2/production/_109105041_chat_1.png';
    $file = $folderPath . $fileName;
    file_put_contents($file, $image_base64);
    
   // $result = tryme($fileName);
    exec("python3 apicall.py $file",$output);

    $contents = file_get_contents("output.txt");
    $fileOutput = "output.txt";

    exec("python3 abstract.py $fileOutput",$result);
    $msg="hi this is printing";
    print_r($result);
    // print_r($msg);
    // print_r($contents);
    //var_dump($output);
print_r($output);


    // function dopara($filename){
    //     $val=$filename;
    //     return $val;
    // }
  
?>