<<<<<<< HEAD
/*
 * My code seems to crash if there is already a folder named "RGB Graphs"
 * Says "too early for import process. 
 * I can't seem to fix this, but it shouldn't be an issue. 
 * If code doesn't work, check if folder name already exists in directory, then delete/change said folder 
 */
 
 
// ==================== main code ====================
=======
//main code
>>>>>>> main
path = getDirectory("Select a directory");
img_list = getFileList(path)


//create folders to place graphs
RGB_dir = path + File.separator + "RGB Graphs" + File.separator;
File.makeDirectory(RGB_dir);
BG_dir = RGB_dir + File.separator + "Background" + File.separator;
CD_dir = RGB_dir + File.separator + "CD" + File.separator;
Flake_dir = RGB_dir + File.separator + "Flake" + File.separator;
<<<<<<< HEAD
File.makeDirectory(Flake_dir);
File.makeDirectory(BG_dir);
File.makeDirectory(CD_dir);

//call all functions one after the other
flakeanalysis(img_list)
bganalysis(img_list)
CDanalysis(img_list)

// ==================== flake analysis ====================
function flakeanalysis(img_list) {
    open(img_list[0]);
    waitForUser("select the rectangle of the flake");
    getSelectionBounds(x, y, w, h);
    run("Close");

    setBatchMode(true);

    for (i = 0; i < img_list.length; i++) {
        if (endsWith(img_list[i], ".tif")) {
            current_img = path + img_list[i];
            open(current_img);
            name = getTitle();
            run("Split Channels");

            ch_nbr = nImages;

            for (c = 1; c <= ch_nbr; c++) {
                selectImage(c);
                makeRectangle(x, y, w, h);
                run("Measure");
            }

            results_name = "RGB results " + name + " flake" + ".csv";
            saveAs("Results", Flake_dir + results_name);
            run("Clear Results");

            run("Close All");
        }
    }

    setBatchMode(false);
}


// ==================== background analysis ====================
function bganalysis(img_list) {
    open(img_list[0]);
    waitForUser("select the rectangle of the background");
    getSelectionBounds(x, y, w, h);
    run("Close");

    setBatchMode(true);

    for (i = 0; i < img_list.length; i++) {
        if (endsWith(img_list[i], ".tif")) {
            current_img = path + img_list[i];
            open(current_img);
            name = getTitle();
            run("Split Channels");

            ch_nbr = nImages;

            for (c = 1; c <= ch_nbr; c++) {
                selectImage(c);
                makeRectangle(x, y, w, h);
                run("Measure");
            }

            results_name = "RGB results " + name + " BG" + ".csv";
            saveAs("Results", BG_dir + results_name);
            run("Clear Results");

            run("Close All");
        }
    }

    setBatchMode(false);
}


// ==================== contrast difference analysis ====================
function CDanalysis(img_list){
	open(img_list[0]); //open one of the images 
	waitForUser("Trace a line from the flake to the background"); //make the initial selection
	getSelectionCoordinates(x, y);
	s = newArray(x.length);
	t = newArray(y.length);
	for (i = 0; i < x.length; i++){
		s[i] = x[i];
		t[i] = y[i];
	}	

	run("Close");

	setBatchMode(true); //batch analyse
	for (i = 0; i < img_list.length; i++){ //for each file in the directory
	
		if (endsWith(img_list[i],".tif")){ //if the file is a tif

			current_img = path + img_list[i]; //select image
			open(current_img);
			run("Split Channels"); //split channels
		
			ch_nbr = nImages ;
	
			for ( c = 1 ; c <= ch_nbr; c++){ //skip the original image, for each RGB channel


				selectImage(c); //select the image of the channel 
				makeLine(s[0], t[0], s[1], t[1]); 
				run("Plot Profile"); //get the profile or plot of the selection
				name = getInfo("image.title"); 
				results_name = "RGB results " + name + " CD" + ".csv";
				Plot.showValues();
				saveAs("Results",CD_dir + results_name);
			
				}
				
			run("Close All");
			}
			
		}	
	
	setBatchMode(false);	
	
=======
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
>>>>>>> main
}
	
