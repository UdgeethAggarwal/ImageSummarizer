<?php

$structure = "upload/";	
/* make sure that directory exists before uploading. If not then try to create directory. Multiple attempts in case of failure */
 
	if (!is_dir($structure)) 
	{
		if(!mkdir($structure, 0777, true))
		{
			mkdir($structure, 0777, true);
		}
	}
	
		$target_dir2 = "uploads/bigstore/".$id."/Gallary/";
/* Change the name of file so that user wont be able to locate it later by other means.*/
$target_file2 = $target_dir2.substr(time(),5).basename($_FILES["fileToUpload"]["name"]);
		$uploadOk = 1;
	
		$imageFileType = pathinfo($target_file2,PATHINFO_EXTENSION);
		// Check if image file is a actual image or fake image
	
		if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg" )  
		{
			$uploadOk = 0;
		}
 
		if ($uploadOk==0) 
		{
			header("Location:next_step.php?id=".$id."&proid=".$t);
		}
		else 
		{
			if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file2)) 
			{
				try
				{
					mysqli_query($connect,"UPDATE `gallery` SET `profile_pic`='$target_file2' WHERE `id`='$id' AND `hid`='$hid'");
					mysqli_close($connect);
					header("Location:next_step.php?id=".$id);
				}
				catch(Exception $e)
				{
					//redirect to upload again on failure. 
					header("Location:upload_profile_pic.php?eid=".$eid."&proid=".$t."&message=failed");
				}
			}
			else
			{
				mysqli_close($connect);
				header("Location: your call .php?id=".$id);
				exit();
			}
		}

?> 