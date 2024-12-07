//declearing html elements

const imgDiv = document.querySelector('.profile-pic-div');
const file = document.querySelector('#file');
const uploadBtn = document.querySelector('#uploadBtn');
const dp_form = document.querySelector('#dp_form');

//if user hover on img div 
imgDiv.addEventListener('mouseenter', function(){
    uploadBtn.style.display = "block";
});

//if we hover out from img div

imgDiv.addEventListener('mouseleave', function(){
    uploadBtn.style.display = "none";
});


file.addEventListener('change', function(){
    //this refers to file
    const choosedFile = this.files[0];

    if (choosedFile) {
        // Submit the form when a new file is selected
        dp_form.submit();
    }
});

function checkFileSize() {
    const fileInput = document.getElementById('file');
    const maxSizeMB = 2; // Set your desired maximum file size in megabytes

    if (fileInput.files.length > 0) {
        const fileSizeMB = fileInput.files[0].size / (1024 * 1024); // Convert to megabytes

        if (fileSizeMB > maxSizeMB) {
            alert('File size exceeds the maximum allowed size of ' + maxSizeMB + 'MB.');
            fileInput.value = ''; // Clear the file input
        }
    }
}
