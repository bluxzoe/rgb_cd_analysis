//main code
path = getDirectory("Select a directory");
img_list = getFileList(path)


//create folders to place graphs
RGB_dir = path + File.separator + "RGB Graphs" + File.separator;
File.makeDirectory(RGB_dir);
BG_dir = RGB_dir + File.separator + "Background" + File.separator;
CD_dir = RGB_dir + File.separator + "CD" + File.separator;
Flake_dir = RGB_dir + File.separator + "Flake" + File.separator;
//File.makeDirectory(BG_dir);
File.makeDirectory(CD_dir);
//File.makeDirectory(Flake_dir);

//flakeanalysis(img_list)
//bganalysis(img_list)
CDanalysis(img_list)

//flake analysis
function flakeanalysis(img_list){
	open(img_list[7])
	waitForUser("select the rectangle of the flake");

	setBatchMode(true);
	for (i = 0; i < img_list.length; i++){
	
		if (endsWith(img_list[i],"tif"))

			current_img = path + img_list[i];
			open(current_img);
			name = getTitle();
			run("Split Channels");
		
			ch_nbr = nImages ; 
	
			for ( c = 1 ; c <= ch_nbr ; c++){
		
				selectImage(c);
				run("Restore Selection");
				run("Measure");
			}
			
			results_name = "RGB results " +name + " FLAKE" + ".csv";
			saveAs("Results",Flake_dir + results_name);
			run("Clear Results");
			
		
	run("Close All");
	}		
	setBatchMode(false);
}

//background analysis
function bganalysis(img_list){
	open(img_list[7])
	waitForUser("select the rectangle of the background");

	setBatchMode(true);
	for (i = 0; i < img_list.length; i++){
	
		if (endsWith(img_list[i],"tif"))

			current_img = path + img_list[i];
			open(current_img);
			name = getTitle();
			run("Split Channels");
		
			ch_nbr = nImages ; 
	
			for ( c = 1 ; c <= ch_nbr ; c++){
		
				selectImage(c);
				run("Restore Selection");
				run("Measure");
			}
			
			results_name = "RGB results " + name + " BG" + ".csv";
			saveAs("Results",BG_dir + results_name);
			run("Clear Results");
			
		
	run("Close All");
	}	
	setBatchMode(false);	
}


//contrast difference analysis
function CDanalysis(img_list){
	open(img_list[0])
	waitForUser("trace a line from the flake to the background");

	setBatchMode(true);
	for (i = 0; i < img_list.length; i++){
		print("i=" +i);
		
		if (endsWith(img_list[i],"tif"))
			print("ends with tif");

			current_img = path + img_list[i];
			open(current_img);
			name = getTitle();
			run("Split Channels");
		
			ch_nbr = nImages ; 
	
			for ( c = 1 ; c <= ch_nbr ; c++){
				
				print("ch=" + ch_nbr);
				print("c =" + c);
				
			}
		
				
		}
			
		else {
			print("not tif");
			}
			
		
	run("Close All");
	}		
	setBatchMode(false);
}
	
